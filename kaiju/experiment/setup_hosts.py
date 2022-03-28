import argparse
from common_funcs import run_cmd
from common_funcs import run_cmd_single
from common_funcs import sed
from common_funcs import start_cmd_disown
from common_funcs import start_cmd_disown_nobg
from common_funcs import upload_file
from common_funcs import run_script
from common_funcs import fetch_file_single
from common_funcs import fetch_file_single_compressed
from common_funcs import fetch_file_single_compressed_bg
from threading import Thread, Lock
from experiments import *
import os
import itertools
from datetime import datetime
from os import system 
from time import sleep
SERVERS_PER_HOST = 1
THRIFT_PORT = 8080
KAIJU_PORT=9081
KAIJU_HOSTS_INTERNAL=""
KAIJU_HOSTS_EXTERNAL=""
netCmd = "sudo sysctl net.ipv4.tcp_syncookies=1 > /dev/null; sudo sysctl net.core.netdev_max_backlog=250000 > /dev/null; sudo ifconfig ens3 txqueuelen 10000000; sudo sysctl net.core.somaxconn=100000 > /dev/null ; sudo sysctl net.core.netdev_max_backlog=10000000 > /dev/null; sudo sysctl net.ipv4.tcp_max_syn_backlog=1000000 > /dev/null; sudo sysctl -w net.ipv4.ip_local_port_range='1024 64000' > /dev/null; sudo sysctl -w net.ipv4.tcp_fin_timeout=2 > /dev/null; "
#these lists are IP addresses, not sure if internal or ext-net, will  try both
clients_list = ["10.254.0.5",
                "10.254.0.208",
                "10.254.3.153",
                "10.254.1.51",
                "10.254.3.4"]
server_list = ["10.254.0.182",
                "10.254.2.99",
                "10.254.0.114",
                "10.254.2.87",
                "10.254.3.46"]



def start_servers(**kwargs):
    HEADER = "pkill -9 java; cd /home/ubuntu/kaiju/; rm *.log;"
    HEADER += netCmd
    baseCmd = "java -XX:+UseParallelGC  \
     -Djava.library.path=/usr/local/lib \
     -Dlog4j.configuration=/home/ubuntu/kaiju/src/main/resources/log4j.properties \
     -jar target/kaiju-1.0-SNAPSHOT.jar \
     -bootstrap_time %d \
     -kaiju_port %d \
     -id %d \
     -cluster %s \
     -thrift_port %d \
     -isolation_level %s \
     -ra_algorithm %s \
     -metrics_console_rate %d \
     -bloom-filter-ne %d \
     -max_object_size %d \
     -drop_commit_pct %f \
     -check_commit_delay_ms %d\
     -outbound_internal_conn %d \
     -locktable_numlatches %d \
      1>server-%d.log 2>&1 & "
    setup_hosts()
    sid = 0
    for server in server_list:
        servercmd = HEADER
        for s_localid in range(0, SERVERS_PER_HOST):
            servercmd += (
               baseCmd % (
                   kwargs.get("bootstrap_time_ms", 1000),
                   KAIJU_PORT+s_localid,
                   sid,
                   KAIJU_HOSTS_INTERNAL,
                   THRIFT_PORT+s_localid,
                   kwargs.get("isolation_level"),
                   kwargs.get("ra_algorithm"),
                   kwargs.get("metrics_printrate", -1),
                   kwargs.get("bloom_filter_numbits", 256),
                   max(16384, (100+kwargs.get("valuesize"))*kwargs.get("txnlen")+1000),
                   kwargs.get("drop_commit_pct", 0),
                   kwargs.get("check_commit_delay", -1),
                   kwargs.get("outbound_internal_conn", 1),
                   kwargs.get("locktable_numlatches", 1024),
                   s_localid))
            sid += 1
        pprint("Starting kv-servers on [%s]" % server)
        start_cmd_disown_nobg(server, servercmd)

def setup_hosts():
    pprint("Appending authorized key...")
    run_cmd("all-hosts", "sudo chown ubuntu /etc/security/limits.conf; sudo chmod u+w /etc/security/limits.conf; sudo echo '* soft nofile 1000000\n* hard nofile 1000000' >> /etc/security/limits.conf; sudo chown ubuntu /etc/pam.d/common-session; sudo echo 'session required pam_limits.so' >> /etc/pam.d/common-session")
    run_cmd("all-hosts", "cat /home/ubuntu/.ssh/kaiju_rsa.pub >> /home/ubuntu/.ssh/authorized_keys", user="ubuntu")
    pprint("Done")

    run_cmd("all-hosts", " wget --output-document sigar.tar.gz 'http://downloads.sourceforge.net/project/sigar/sigar/1.6/hyperic-sigar-1.6.4.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fsigar%2Ffiles%2Fsigar%2F1.6%2F&ts=1375479576&use_mirror=iweb'; tar -xvf sigar*; sudo rm /usr/local/lib/libsigar*; sudo cp ./hyperic-sigar-1.6.4/sigar-bin/lib/libsigar-amd64-linux.so /usr/local/lib/; rm -rf *sigar*")
    run_cmd("all-hosts", "sudo echo 'include /usr/local/lib' >> /etc/ld.so.conf; sudo ldconfig")

def fetch_logs(runid, clients, servers, **kwargs):
    def fetchYCSB(rundir, client):
        client_dir = rundir+"/"+"C"+client
        system("mkdir -p "+client_dir)
        fetch_file_single_compressed(client, "/home/ubuntu/kaiju/contrib/YCSB/*.log", client_dir)

    def fetchYCSBbg(rundir, client):
        client_dir = rundir+"/"+"C"+client
        system("mkdir -p "+client_dir)
        sleep(.1)
        fetch_file_single_compressed_bg(client, "/home/ubuntu/kaiju/contrib/YCSB/*.log", client_dir)

    def fetchkaiju(rundir, server, symbol):
        server_dir = rundir+"/"+symbol+server
        system("mkdir -p "+server_dir)
        fetch_file_single_compressed(server, "/home/ubuntu/kaiju/*.log", server_dir)

    def fetchkaijubg(rundir, server, symbol):
        server_dir = rundir+"/"+symbol+server
        system("mkdir -p "+server_dir)
        fetch_file_single_compressed_bg(server, "/home/ubuntu/kaiju/*.log", server_dir)

    outroot = args.output_dir+'/'+runid

    system("mkdir -p "+args.output_dir)

    bgfetch = kwargs.get("bgrun", False)

    ths = []
    pprint("Fetching YCSB logs from clients.")
    
    for i,client in enumerate(clients):
        if not bgfetch:
            t = Thread(target=fetchYCSB, args=(outroot, client))
            t.start()
            ths.append(t)
        else:
            fetchYCSBbg(outroot,client)

    for th in ths:
        th.join()
    pprint("Done clients")

    ths = []
    pprint("Fetching logs from servers.")
    for i,server in enumerate(servers):
        if not bgfetch:
            t = Thread(target=fetchkaiju, args=(outroot, server, "S"))
            t.start()
            ths.append(t)

        else:
            fetchkaijubg(outroot, server, "S")

    for th in ths:
        th.join()
    pprint("Done")

    
    if bgfetch:
        sleep(30)
def run_cmd_in_kaiju(hosts, cmd, user='ubuntu'):
    run_cmd(hosts, "cd /home/ubuntu/kaiju/; %s" % cmd, user)

def pprint(str):
    global USE_COLOR
    if USE_COLOR:
        print '\033[94m%s\033[0m' % str
    else:
        print str
def start_ycsb_clients(**kwargs):
    def fmt_ycsb_string(runType):
        return (('cd /home/ubuntu/kaiju/contrib/YCSB;' +
                 netCmd+
                 'rm *.log;' \
                     'bin/ycsb %s kaiju -p hosts=%s -threads %d -p txnlen=%d -p readproportion=%s -p updateproportion=%s -p fieldlength=%d -p histogram.buckets=%d -p fieldcount=1 -p operationcount=100000000 -p recordcount=%d -p isolation_level=%s -p read_atomic_algorithm=%s -t -s -p requestdistribution=%s -p maxexecutiontime=%d -P %s') 
                     % (                              
                            runType,
                            KAIJU_HOSTS_EXTERNAL,
                                                      kwargs.get("threads", 10) if runType != 'load' else min(1000, kwargs.get("recordcount")/10),
                                                      kwargs.get("txnlen", 8),
                                                      kwargs.get("readprop", .5),
                                                      1-kwargs.get("readprop", .5),
                                                      kwargs.get("valuesize", 1),
                                                      kwargs.get("numbuckets", 10000),
                                                      kwargs.get("recordcount", 10000),
                                                      kwargs.get("isolation_level", "READ_COMMITTED"),
                                                      kwargs.get("ra_algorithm", "KEY_LIST"),
                            kwargs.get("keydistribution", "zipfian"),
                            kwargs.get("time", 60) if runType != 'load' else 10000,
                            kwargs.get("workload", "workloads/workloada")))
    ip_client = clients_list[0]
    pprint("Loading YCSB on single client: %s." % (ip_client))
    run_cmd_single(ip_client, fmt_ycsb_string("load"), time=kwargs.get("recordcount", 180))
    pprint("Done")
    sleep(10)

    pprint("Running YCSB on all clients.")
    if kwargs.get("bgrun", False):
        for client in clients_list:
            start_cmd_disown(client, fmt_ycsb_string("run"))

        sleep(kwargs.get("time")+15)
    else:
        run_cmd("all-clients", fmt_ycsb_string("run"), time=kwargs.get("time", 60)+30)
    pprint("Done")


def run_ycsb_trial(tag, serverArgs="", **kwargs):
    pprint("Running trial %s" % kwargs.get("runid", "no label"))
    pprint("Restarting kaiju clusters %s" % tag)
    #if kwargs.get("killservers", True):
    start_servers(**kwargs)
    sleep(kwargs.get("bootstrap_time_ms", 1000)/1000.*2+5)
    #else:
    #stop_kaiju_clients(clusters)
    start_ycsb_clients(**kwargs)
    runid = kwargs.get("runid", str(datetime.now()).replace(' ', '_'))
    #print "KILLING JAVA"
    #run_cmd("all-servers", "pkill --signal SIGQUIT java")
    fetch_logs(runid, clients_list, server_list)

def jumpstart_hosts():
    pprint("Resetting git...")
    run_cmd_in_kaiju('all-hosts', 'git stash', user="ubuntu")
    pprint("Done")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Setup cassandra on EC2')
    parser.add_argument('--tag', dest='tag', required=True, help='Tag to use for your instances')
    parser.add_argument('--fetchlogs', '-f', action='store_true',
                        help='Fetch logs and exit')
    parser.add_argument('--launch', '-l', action='store_true',
                        help='Launch EC2 cluster')
    parser.add_argument('--claim', action='store_true',
                        help='Claim non-tagged instances as our own')
    parser.add_argument('--kill_num',
                        help='Kill specified number of instances',
                        default=-1,
                        type=int)
    parser.add_argument('--setup', '-s', action='store_true',
                        help='Set up already running EC2 cluster')
    parser.add_argument('--terminate', '-t', action='store_true',
                        help='Terminate the EC2 cluster')
    parser.add_argument('--restart', '-r', action='store_true',
                        help='Restart kaiju cluster')
    parser.add_argument('--rebuild', '-rb', action='store_true',
                        help='Rebuild kaiju cluster')
    parser.add_argument('--fetch', action='store_true',
                        help='Fetch logs')
    parser.add_argument('--rebuild_clients', '-rbc', action='store_true',
                        help='Rebuild kaiju clients')
    parser.add_argument('--rebuild_servers', '-rbs', action='store_true',
                        help='Rebuild kaiju servers')
    parser.add_argument('--num_servers', '-ns', dest='servers', nargs='?',
                        default=2, type=int,
                        help='Number of server machines per cluster, default=2')
    parser.add_argument('--num_clients', '-nc', dest='clients', nargs='?',
                        default=2, type=int,
                        help='Number of client machines per cluster, default=2')
    parser.add_argument('--output', dest='output_dir', nargs='?',
                        default="./output", type=str,
                        help='output directory for runs')
    parser.add_argument('--clusters', '-c', dest='clusters', nargs='?',
                        default="us-east-1", type=str,
                        help='List of clusters to start, command delimited, default=us-east-1:1')
    parser.add_argument('--no_spot', dest='no_spot', action='store_true',
                        help='Don\'t use spot instances, default off.')
    parser.add_argument('--color', dest='color', action='store_true',
                        help='Print with pretty colors, default off.')
    parser.add_argument('-D', dest='kaiju_args', action='append', default=[],
                     help='Parameters to pass along to the kaiju servers/clients.')

    parser.add_argument('--placement_group', dest='placement_group', default="KAIJUCLUSTER")

    parser.add_argument('--branch', dest='branch', default='master',
                        help='Parameters to pass along to the kaiju servers/clients.')

    parser.add_argument('--experiment', dest='experiment',
                     help='Named, pre-defined experiment.')

    parser.add_argument('--ycsb_vary_constants_experiment', action='store_true', help='run experiment for varying constants')

    args,unknown = parser.parse_known_args()

    USE_COLOR = args.color
    pprint("Reminder: Run this script from an ssh-agent!")
    global KAIJU_HOSTS_EXTERNAL
    global KAIJU_HOSTS_INTERNAL
    KAIJU_HOSTS_INTERNAL = None
    for server in server_list:
        for loc_id in range (0,SERVERS_PER_HOST):
            if KAIJU_HOSTS_INTERNAL:
                KAIJU_HOSTS_INTERNAL += ","
                KAIJU_HOSTS_EXTERNAL += ","
            else:
                KAIJU_HOSTS_EXTERNAL = ""
                KAIJU_HOSTS_INTERNAL = ""
            KAIJU_HOSTS_INTERNAL += server + ":" + str(KAIJU_PORT+loc_id)
            KAIJU_HOSTS_EXTERNAL += server + ":" + str(THRIFT_PORT+loc_id)
    kaijuArgString = ' '.join(['-D%s' % arg for arg in args.kaiju_args])
    if args.setup or args.launch:
        setup_hosts()
        jumpstart_hosts()
    if args.experiment:
        firstrun = True
        tag = args.tag
        iteration = 0
        readprop = 0.95
        numkeys = 1000000
        valuesize = 1
        txnlen = 4
        threads = 1000
        drop_commit_pct = 0
        check_commit_delay = -1
        args.output_dir=args.output_dir+"/"+args.experiment+"-"+str(datetime.now()).replace(" ", "-").replace(":","-").split(".")[0]

        system("mkdir -p "+args.output_dir)
        system("cp experiments.py "+args.output_dir)
        
        nc = 5
        ns = 5
        config = "READ_ATOMIC_STAMP"
        run_ycsb_trial(tag, runid=("%s-%d-THREADS%d-RPROP%s-VS%d-TXN%d-NC%s-NS%s-NK%d-DCP%f-CCD%d-IT%d" % (config,
                                                                                                            txnlen,
                                                                                                            threads,
                                                                                                            readprop,
                                                                                                            valuesize,
                                                                                                            txnlen,
                                                                                                            nc,
                                                                                                            ns,
                                                                                                            numkeys,
                                                                                                            drop_commit_pct,
                                                                                                            check_commit_delay,
                                                                                                            iteration)),
                                                               bootstrap_time_ms=10000,
                                                               threads=1000,
                                                               txnlen=4,
                                                               readprop=0.95,
                                                               recordcount=1000000,
                                                               time=60,
                                                               timeout=120*10000,
                                                               ra_algorithm = "TIMESTAMP",
                                                               isolation_level = "READ_ATOMIC",
                                                               keydistribution= "zipfian",
                                                               valuesize=1,
                                                               numbuckets=100,
                                                               metrics_printrate=-1,
                                                               killservers=firstrun,
                                                               drop_commit_pct=drop_commit_pct,
                                                               check_commit_delay=check_commit_delay,
                                                               bgrun=False)
        
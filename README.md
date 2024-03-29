# RA-NOC2 Prototype

This repository contains the prototype for the RA-NOC2 project. It is based on the repository from the SIGMOD 2014 paper titled [Scalable Atomic Visibility with RAMP Transactions](http://www.bailis.org/papers/ramp-sigmod2014.pdf) and includes enhancements to run experiments on ORA, LORA and the OPW version of RAMP-F and RAMP-S. 

Most of the logic for the algorithms is located in the respective ServiceHandler files. For RA-NOC2 the logic is found in ReadAtomicOraBasedServiceHandler.java. Some more logic is found in the MemoryStorageEngine.java class which handles a lot of the server-side logic.

## Setting up the CloudLab Cluster

1. Start an experiment with an OpenStack profile. 
2. Select a link speed of 10Gbps and the required number of nodes (clients + servers) using xl170 from Utah. Please note that the results were calculated using 5 servers and 5 clients unless otherwise specified but the cluster used was always of 50 nodes as that was needed for the scale up experiment.
3. Once the CloudLab experiment is ready, access the OpenStack Dashboard as explained by CloudLab and create clients + servers nodes of size m1.xlarge using the bionic-server image. Make sure to insert the following bash script in the configuration option:

```
#!bin/bash
sudo apt update
sudo apt install -y default-jdk
sudo apt install -y pssh
sudo apt install -y maven
sudo apt install -y python3-pip
pip3 install pexpect
```


4. Next, create one m1.medium instance, which we refer to as the Host and is the machine from which we will run our experiment. 
5. Assign a floating IP to the Host machine, copy the codebase to it, and SSH to it. The codebase should be copied so that in `/home/ubuntu` three folders appear:

- kaiju
- hosts
- results

6. Access the `all-clients.txt` file and write the IP addresses of all client machines, the same for `all-servers.txt`. Finally, in `all-hosts.txt`, write all clients and all servers (servers first).

7. Now, change to the `/home/ubuntu/kaiju/experiment` folder and run `bash setup_cluster.sh`. (It will ask for a password to setup passwordless ssh among all the nodes, it's the same password that is used for the Openstack dahsboard)

Remark: for replication experiments use double the number of server machines.
## Running an Experiment

In `experiments.py`, you will find different experiments that you can run from the RAMP paper. You can expand and modify these experiments by altering the lists of parameters in the dictionary. For example, `default` is a test with default parameters. To run any experiment, change to the `/home/ubuntu/kaiju/experiment` folder and run:

```
python setup_hosts.py --color -c us-west-2 -nc NUM_CLIENTS -ns NUM_SERVERS --experiment EXP --tag example
```
Where `EXP` is the name of the experiment in `experiments.py`, and `NUM_CLIENTS` and `NUM_SERVERS` are the number of physical nodes, by default write 5 and 5.

Alternatively, you can run one of the existing experiments by running:
1. `bash run_default.sh`: runs a simple experiment with default parameters.
2. `bash run_number_clients.sh`: runs an experiment varying the number of client threads.
3. `bash run_number_servers.sh`: runs an experiment varying the number of servers (beware you need enough nodes for this).
etc.

and many others. You can also run all by doing `bash run_all.sh`,this will take several hours and is discourage as if the cluster has any problem in the middle of it you may get faulty results and not realise.

The logs will be uploaded to the `output` folder.

You can process the latest results by calling `bash process_latest_results.sh` or process a specific result by calling `python3 process_results.py "folder_name" "experiment_name"` and adding `--freshness` if you want to process data freshness and not latency/throughput.


## Generate Histories
Running `bash run_default.sh` will generate two histories, one for RAMP-F and one for RAMP-S. (Support of histories for the other algorithms is there but untested, please check if it works before running experiments for them). Run `python3 analyze_server_logs.py <experiment-folder-name> <output-file>` to generate history. Note that experiment folder name is the folder where inside you can find all the folders `C<ip-address>` and `S<ip-address>.`

## Running custom experiments
Modify `experiments.py` and run `python3 process_results.py "folder_name" "experiment_name"` with your new experiment.

## Further Questions

For further information on the codebase, please refer to the [RAMP GitHub repository](https://github.com/pbailis/ramp-sigmod2014-code).

defaultsettings = { "serversList" : [(5,5)],
                    "txnlen" : [16],
                    "threads" : [1000],
                    "numseconds" : 60,
                    "configs" : [ 
                                  "READ_ATOMIC_STAMP", 
                                  "READ_ATOMIC_LORA",
                                  "READ_ATOMIC_LIST",
                                  "READ_ATOMIC_CONST_ORT",
                                  "READ_ATOMIC_NOC",
                                  "READ_ATOMIC_FASTOPW",
                                  #"READ_ATOMIC_SMALLOPW",
                                ],
                    "readprop" : [0.95],
                    "iterations" : range(0,1),
                    "numkeys" : [1000000],
                    "valuesize" : [1],
                    "keydistribution" : ["zipfian"],
                    "bootstrap_time_ms" : 10000,
                    "launch_in_bg" : False,
                    "freshness" : 0,
                    "replication" : 1,
                    "tester" : 0,
                    "drop_commit_pcts" : [0],
                    "check_commit_delays" : [-1],
                 }

tester_RAMPF = { "serversList" : [(2,2)],
                    "txnlen" : [16],
                    "threads" : [1000],
                    "numseconds" : 20,
                    "configs" : [
                                  "READ_ATOMIC_LIST",
                                ],
                    "readprop" : [0.95],
                    "iterations" : range(0,1),
                    "numkeys" : [1000000],
                    "valuesize" : [1],
                    "keydistribution" : ["zipfian"],
                    "bootstrap_time_ms" : 10000,
                    "launch_in_bg" : False,
                    "freshness" : 0,
                    "replication" : 0,
                    "ra_tester" : 1,
                    "drop_commit_pcts" : [0],
                    "check_commit_delays" : [-1],
                 }

tester_RAMPS = { "serversList" : [(2,2)],
                    "txnlen" : [16],
                    "threads" : [1000],
                    "numseconds" : 20,
                    "configs" : [
                                  "READ_ATOMIC_STAMP",
                                ],
                    "readprop" : [0.95],
                    "iterations" : range(0,1),
                    "numkeys" : [1000000],
                    "valuesize" : [1],
                    "keydistribution" : ["zipfian"],
                    "bootstrap_time_ms" : 10000,
                    "launch_in_bg" : False,
                    "freshness" : 0,
                    "replication" : 0,
                    "ra_tester" : 1,
                    "drop_commit_pcts" : [0],
                    "check_commit_delays" : [-1],
                 }

freshness = { "serversList" : [(5,5)],
                    "txnlen" : [16],
                    "threads" : [1000],
                    "numseconds" : 60,
                    "configs" : [ 
                                  "READ_ATOMIC_STAMP", 
                                  "READ_ATOMIC_LORA",
                                  "READ_ATOMIC_LIST",
                                  "READ_ATOMIC_CONST_ORT",
                                  "READ_ATOMIC_NOC",
                                  "READ_ATOMIC_FASTOPW",
                                  #"READ_ATOMIC_SMALLOPW",
                                ],
                    "readprop" : [0.95],
                    "iterations" : range(0,1),
                    "numkeys" : [1000000],
                    "valuesize" : [1],
                    "keydistribution" : ["zipfian","uniform"],
                    "bootstrap_time_ms" : 10000,
                    "launch_in_bg" : False,
                    "freshness" : 1,
                    "tester" : 0,
                    "replication" : 1,
                    "drop_commit_pcts" : [0],
                    "check_commit_delays" : [-1],
                 }

txn_len = { "serversList" : [(5,5)],
                    "txnlen" : [2,4,8,16,32,64,128,256],
                    "threads" : [1000],
                    "numseconds" : 60,
                    "configs" : [ 
                                  "READ_ATOMIC_STAMP", 
                                  "READ_ATOMIC_LORA",
                                  "READ_ATOMIC_LIST",
                                  "READ_ATOMIC_CONST_ORT",
                                  "READ_ATOMIC_NOC",
                                  "READ_ATOMIC_FASTOPW",
                                  #"READ_ATOMIC_SMALLOPW",
                                ],
                    "readprop" : [0.95],
                    "iterations" : range(0,1),
                    "numkeys" : [1000000],
                    "valuesize" : [1],
                    "keydistribution" : ["zipfian"],
                    "bootstrap_time_ms" : 10000,
                    "launch_in_bg" : False,
                    "freshness" : 0,
                    "replication" : 1,
                    "tester" : 0,
                    "drop_commit_pcts" : [0],
                    "check_commit_delays" : [-1],
                 }

read_prop= { "serversList" : [(5,5)],
                    "txnlen" : [16],
                    "threads" : [1000],
                    "numseconds" : 60,
                    "configs" : [ 
                                  "READ_ATOMIC_STAMP", 
                                  "READ_ATOMIC_LORA",
                                  "READ_ATOMIC_LIST",
                                  "READ_ATOMIC_CONST_ORT",
                                  "READ_ATOMIC_NOC",
                                  "READ_ATOMIC_FASTOPW",
                                  #"READ_ATOMIC_SMALLOPW",
                                ],
                    "readprop" : [0,0.3,0.5,0.7,0.95],
                    "iterations" : range(0,1),
                    "numkeys" : [1000000],
                    "valuesize" : [1],
                    "tester" : 0,
                    "keydistribution" : ["zipfian"],
                    "bootstrap_time_ms" : 10000,
                    "launch_in_bg" : False,
                    "freshness" : 0,
                    "replication" : 1,
                    "drop_commit_pcts" : [0],
                    "check_commit_delays" : [-1],
                 }

num_servers = { "serversList" : [(5,5),(10,10),(15,15),(20,20)],
                    "txnlen" : [16],
                    "threads" : [1000],
                    "numseconds" : 60,
                    "configs" : [ 
                                  "READ_ATOMIC_STAMP", 
                                  "READ_ATOMIC_LORA",
                                  "READ_ATOMIC_LIST",
                                  "READ_ATOMIC_CONST_ORT",
                                  "READ_ATOMIC_NOC",
                                  "READ_ATOMIC_FASTOPW",
                                  #"READ_ATOMIC_SMALLOPW",
                                ],
                    "readprop" : [0.95],
                    "iterations" : range(0,1),
                    "numkeys" : [1000000],
                    "valuesize" : [1],
                    "keydistribution" : ["zipfian"],
                    "bootstrap_time_ms" : 10000,
                    "launch_in_bg" : False,
                    "freshness" : 0,
                    "tester" : 0,
                    "replication" : 1,
                    "drop_commit_pcts" : [0],
                    "check_commit_delays" : [-1],
                 }

num_clients = { "serversList" : [(5,5)],
                    "txnlen" : [16],
                    "threads" : [100,250,500,750,1000],
                    "numseconds" : 60,
                    "configs" : [ 
                                  "READ_ATOMIC_STAMP", 
                                  "READ_ATOMIC_LORA",
                                  "READ_ATOMIC_LIST",
                                  "READ_ATOMIC_CONST_ORT",
                                  "READ_ATOMIC_NOC",
                                  "READ_ATOMIC_FASTOPW",
                                  #"READ_ATOMIC_SMALLOPW",
                                ],
                    "readprop" : [0.95],
                    "iterations" : range(0,1),
                    "numkeys" : [1000000],
                    "valuesize" : [1],
                    "keydistribution" : ["zipfian"],
                    "bootstrap_time_ms" : 10000,
                    "launch_in_bg" : False,
                    "freshness" : 0,
                    "replication" : 1,
                    "tester" : 0,
                    "drop_commit_pcts" : [0],
                    "check_commit_delays" : [-1],
                 }

num_keys = { "serversList" : [(5,5)],
                    "txnlen" : [16],
                    "threads" : [1000],
                    "numseconds" : 60,
                    "configs" : [ 
                                  "READ_ATOMIC_STAMP", 
                                  "READ_ATOMIC_LORA",
                                  "READ_ATOMIC_LIST",
                                  "READ_ATOMIC_CONST_ORT",
                                  "READ_ATOMIC_NOC",
                                  "READ_ATOMIC_FASTOPW",
                                  "READ_ATOMIC_SMALLOPW",
                                ],
                    "readprop" : [0.95],
                    "iterations" : range(0,1),
                    "numkeys" : [10,100,1000,10000,100000,1000000],
                    "valuesize" : [1],
                    "replication" : 1,
                    "keydistribution" : ["zipfian"],
                    "bootstrap_time_ms" : 10000,
                    "launch_in_bg" : False,
                    "freshness" : 0,
                    "tester" : 0,
                    "drop_commit_pcts" : [0],
                    "check_commit_delays" : [-1],
                 }

value_size = { "serversList" : [(5,5)],
                    "txnlen" : [16],
                    "threads" : [1000],
                    "numseconds" : 60,
                    "configs" : [ 
                                  "READ_ATOMIC_STAMP", 
                                  "READ_ATOMIC_LORA",
                                  "READ_ATOMIC_LIST",
                                  "READ_ATOMIC_CONST_ORT",
                                  "READ_ATOMIC_NOC",
                                  "READ_ATOMIC_FASTOPW",
                                  "READ_ATOMIC_SMALLOPW",
                                ],
                    "readprop" : [0.95],
                    "iterations" : range(0,1),
                    "numkeys" : [1000000],
                    "valuesize" : [1,10,50,100,500,1000],
                    "keydistribution" : ["zipfian"],
                    "bootstrap_time_ms" : 10000,
                    "launch_in_bg" : False,
                    "freshness" : 0,
                    "replication" : 1,
                    "tester" : 0,
                    "drop_commit_pcts" : [0],
                    "check_commit_delays" : [-1],
                 }
experiments = {
    "default" : defaultsettings,
    "freshness" : freshness,
    "txn_len" : txn_len,
    "read_prop" : read_prop,
    "num_servers" : num_servers,
    "num_clients" : num_clients,
    "num_keys" : num_keys,
    "value_size" : value_size,
    "tester_F" : tester_RAMPF,
    "tester_S" : tester_RAMPS,
}
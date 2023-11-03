TAG="tester"
python3 setup_cluster.py
python setup_hosts.py --color -c us-west-2 --experiment tester_S --tag $TAG


TAG="tester"
python3 setup_cluster.py
python setup_hosts.py --color -c us-west-2 --experiment tester_F --tag $TAG

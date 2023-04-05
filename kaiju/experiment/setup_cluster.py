import argparse
import os

def setup(setup_ssh=False):
    username = "ubuntu"

    file_name = "/home/ubuntu/hosts/all-hosts.txt"

    # Read the contents of the file and store the nodes in a list
    with open(file_name, "r") as f:
        nodes = f.readlines()

    # Remove newline characters from the nodes
    nodes = [node.strip() for node in nodes]
    print("The nodes are: ", nodes)
     
    os.system("cd /home/ubuntu/kaiju ; mvn package")
    if setup_ssh:
        os.system("ssh-keygen -t rsa")
    for node in nodes:
        if setup_ssh:
            os.system(f"ssh-copy-id -o StrictHostKeyChecking=no {username}@{node}")
        os.system(f"scp -prq /home/ubuntu/* {username}@{node}:/home/ubuntu/")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--setup_ssh", action="store_true",help="Setup ssh keys")
    args = parser.parse_args()
    setup(args.setup_ssh)
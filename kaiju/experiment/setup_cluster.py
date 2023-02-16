import os

username = "ubuntu"

file_name = "/home/ubuntu/hosts/all-hosts.txt"

# Read the contents of the file and store the nodes in a list
with open(file_name, "r") as f:
    nodes = f.readlines()

# Remove newline characters from the nodes
nodes = [node.strip() for node in nodes]

os.system("cd /home/ubuntu/kaiju ; mvn package")
os.system("ssh-keygen -t rsa")
for node in nodes:
    os.system(f"ssh-copy-id -o StrictHostKeyChecking=no {username}@{node}")
    os.system(f"scp -prq /home/ubuntu/* {username}@{node}:/home/ubuntu/")
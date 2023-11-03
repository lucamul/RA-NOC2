import csv
import os
import re

def append_transactions_to_csv(log_file_path, output_file_path):
    with open(log_file_path, 'r') as log_file:
        with open(output_file_path, 'w') as output:
            for line in log_file:
                if "TR:" in line:
                    wr_match = re.search(r'[wr]\(([^)]+)\)', line)
                    if wr_match:
                        wr_part = wr_match.group(0)
                        output.write(wr_part + '\n')


def process_tester(dir_name, output_file):
    # create output file and print header
    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['transaction_id', 'type', 'client_id', 'key', 'timestamp'])

    for g in os.listdir(dir_name):
        if g.find("S") == -1:
            continue
        g = dir_name + '/' + g
        s = g.split("/S")[1]
        append_transactions_to_csv(g + '/server-0.log', output_file)

if __name__ == "__main__":
    # get dir_name and output_file as input using parser
    import argparse
    parser = argparse.ArgumentParser(description='Process server logs.')
    parser.add_argument('directory', metavar='directory', type=str, help='directory name')
    parser.add_argument('output_file', metavar='output_file', type=str, help='output file name')
    args = parser.parse_args()
    process_tester(args.directory, args.output_file)
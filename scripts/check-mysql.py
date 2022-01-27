import mysql.connector
from concurrent.futures import ThreadPoolExecutor
import argparse


def main():
    with open(input_file, "r") as myfile:
        content = myfile.read()

    # parse nmap normal format output
    split_port = content.split("3306/tcp")
    with ThreadPoolExecutor(max_workers=20) as executor:
        for port in split_port:
            host_part = port.split("Nmap scan report for ")
            host_part_2 = host_part[len(host_part) - 1].split("(")
            host = host_part_2[0]

            executor.submit(check_server, host, "root")
            executor.submit(check_server, host, "user")
            executor.submit(check_server, host, "gast")
            executor.submit(check_server, host, "guest")

def check_server(host, user):
    try:
        cnx = mysql.connector.connect(host=host, user=user, connection_timeout=5)
        cnx.close()
        print("Connection worked: " + user + "@" + host)
        with open(output_file, "a") as my_file:
            my_file.write(user + "@" + host + "\n")
    except Exception as e:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check MySQL Server conenctions.")
    parser.add_argument(
        "-i", type=str, default="./input.txt", help="Path to nmap scan (normal output format)"
    )
    parser.add_argument(
        "-o", type=str, default="./output.txt", help="Path to output file"
    )
    args = parser.parse_args()
    input_file = args.i
    output_file = args.o
    main()
import os
import subprocess
import argparse
import re


def main(input_file, output_file):
    if os.path.exists(input_file):
        with open(input_file, "r") as myfile:
            content = myfile.readlines()
            for line in content:
                output_string = []
                domain = line.strip()

                host_result = subprocess.run(["host", domain], capture_output=True)
                first_ip_match = re.search("address .*?\\\\n", str(host_result.stdout))
                if first_ip_match:
                    first_ip = first_ip_match.group().replace("address ", "").replace("\\n", "")
                    output_string.append(first_ip)

                    whois_result = subprocess.run(["whois", first_ip], capture_output=True)

                    whois_match = re.search("netname:.*?\\\\n", str(whois_result.stdout))
                    if whois_match:
                        netname = whois_match.group().replace("netname:", "").replace("\\n", "").strip()
                        output_string.append(netname)
                    else:
                        print("No netname found for domain...")
                    

                    try:
                        org_match = re.search("org:.*?\\\\n", str(whois_result.stdout))
                        if org_match:
                            org = org_match.group().replace("org:", "").replace("\\n", "").strip()
                            output_string.append(org)
                    except:
                        print("No org found for domain...")

                with open(output_file, "a") as my_file:
                    print(", ".join(output_string))
                    my_file.write(", ".join(output_string) + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add host infos to domainlist.")
    parser.add_argument("-i", type=str, default="input.txt", help="Input hostlist.")
    parser.add_argument("-o", type=str, default="orgs.txt", help="Output CVE with host and org infos.")
    args = parser.parse_args()
    main(args.i, args.o)
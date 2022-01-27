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
                try:
                    if re.search("\[CVE.*?\]", line):
                        cve = re.search("\[CVE.*?\]", line).group()
                        output_string.append(cve)
                except:
                    pass

                http = re.search("( )?http.*?//.*?(/|,)", line).group().strip().replace(",", "")
                output_string.append(http)

                domain = re.search("//.*?(/|,)", line).group().replace(",", "").replace("//", "").replace("/", "")

                host_result = subprocess.run(["host", domain], capture_output=True)
                first_ip = re.search("address .*?\\\\n", str(host_result.stdout)).group().replace("address ", "").replace("\\n", "")
                output_string.append(first_ip)

                whois_result = subprocess.run(["whois", first_ip], capture_output=True)

                try:
                    output_string.append(re.search("netname:.*?\\\\n", str(whois_result.stdout)).group().replace("netname:", "").replace("\\n", "").strip())
                except:
                    print("No netname found for domain...")
                try: 
                    output_string.append(re.search("org:.*?\\\\n", str(whois_result.stdout)).group().replace("org:", "").replace("\\n", "").strip())
                except:
                    print("No org found for domain...")

                with open(output_file, "a") as my_file:
                    print(", ".join(output_string))
                    my_file.write(", ".join(output_string) + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add host infos to vulns.")
    parser.add_argument("-i", type=str, default="input.txt", help="Input normal url results from nuclei.")
    parser.add_argument("-o", type=str, default="orgs.txt", help="Output CVE with host and org infos.")
    args = parser.parse_args()
    main(args.i, args.o)
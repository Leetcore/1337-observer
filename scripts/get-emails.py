# get emails from domains with crawling
import requests

requests.packages.urllib3.disable_warnings()
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
all_emails = []
max_crawl_depth = 5
max_crawl_count = 1000


def main():
    print("Insert domain:")
    # domain = input()
    domain = "https://www.domain.de"
    domain = domain.strip()
    if domain.startswith("http"):
        start_crawler(domain, 0, 0)
    else:
        start_crawler("https://" + domain + "/", 0, 0)

def start_crawler(url, limit, counter):
    limit = limit + 1
    if limit > max_crawl_depth:
        return

    if counter > max_crawl_count:
        return

    try:
        site_response = request_url(url)
        if site_response is not False and site_response is not None:
            # find links and start crawling!
            soup = BeautifulSoup(site_response.text, "html.parser")
            get_email(site_response)
            parsed_url = urlparse(site_response.url)

            # get html links
            a_tags = soup.find_all("a")
            for a_tag in a_tags:
                counter = counter + 1
                link = a_tag.attrs.get("href")

                if link and link.startswith("/"):
                    port = ""
                    if parsed_url.port:
                        port = ":" + str(parsed_url.port)
                    full_link = (f"{parsed_url.scheme}://{parsed_url.hostname}{port}{link}")
                    start_crawler(full_link, limit, counter)

                # check base tag urls
                base_tag = soup.find("base")
                if base_tag:
                    base = base_tag.attrs.get("href")
                    port = ""
                    if parsed_url.port:
                        port = ":" + str(parsed_url.port)
                    full_link = f"{parsed_url.scheme}://{base}{port}{link}"
                    start_crawler(full_link, limit, counter)

                # absolut urls to same domain
                if link and link.startswith("http:"):
                    if parsed_url.hostname in link:
                        start_crawler(link, limit, counter)

            # get http links
            link_array = re.findall(
                r"(http|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?",
                site_response.text,
            )
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
            session = requests.session()
            session.headers[
                 "User-Agent"
            ] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36 CRAWLER"
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

def get_email(response):
    # print(response.url)

    # find email address in response
    # [\w|-|\.|\+]*@[\w|-|\.|\+]*\.\w*
    email_array = re.findall(r"[\w|-|\.|\+]*@[\w|-|\.|\+]*\.\w*", response.text)

    for email in email_array:
        if email not in all_emails:
            all_emails.append(email)
            print(email)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Crawls a website and finds email adresses."
    )
    args = parser.parse_args()
    main()
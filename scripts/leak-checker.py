from bs4 import BeautifulSoup
import requests

requests.packages.urllib3.disable_warnings()
from concurrent.futures import ThreadPoolExecutor
import colorama

colorama.init(autoreset=True)
import os
import argparse

folder = os.path.dirname(__file__)
visited_pages = []


def main():
    global leaky_paths

    with open(input_file, "r") as myfile:
        content = myfile.readlines()

    with open(leak_file_path, "r") as myfile:
        leaky_paths = myfile.readlines()

    with ThreadPoolExecutor(max_workers=50) as executor:
        for line in content:
            if line.startswith("http"):
                executor.submit(start_crawler, line.strip())
            else:
                executor.submit(start_crawler, "http://" + line.strip() + "/")
                executor.submit(start_crawler, "http://" + line.strip() + ":8080/")
                executor.submit(start_crawler, "http://" + line.strip() + ":8081/")
                executor.submit(start_crawler, "https://" + line.strip() + "/")
                executor.submit(start_crawler, "https://" + line.strip() + ":4434/")
                executor.submit(start_crawler, "https://" + line.strip() + ":8443/")

def start_crawler(url):
    try:
        site_result = request_url(url)
        if not type(site_result) == bool:
            url_comps = site_result.url.split("/")
            for folder_index in range(3, len(url_comps)):
                for leaky_path in leaky_paths:
                    new_url = []
                    l_path = leaky_path.strip()
                    # url magic
                    for index, comp in enumerate(url_comps):
                        if len(url_comps) <= 3 or index < len(url_comps) - (
                            len(url_comps) - folder_index
                        ):
                            new_url.append(comp)
                    new_url.append(l_path)
                    new_site_response = request_url("/".join(new_url))
                    if not type(new_site_response) == bool:
                        # filter result
                        for match_string in [
                            'remote "origin"',
                            "json",
                            "<",
                            "[",
                            "admin",
                        ]:
                            if match_string in new_site_response.text.lower():
                                get_banner(new_site_response)
                                return

    except Exception as e:
        print(e)

def get_banner(response):
    soup = BeautifulSoup(response.text, "html.parser")
    url = response.url
    banner_array = []
    banner_array.append(response.url)
    banner_array.append(response.headers.get("Server"))
    banner_array.append(str(len(response.text)) + " chars")
    try:
        if soup.find("title"):
            title = soup.find("title").get_text().strip().replace("\n", "")
        else:
            title = ""
        banner_array.append(title)
        meta_tags = soup.find_all("meta", attrs={"name": "generator"})
        if len(meta_tags) > 0:
            for meta_tag in meta_tags:
                banner_array.append(meta_tag.attrs.get("content"))
    except Exception as e:
        print(e)
    fullstring = ", ".join(str(item) for item in banner_array)

    print(colorama.Fore.GREEN + fullstring)

    with open(output_file + "_banner.txt", "a") as my_file:
        my_file.write(fullstring + "\n")

    with open(output_file, "a") as my_file:
        my_file.write(url + "\n")

def request_url(url):
    try:
        if url not in visited_pages:
            session = requests.session()
            session.headers[
                "User-Agent"
            ] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36"
            header = session.head(url=url, timeout=3, verify=False)

            # check status code
            if header.status_code >= 400:
                return False

            # check content type
            one_allowed_content_type = False
            for allowed_content_type in ["html", "xml", "plain", "json"]:
                if allowed_content_type in header.headers.get("content-type").lower():
                    one_allowed_content_type = True

            if not one_allowed_content_type or header.is_redirect:
                return False

            response = session.get(url=url, timeout=3, verify=False)
            session.close()

            visited_pages.append(url)
            return response
        else:
            return False
    except Exception as e:
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check leaky urls from subdomain/domain list."
    )
    parser.add_argument(
        "-i", type=str, default="./input.txt", help="Path to input url file"
    )
    parser.add_argument(
        "-o", type=str, default="./output.txt", help="Path to output file"
    )
    parser.add_argument(
        "-leaky", type=str, default="./leaky.txt", help="Path to leaky names"
    )
    args = parser.parse_args()
    input_file = args.i
    output_file = args.o
    leak_file_path = args.leaky
    main()
import requests
requests.packages.urllib3.disable_warnings()
from concurrent.futures import ThreadPoolExecutor
import colorama

colorama.init(autoreset=True)
import os
from bs4 import BeautifulSoup
import argparse

folder = os.path.dirname(__file__)
visited_pages = []
output_strings = []


def main():
    with open(input_file, "r") as myfile:
        content = myfile.readlines()

        with ThreadPoolExecutor(max_workers=100) as executor:
            for line in content:
                executor.submit(start_crawler, "http://" + line.strip() + "/")
                executor.submit(start_crawler, "http://" + line.strip() + ":8080/")
                executor.submit(start_crawler, "http://" + line.strip() + ":8081/")
                executor.submit(start_crawler, "https://" + line.strip() + "/")
                executor.submit(start_crawler, "https://" + line.strip() + ":4434/")
                executor.submit(start_crawler, "https://" + line.strip() + ":8443/")

def start_crawler(url):
    try:
        site_result = request_url(url)
        if site_result is not False:
            get_banner(site_result[0], site_result[1])
    except Exception as e:
        print(e)


def request_url(url):
    try:
        if url not in visited_pages:
            session = requests.session()
            session.headers[
                "User-Agent"
            ] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.152 Safari/537.36"
            header = session.head(url=url, timeout=3, verify=False)
            
            # ignore 404 and error pages
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

            response = session.get(url=url, timeout=2, verify=False)
            session.close()

            soup = BeautifulSoup(response.text, "html.parser")
            visited_pages.append(url)
            return (response, soup)
        else:
            return False
    except Exception as e:
        return False


def get_banner(request, soup):
    banner_array = []
    banner_array.append(request.url)
    banner_array.append(request.headers.get("Server"))
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
    if fullstring not in output_strings:
        output_strings.append(fullstring)
        print(colorama.Fore.GREEN + fullstring)
        with open(output_file + "_banner.txt", "a") as output_1:
            output_1.write(fullstring + "\n")
        with open(output_file, "a") as output_2:
            output_2.write(request.url + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check if domain has an active website and grab banner."
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

import argparse
import requests
from bs4 import BeautifulSoup
import time


def main(input_file, output_file, first):
    # use input file
    current_token = get_first_token()
    if input_file != "no":
        # use input file
        with open(input_file, "r") as myfile:
            content = myfile.readlines()
            for line in content:
                if first == "no":
                    for counter in range(1, 10):
                        urls = get_results(line.strip(), counter, current_token)
                        time.sleep(2)
                        for url in urls:
                            print(url)
                            with open(output_file, "a") as out:
                                out.write(url + "\n")
    else:
        # ask for search query
        print("Search:")
        query = input()
        results = []
        for counter in range(1, 10):
            (urls, token) = get_results(query, counter, current_token)
            results.append(urls)
            time.sleep(2)
        for result in results:
            for url in result:
                print(url)
                with open(output_file, "a") as out:
                    out.write(url + "\n")

def get_first_token():
    session = requests.session()
    session.headers[
        "User-Agent"
    ] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0"
    response = session.get("https://www.startpage.com/")
    session.close()

    soup = BeautifulSoup(response.text, "html.parser")
    token = soup.find("input", name="sc")
    return token

def get_results(string, counter, token):
    search = string
    print("Search for " + search)
    session = requests.session()
    session.headers[
        "User-Agent"
    ] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0"
    response = session.post(
        url="https://www.startpage.com/sp/search",
        data={
            "query": search,
            "lui": "deutsch",
            "language": "deutsch",
            "cat": "web",
            "sc": token,
            "page": str(counter),
            "abp": "-1",
            "t": "dark"
        },
    )
    session.close()

    soup = BeautifulSoup(response.text, "html.parser")
    a_tags = soup.findAll("a", class_="result__url")
    new_token = soup.find("input", name="sc")

    result = []
    for a in a_tags:
        result.append(a.attrs.get("href"))
    return (result, new_token)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check list of strings against startpage search engine and get the results."
    )
    parser.add_argument("-i", type=str, default="no", help="Path to input file")
    parser.add_argument(
        "-o", type=str, default="output.txt", help="Path to output file"
    )
    parser.add_argument(
        "-first", type=str, default="no", help="Get only the first result"
    )
    args = parser.parse_args()
    main(args.i, args.o, args.first)
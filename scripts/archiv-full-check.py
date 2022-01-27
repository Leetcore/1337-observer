import os
import argparse


def main(input_file, folder, batch):
    if input_file != "no":
        # use input file
        with open(input_file, "r") as myfile:
            content = myfile.readlines()
            for line in content:
                start_wizard(line.strip(), folder, batch)
    else:
        # ask for target domain
        print("Target domain:")
        domain = input()
        start_wizard(domain, folder, batch)


def start_wizard(domain, folder, batch):
    domain = domain.strip()
    folder = folder.strip()
    print("Start with: " + domain)
    domain_parts = domain.split("/")
    if len(domain_parts) >= 2:
        domain = domain_parts[2].replace("www.", "")

    if os.path.exists(folder + "/" + domain + "_subs") == False:
        os.system(
            "amass enum -active -brute -w lists/dns.txt -d '"
            + domain
            + "' -dir '"
            + folder
            + domain
            + "_subs' -noalts -max-dns-queries 1500 -rf config/resolver.txt -nolocaldb"
        )

        os.system(
            "python3 scripts/active-checker.py -i '"
            + folder
            + domain
            + "_subs/amass.txt' -o "
            + folder
            + domain
            + "_subs/active.txt"
        )

        os.system(
            "nuclei -tags cve -rl 100 -i '"
            + folder
            + domain
            + "_subs/active.txt' -o '"
            + folder
            + domain
            + "_subs/cve.txt'"
        )

        if batch == "no":
            print("Take screenshots? yes/no")
            screenshot_check = input()
            if screenshot_check.lower() == "yes" or screenshot_check.lower() == "y":
                os.system(
                    "python3 scripts/take-screenshots.py -i '"
                    + folder
                    + domain
                    + "_subs/active.txt' -o "
                    + folder
                    + domain
                    + "_subs/screenshot_log.txt -folder "
                    + folder
                    + domain
                    + "_subs/"
                )

        if batch == "no":
            print("NMAP port scan? yes/no")
            nmap_scan = input()
            if nmap_scan.lower() == "yes" or nmap_scan.lower() == "y":
                os.system(
                    "nmap --top-ports 50 -sV -T5 --open -A --script vulners --script-args mincvss=8 --stats-every 30s -iL '"
                    + folder
                    + domain
                    + "_subs/amass.txt' -oN '"
                    + folder
                    + domain
                    + "_subs/nmap.txt'"
                )
    else:
        print(
            "Folder in "
            + folder
            + " already exist, skip subdomain recon for "
            + domain
            + "."
        )

    if batch == "no":
        print("Check org information for more domains? yes/no")
        domain_check = input()
        if domain_check.lower() == "yes" or domain_check.lower() == "y":
            os.system("amass intel -d " + domain + " -whois -dir " + folder + domain)
            print("Check all new org domains? yes/no")
            full_domain_check = input()
            if full_domain_check.lower() == "yes" or full_domain_check.lower() == "y":
                os.system(
                    "amass enum -active -brute -w lists/dns.txt -df '"
                    + folder
                    + domain
                    + "/amass.txt' -dir '"
                    + folder
                    + domain
                    + "_subs' -noalts -max-dns-queries 1500 -rf config/resolver.txt -nolocaldb"
                )
                os.system(
                    "python3 scripts/active-checker.py -i '"
                    + folder
                    + domain
                    + "_subs/amass.txt' -o '"
                    + folder
                    + domain
                    + "_subs/active.txt'"
                )
                if batch == "no":
                    os.system(
                        "python3 scripts/take-screenshots.py -i '"
                        + folder
                        + domain
                        + "_subs/active.txt' -o "
                        + folder
                        + domain
                        + "_subs/screenshot_log.txt -folder "
                        + folder
                        + domain
                        + "_subs/"
                    )

    if batch == "no":
        print("Crawl websites that we have found? yes/no")
        crawl_check = input()
        if crawl_check.lower() == "yes" or crawl_check.lower() == "y":
            os.system(
                "python3 scripts/crawler.py -i '"
                + folder
                + domain
                + "_subs/active.txt' -o '"
                + folder
                + domain
                + "_subs/crawled.txt'"
            )

            print("Check results with SQLmap? yes/no")
            sql_check = input()
            if sql_check.lower() == "yes" or sql_check.lower() == "y":
                with open(folder + "/" + domain + "_subs/active.txt", "r") as myfile:
                    content = myfile.readlines()
                    for line in content:
                        if (
                            "?" in line.strip()
                            or "=" in line.strip()
                            or "id" in line.strip()
                        ):
                            os.system(
                                "sqlmap -u '"
                                + line.strip()
                                + "' -b --batch --banner --threads 5 --random-agent"
                            )

    if batch == "no":
        print("Check for leaks? yes/no")
        leak_check = input()
        if leak_check.lower() == "yes" or leak_check.lower() == "y":
            os.system(
                "python3 scripts/leak-checker.py -i '"
                + folder
                + domain
                + "_subs/amass.txt' -o '"
                + folder
                + domain
                + "_subs/leaks.txt' -leaky lists/leaky-urls.txt"
            )
            if crawl_check.lower() == "yes" or crawl_check.lower() == "y":
                os.system(
                    "python3 scripts/leak-checker.py -i '"
                    + folder
                    + domain
                    + "_subs/crawled.txt' -o '"
                    + folder
                    + domain
                    + "_subs/leaks.txt' -leaky lists/leaky-urls.txt"
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Crawl websites from subdomain/domain list"
    )
    parser.add_argument("-i", type=str, default="no", help="Path to input file")
    parser.add_argument(
        "-folder", type=str, default="scans/", help="Subfolder to save results."
    )
    parser.add_argument(
        "-batch", type=str, default="no", help="Dont ask for inline questions."
    )
    args = parser.parse_args()
    main(args.i, args.folder, args.batch)

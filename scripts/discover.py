import os
import argparse


def main(input_file, folder, vuln, hard, skip):
    try:
        if input_file != "no":
            # use input file
            with open(input_file, "r") as myfile:
                content = myfile.readlines()
                for line in content:
                    start_wizard(line.strip(), folder, vuln, hard, skip)
        else:
            # ask for target domain
            print("Target domain:")
            domain = input()
            start_wizard(domain, folder, vuln, hard, skip)
    except KeyboardInterrupt as e:
        print(e)

def start_wizard(domain, folder, vuln, hard, skip):
    domain = domain.strip()
    folder = folder.strip()

    print(f"\nStart with: {domain}")
    domain_parts = domain.split("/")
    if len(domain_parts) >= 2:
        domain = domain_parts[2].replace("www.", "")

    if os.path.exists(f"{folder}/{domain}") == True and skip == "yes":
        print(
            "Folder in "
            + folder
            + " already exist, skip subdomain recon for "
            + domain
            + "."
        )
        return

    if os.path.exists(f"{folder}/{domain}") == False:
        os.system(f'mkdir "{folder}/{domain}"')

    if os.path.exists(f'{folder}/{domain}/subs.txt') == False:
        os.system(f'echo "{domain}" > "{folder}/{domain}/subs.txt"')
        os.system(f'~/go/bin/subfinder -d "{domain}" -o "{folder}/{domain}/subs.txt"')

    if os.path.exists(f'{folder}/{domain}/active_banner.txt') == False:
        print("\nCheck if websites are up!")
        os.system(
            "~/go/bin/httpx -nc -fhr -title -tech-detect -server -status-code -p 80,8080,8081,8443,443,4434,4433,8443,5000,1337 -mc 200 -retries 0 -timeout 3 -maxhr 1 -l '"
            + folder
            + domain
            + "/subs.txt' -o '"
            + folder
            + domain
            + "/active_banner.txt'"
        )

    if os.path.exists(f'{folder}/{domain}/active.txt') == False:
        os.system(
            "awk -F' ' '{print $1}' '"
            + folder
            + domain
            + "/active_banner.txt' > '"
            + folder
            + domain
            + "/active.txt'"
        )

    if os.path.exists(f'{folder}/{domain}/crawled.txt') == False:
        os.system(
            "python3 scripts/crawler.py -i '"
            + folder
            + domain
            + "/active.txt' -o '"
            + folder
            + domain
            + "/crawled.txt'"
        )

    if vuln.lower() == "yes":
        if os.path.exists(f'{folder}/{domain}/cve.txt') == False:
            # scan for more vulns
            more_tags = ""
            if hard.lower() == "yes":
                more_tags = ",sqli,rce"
    
                print("\nTesting: Services")
            os.system(
                "nmap -sV -Pn --top-ports 50 --script vulners --script-args mincvss=8 --open -iL '"
                + folder
                + domain
                + "/active.txt' -oN '"
                + folder
                + domain
                + "/nmap.txt'"
            )

            print("\nTesting: Security")
            os.system(
                "~/go/bin/nuclei -l '"
                + folder
                + domain
                + "/active.txt' -tags cve" + more_tags + " -retries 0 -mhe 1 -s critical -o '"
                + folder
                + domain
                + "/cve.txt'"
            )

        if os.path.exists(f'{folder}/{domain}/org.txt') == False and os.path.exists(f'{folder}/{domain}/cve.txt') == True:
            print("\nCheck org/network information!")
            os.system(
                "python3 scripts/add-orginfo.py -i '"
                + folder
                + domain
                + "/cve.txt' -o '"
                + folder
                + domain
                + "/org.txt'"
            )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Full discover list.")
    parser.add_argument("-i", type=str, default="no", help="Path to input file.")
    parser.add_argument(
        "-folder", type=str, default="scans/", help="Subfolder to save results."
    )
    parser.add_argument(
        "-vuln", type=str, default="no", help="Check for critical vulns."
    )
    parser.add_argument(
        "-hard", type=str, default="no", help="Check for critical SQLi or RCE."
    )
    parser.add_argument(
        "-skip", type=str, default="yes", help="Skip folder and scan another target."
    )
    args = parser.parse_args()
    main(args.i, args.folder.lower(), args.vuln.lower(), args.hard.lower(), args.skip.lower())
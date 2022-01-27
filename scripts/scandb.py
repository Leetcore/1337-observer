from censys.search import CensysHosts
import time

h = CensysHosts()

ip_result = []
for count in range(10, 1000):
    for page in h.search('services.http.response.html_title:"Outlook" and location.country=`Germany`', pages=count):
        for result in page:
            print(result["ip"])
            ip_result.append(result["ip"])
        time.sleep(3)

with open("owa_deutschland.txt", "a") as my_file:
    my_file.write("\n".join(ip_result))
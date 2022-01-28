#!/bin/bash

echo "Install golang"
sudo apt install golang nmap curl
echo "Install project discovery"
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
echo "nmap vulners script"
if [[ -f "/usr/share/nmap/scripts/" ]]
then
    curl https://svn.nmap.org/nmap/scripts/vulners.nse > /usr/share/nmap/scripts/vulners.nse
fi
if [[ -f "/opt/homebrew/Cellar/nmap/7.92/share/nmap/scripts/" ]]
then
    curl https://svn.nmap.org/nmap/scripts/vulners.nse > /opt/homebrew/Cellar/nmap/7.92/share/nmap/scripts
fi
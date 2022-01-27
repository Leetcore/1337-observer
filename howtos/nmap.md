# NMAP

## basic scan
``` bash
sudo nmap -sV -sS -sC host
```

## SNMP
``` bash
sudo nmap --script=snmp* -sU IP
```

## Vulners script
Single target:

``` bash
nmap -sV --script vulners --script-args mincvss=9 host
```

Fast host list:

``` bash
nmap --top-ports 50 --open -sV -T5 --script vulners --script-args mincvss=9 --stats-every 60s -iL domains.txt -oN nmap.txt
```

## nmap searchsploit
``` bash
nmap -sV -sC host -oX host.xml
searchsploit --nmap host.xml
```

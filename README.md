## Willkommen bei 1337observer
Ein Repo voller automatisierte Scripte zum Suchen nach kritischen
Schwachstellen in Webanwendungen. Hilfreich für Bug Bounties, 
Capture The Flags und zum Testen der eigenen Infrastruktur.

* Unter /scripts liegt `discover.py`.
* Unter /scans werden standardmäßig die Scans abgelegt.

# Installation
Automatische Installation (getestet auf Kali-Linux):
``` bash
cd setup/
bash setup.sh
```

Die Go Pakete sollten in ~/ sein.

Manuelle Installation:
* Subfinder: https://www.github.com/projectdiscovery/subfinder (MUSS!)
* httpx: https://www.github.com/projectdiscovery/httpx  (MUSS!)
* Nuclei: https://www.github.com/projectdiscovery/nuclei (MUSS!)
* Python 3: https://www.python.org/ (MUSS!)

# Standard Scan:
Das Script `discover.py` automatisiert die Tools. Wenn es ohne
Eingabe ausgeführt wird, fragt es nach einer Domain.

Es kann auch mit einer Liste von Domains im Format `domain.de`
gestartet werden.

Im Hauptordner ausführen:
`python3 scripts/discovery.py -i lists/domains.txt -batch yes`

Standardmäßig wird nur der Recon-Teil gestartet. Dabei wird nach Subdomains
und Hosts gesucht, sowie die laufende Webserver.

## Schwachstellen finden:
Dieser Scan sucht nach CVEs auf den gefundenen Websites.

Im Hauptordner ausführen:
`python3 scripts/discovery.py -vuln yes`

### Hard-Mode:
Der Hard-Mode fügt auch SQLi und RCE hinzu, ohne dass es einen CVE dazu gibt.
Weitere automatisierte Tests auf den gefundenen Websites (dauert länger)

Im Hauptordner ausführen:
`python3 scripts/discovery.py -vuln yes -hard yes`

## Ergebnisse filtern nach Text z.B. Mail, OWA, Wordpress:
Wer spezielle Server/URLs sucht, kann mit `grep` die Ergebnisse filtern und
weiterverarbeiten.
Um alle Mailserver zu checken, die eine erreichbare Webseite haben, filtert 
man im Ordner "scans" die Unterordner der Ergebnisse so:

```
grep -rih owa */active.txt
```
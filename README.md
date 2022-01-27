## Willkommen bei 1337observer
Hier werden einfache Tools und Listen programmiert, um das Internet zu scannen.

* Unter /scripts liegt `discover.py`.
* Unter /scans werden standardmäßig die Scans abgelegt.

# Installation
* Subfinder: https://www.github.com/projectdiscovery/subfinder (MUSS!)
* httpx: https://www.github.com/projectdiscovery/httpx  (MUSS!)
* Nuclei: https://www.github.com/projectdiscovery/nuclei (MUSS!)
* Python 3: https://www.python.org/ (MUSS!)

# Standard Scan:
Das Script `discover.py` automatisiert die Tools.
Man startet mit einer Liste von Domains im Format `domain.de`.

Im Hauptordner ausführen:
`python3 scripts/discovery.py -i lists/domains.txt -batch yes`

## Ergebnisse filtern nach Text z.B. Mail, OWA, Wordpress:

Wer spezielle Server/URLs sucht, kann mit `grep` die Ergebnisse filtern und weiterverarbeiten.
Um alle Mailserver zu checken, die eine erreichbare Webseite haben, filtert man im Ordner "scans"
die Unterordner der Ergebnisse so:

```
grep -rih owa */active.txt
```
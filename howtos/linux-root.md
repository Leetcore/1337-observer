# From user to root
``` bash
find / -perm +6000 2> /dev/null
```

## check apps you can run
``` bash
sudo -l
```

## root flag
``` bash
command_you_can_run --var-in-there="/root/flag.txt"
```

## core dumps
``` bash
ulimit -S -c unlimited
kill -11 pid
cat /var/crash/...
```
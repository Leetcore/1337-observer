# Encoding with Linux


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
echo -n "" | xxd -r -p
```
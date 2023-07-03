# /bin/bash

giturls=(
    "https://github.com/carlospolop/PEASS-ng.git"
    "https://github.com/PowerShellMafia/PowerSploit.git"
    "https://github.com/ly4k/PwnKit.git"
    "https://github.com/mbechler/marshalsec.git"
    "https://github.com/calebstewart/CVE-2021-1675.git"
    "https://github.com/AonCyberLabs/Windows-Exploit-Suggester.git"
    "https://github.com/ropnop/kerbrute.git"
    "https://github.com/SecureAuthCorp/impacket.git"
    "https://github.com/openwall/john.git"
    "https://github.com/djhohnstein/SharpChromium.git"
    "https://github.com/DrorDvash/CVE-2022-22954_VMware_PoC.git"
)

if [[ -d "git" ]]
then
    cd git
else
    mkdir git
    cd git
fi

for url in ${giturls[@]}; do
    filename=$(echo ${url##*/})
    folder=$(echo ${filename%%.git})
    if [[ -d "${folder}" ]]
    then
        cd ${folder}
        git fetch --all
        cd ..
    else
        git clone ${url}
    fi
done
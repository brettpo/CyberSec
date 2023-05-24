#!/bin/bash

# List of domains to check
domains=(
    "admin.inlanefreight.htb"
    "admin.internal.inlanefreight.htb"
    "careers.inlanefreight.htb"
    "cluster14.us.inlanefreight.htb"
    "dc1.inlanefreight.htb"
    "dc2.inlanefreight.htb"
    "dev.ir.inlanefreight.htb"
    "ftp.admin.inlanefreight.htb"
    "internal.inlanefreight.htb"
    "ir.inlanefreight.htb"
    "messagecenter.us.inlanefreight.htb"
    "ns.inlanefreight.htb"
    "resources.inlanefreight.htb"
    "securemessaging.inlanefreight.htb"
    "test1.inlanefreight.htb"
    "us.inlanefreight.htb"
    "wsus.internal.inlanefreight.htb"
    "ww02.inlanefreight.htb"
    "www1.inlanefreight.htb"
)

# ANSI escape sequence for red color
RED='\033[0;31m'
# ANSI escape sequence to reset color
NC='\033[0m'

for domain in "${domains[@]}"
do
    output=$(dig axfr $domain @10.129.112.212 2>/dev/null)
    
    if echo "$output" | grep -q ';; Transfer failed.'; then
        continue
    fi
    
    if echo "$output" | grep -q 'internal'; then
        echo -e "${RED}Zone transfer successful for: $domain${NC}"
        echo "$output" | grep 'IN' | awk '{print $1}' | grep -v '^inlanefreight.htb.' | sed 's/\.$//' | sort -u | awk '{print "\""$0"\""}'
    fi
done

#!/bin/bash
#list of domains to check
domains=(
  "admin.inlanefreight.htb" 
  "ftp.admin.inlanefreight.htb"
  "careers.inlanefreight.htb"
  "dc1.inlanefreight.htb"
  "dc2.inlanefreight.htb"
  "internal.inlanefreight.htb"
  "admin.internal.inlanefreight.htb"
  "wsus.internal.inlanefreight.htb"
  "ir.inlanefreight.htb"
  "dev.ir.inlanefreight.htb"
  "ns.inlanefreight.htb"
  "resources.inlanefreight.htb"
  "securemessaging.inlanefreight.htb"
  "test1.inlanefreight.htb"
  "us.inlanefreight.htb"
  "cluster14.us.inlanefreight.htb"
  "messagecenter.us.inlanefreight.htb"
  "ww02.inlanefreight.htb"
  "www1.inlanefreight.htb"
)

for domain in "${domains[@]}"
do
  echo "Performing zone transfer on: $domain"
  output=$(dig axfr $domain @10.129.112.212)
  if echo "$output" | grep -q ';; transfer failed.'; then
    echo "Zone transfer failed for: $domain"
  else
    echo "Zone transfer successful for: $domain"
    echo "$output"
  fi
done

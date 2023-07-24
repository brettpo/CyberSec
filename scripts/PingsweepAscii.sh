#!/bin/bash

# Input file containing a list of IPs and hostnames
input_file="input_list.txt"

# Output file for ping results
output_file="ping_results.txt"

# Function to get the IP address from a hostname
get_ip_from_hostname() {
    local hostname="$1"
    local ip=$(host "$hostname" | awk '/has address/ {print $NF}')
    echo "$ip"
}

# Check if the input file exists
if [ ! -f "$input_file" ]; then
    echo "Input file '$input_file' not found!"
    exit 1
fi

# Loop through the entries in the input file, ping them, get the IP, and write to the output file
while IFS= read -r entry; do
    if ip=$(get_ip_from_hostname "$entry"); then
        echo "|$entry|$ip" >> "$output_file"
    else
        echo "|$entry|N/A" >> "$output_file"
    fi
done < "$input_file"

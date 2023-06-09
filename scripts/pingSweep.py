import subprocess
import socket

subnet = input("Please enter IP in XXX.XXX.XXX format: ")   # Specify your subnet here
range_start = 1        # Specify the start of the IP range here
range_end = 254        # Specify the end of the IP range here

for ip in range(range_start, range_end + 1):
    target = f"{subnet}.{ip}"
    result = subprocess.run(['ping', '-c', '1', '-W', '1', target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if result.returncode == 0:
        try:
            hostname = socket.gethostbyaddr(target)[0]
        except socket.herror:
            hostname = "Unknown"
        
        print(f"Host {target} is up. Hostname: {hostname}")

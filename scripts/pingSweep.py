import subprocess
import socket
import sys

def print_help():
    print("Usage: python3 pingsweep.py <subnet> [range_start] [range_end] [-v|--verbose]")
    print("       python3 pingsweep.py -h")
    print()
    print("Options:")
    print("  <subnet>        Specify the subnet in XXX.XXX.XXX format")
    print("  [range_start]   Specify the start of the IP range (default: 1)")
    print("  [range_end]     Specify the end of the IP range (default: 254)")
    print("  -v, --verbose   Enable verbose output")
    print("  -h, --help      Show this help message and exit")

def is_valid_subnet(subnet):
    segments = subnet.split(".")
    return len(segments) == 3

if len(sys.argv) == 1 or sys.argv[1] in ("-h", "--help"):
    print_help()
    sys.exit()

subnet = sys.argv[1]   # Retrieve the subnet from command-line argument

if not is_valid_subnet(subnet):
    print("Error: Invalid subnet format. Subnet should be in XXX.XXX.XXX format.")
    sys.exit()

range_start = 1        # Default start of the IP range
range_end = 254        # Default end of the IP range
verbose = False        # Verbose flag, initially set to False

if len(sys.argv) > 2:
    try:
        range_start = int(sys.argv[2])
    except ValueError:
        print("Error: Invalid range start value.")
        sys.exit()

if len(sys.argv) > 3:
    try:
        range_end = int(sys.argv[3])
    except ValueError:
        print("Error: Invalid range end value.")
        sys.exit()

if len(sys.argv) > 4:
    if sys.argv[4] in ("-v", "--verbose"):
        verbose = True

if range_start > range_end:
    print("Error: Range start value cannot be greater than range end value.")
    sys.exit()

if range_start == 1 and range_end == 254:
    print_help()
    sys.exit()

for ip in range(range_start, range_end + 1):
    target = f"{subnet}.{ip}"
    result = subprocess.run(['ping', '-c', '1', '-W', '1', target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if result.returncode == 0:
        try:
            hostname = socket.gethostbyaddr(target)[0]
        except socket.herror:
            hostname = "Unknown"
        
        if verbose:
            print(f"Host {target} is up. Hostname: {hostname}")
        else:
            print(f"Host {target} is up.")
    else:
        if verbose:
            print(f"Host {target} is down.")
        else:
            print(f"Host {target} is down.")

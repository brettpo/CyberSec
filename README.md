# CyberSec
## Cyber security scripts created during my practice on picoCTF


This repo contains any and all scripts that I write for capturing flags on picoCTF
All scripts uploaded will be added and the relevant CTF challenge on picoCTF will be referenced using the challenge name as the file name, the challenge description will be added under the relevant heading in this file

### Basic-Mod-1

We found this weird message being passed around on the servers, we think we have a working decryption scheme. Download the message here. Take each number mod 37 and map it to the following character set: 0-25 is the alphabet (uppercase), 26-35 are the decimal digits, and 36 is an underscore. Wrap your decrypted message in the picoCTF flag format (i.e. picoCTF{decrypted_message})


### PingSweep.py

This is a simple pythin script that i wrote that takes an input from the user in XXX.XXX.XXX. format in order to sweep all IP addresses on a network.


### bruteForceBypass.sh

This is a script I wrote in order to bypass the bruteforce protection on a website that I was authorise to attack, this website contained the user "think" and the password "123" in the html comments. This "think" user was a regular user with valid credentials. 
I used this script in order to generate the usernames.txt file which inserted "think" and the other username found using wpscan, "admin" in alternating lines.
This script also took in a supplied wordlist and inserted "123" into every second line and generated a new password list.
These two files were used with burpsuite pitchfork attack to gain access to the admin account


### passwordCrack4.Decoder.py

This script was created using a password list given within the python program provided by picoCTF in the "PW Crack 4" challenge in order to loop through all the passwords given and find the correct one for the program

### pwCrack5.Decoder.py

This script was created in a similar mannar to passwordCrack4.Decoder.py in order to get the password for the python program provided in the picoCTF challenge "PW Crack 5". This time, a dictionary was provided, but there were white spaces surrounding the passwords, as such the python fuction "strip" was used.

### keygenme-py-solve.py

This script was created in order to solve the challenge "keygenme-py" on picoCTF. This script decodes the key to unlock the full version of the program provided by converting the positions of the username, set out in the if tree in the program, into sha256 and adding them to the first and last parts of the key in order to get the full key

### base64.py

This script was created to solve the ctf challenge "scripting" on tryhackme, URL: https://tryhackme.com/room/scripting.
This script reads a file "b64.txt", decodes the base64 50 times, and prints the flag.

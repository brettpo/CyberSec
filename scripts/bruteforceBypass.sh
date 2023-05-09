#!/bin/bash

## FIRST: Create a wordlist with all the possible passwords
## This script will create a "newPasswords.txt" file with passwords, & a "usernames.txt" file with usernames

## This line creates the password list by taking passwords.txt and inserting "123" (the known password for user "think") every other line
awk ' {print;} NR % 1 == 0 { print "123"; }'  passwords.txt > newPasswords.txt

## These lines create the username list by adding "admin" and "think" 100 times to username.txt
function addName { echo "admin" >> usernames.txt; echo "think" >> usernames.txt; }
for value in {1..110}
do
addName
done

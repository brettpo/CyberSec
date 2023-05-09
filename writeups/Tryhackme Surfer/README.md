# surfer Writeup

##### Room link: https://tryhackme.com/room/surfer

<p align="center">
  <img src="https://tryhackme-images.s3.amazonaws.com/room-icons/6924475c1dc389f44b230968c782d984.png">
</p>

## Tasks:
Uncover the flag on the hidden application page.

## 1. Enumeration
Start by enumerating the open ports using nmap

> Starting Nmap 7.93 ( https://nmap.org ) at 2023-05-09 16:08 SAST
> 
> Nmap scan report for 10.10.14.126
> 
> Host is up (0.19s latency).
> 
> 
> PORT     STATE  SERVICE       VERSION
> 
> 21/tcp   closed ftp
> 
> 22/tcp   open   ssh           OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
> 
> 23/tcp   closed telnet
> 
> 25/tcp   closed smtp
> 
> 53/tcp   closed domain
> 
> 80/tcp   open   http          Apache httpd 2.4.38 ((Debian))
> 
> ...
> 
> Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
> 
> 
> 
> Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
> 
> Nmap done: 1 IP address (1 host up) scanned in 9.18 seconds


We have 2 open ports: 22 and 80.

## Ports

### Port 80:

<p align="center">
  <img src="https://imgur.com/4jYAM8M.png">
</p>

We have a login page, so let's start by trying some common usernames and passwords:

admin:password

root:root

root:password

admin:admin

Admin:admin was a hit!

<p align="center">
  <img src="https://imgur.com/DoEnsgd.png">
</p>

At the bottom of the page there is a button "Export to PDF", which generates a report when clicked:

<p align="center">
  <img src="https://imgur.com/YfoF6FO.png">
</p>

And in the "Recent activity tab" we can see a "/internal/admin.php" directory. 

<p align="center">
  <img src="https://imgur.com/goe5xeu.png">
</p>

But it can "only be accessed locally".

What if we used the "export2pdf" function we saw called earlier, and tried to get a pdf of the webpage?

## Burpsuite

Open burp, and intercept the exporting of the report from the dashboard.

<p align="center">
  <img src="https://imgur.com/BqTfylS.png">
</p>

Edit the url at the bottom to the internal url: 127.0.0.1/internal/admin.php:

<p align="center">
  <img src="https://imgur.com/cQLPB3U.png">
</p>

Forward the request, and we get the flag.

<p align="center">
  <img src="https://imgur.com/TjZ4EST.png">
</p>

## End

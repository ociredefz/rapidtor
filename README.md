rapidtor
========

Introduction
------------

With **rapidtor** you can change the identity in **TOR** network after how many seconds you wants, 
configure your **torserver** and **Vidalia** or **Polipo** with **ControlPort** support, after that use 
this Class to make login and change identity whenever you want.

Howto
-----

First generate the hashed control password:

```bash
deftcode ~ $ tor --quiet --hash-password torpasswd
16:C9B4152185E88628607DE42FA83F01801BD332C8D91ACC6B29CC863F4A
```

Edit the **~/.torrc** configuration file and uncomment the lines below and
then change the **HashedControlPassword** with previously generated hash:

```bash
RunAsDaemon 1
ControlPort 9051
HashedControlPassword 16:C9B4152185E88628607DE42FA83F01801BD332C8D91ACC6B29CC863F4A
```

Force the tor daemon to use your custom configuration file:

```bash
deftcode ~ $ tor --quiet -f ~/.torrc
Mar 07 09:46:12.543 [notice] Tor v0.2.4.20 (git-0d50b03673670de6).
Mar 07 09:46:12.543 [notice] Read configuration file "/home/eurialo/.torrc".
Mar 07 09:46:12.550 [notice] Opening Socks listener on 127.0.0.1:9050
Mar 07 09:46:12.550 [notice] Opening Control listener on 127.0.0.1:9051
Mar 07 09:46:12.550 [notice] Opening OR listener on 0.0.0.0:9001
```

Run rapidtor:

```bash
deftcode ~ $ python rapidtor.py
Authentication....OK!
>> Changed identity in 5 second/s..OK!
>> Changed identity in 5 second/s..OK!
>> Changed identity in 5 second/s..OK!
...
```
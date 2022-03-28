# no-ppap-milter

This Milter rejects the email which has encrypted zip file.

If the MTA receives such email, this will respond `550 5.7.1 We do not accpet encrypted zip.` on the DATA command to reject it.

## Requirements

### CentOS7

```console
yum install -y python3 gcc python3-devel sendmail-devel
```

### Ubuntu 20.04

```console
apt-get install -y python3-pip libmilter-dev
```

## Install

```cosole
pip install no-ppap-milter
```

## Run

This will listen on port 9201 by default.

```
no-ppap-milter
```

If you want to use another port,

```
no-ppap-milter --socket-name inet:1234
```

will listen on port 1234.

If you want to use UNIX domain socket, invoke like this.

```
no-ppap-milter --socket-name unix:/var/run/milter.sock
```

# Returnhome

This script will start or stop a services based on the fact iv one or more of the given IP addresses are reachable. I use it to stop my video surveillance (stop the motion service) when ever my phone is connected to my Wifi.

## Installation and dependencies

I tested the script with Python 3.4.2, it needs the arpreq package which can be obtained with

```pip3 install arpreq```


## Usage

The config file should be self-explanatory
```
[DEFAULT]
LogFile = ./returnhome.log
LogLevel = INFO

[ACTION]
success = sudo systemctl stop motion # action to execute when at least on device is found
failed = sudo systemctl start motion # action to execute when no device is found
service = motion # service name to monitor

[DEVICE0]
IP = 192.168.188.6
VerifyArp = True # Given MAC will be verified against ARP-cache
Mac = 8d:64:e41:6a:61:ff

[DEVICE0]
IP = 192.168.188.101
VerifyArp = False

[DEVICE99]
...
```

Copy the files to your desired directory and let it run as a cronjob.

**The script needs to be run as root**

## Problems
* Some OSes require the command `sudo ping ...` to do a ping. A quick google search should give you an answer how to resolve that issue for your OS.

## License

GNU GPLv3

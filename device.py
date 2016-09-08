import sys
import subprocess
import logging
import re
import arpreq

class Device:

    def __init__(self, ip, verify_arp, mac=''):
        self.ip = ip
        self.verify_arp = verify_arp
        if verify_arp:
            self.mac = mac



    def ping(self):
        logger = logging.getLogger()
        pingcount = '2'
        timeout = '1'
        try:
            p = subprocess.Popen(['ping', '-c ' + pingcount, '-W ' + timeout, self.ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            logger.error(e)
            sys.exit(1)
        stdout, stderr = [x.decode('utf8') for x in p.communicate()]
        if stderr: logger.warn(stderr)
        loss = int(re.search('\d+% packet loss', stdout).group(0).strip('% packet loss'))
        return loss < 100

    def verifyArp(self):
        return arpreq.arpreq(self.ip) == self.mac
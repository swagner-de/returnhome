import sys
import subprocess
import logging
import re
import arpreq
import time

class Device:

    def __init__(self, ip, verify_arp, retryInterval, retryAttempts, mac=''):
        self.ip = ip
        self.verify_arp = verify_arp
        self.retryInterval = retryInterval
        self.retryAttempts = retryAttempts
        if verify_arp:
            self.mac = mac
        self.logger = logging.getLogger()



    def __ping(self):
        logger = logging.getLogger()
        pingcount = '3'
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

    def __verifyArp(self):
        return arpreq.arpreq(self.ip) == self.mac

    def check(self):
        for i in range(0, self.retryAttempts):
            if self.__check(): return True
            if self.mac_failed: return False
            time.sleep(self.retryInterval)
        return False

    def __check(self):
        reachable = False
        if self.__ping():
            self.logger.info(('%s is pingable') % (self.ip))
            if self.verify_arp:
                if self.__verifyArp():
                    self.logger.info(('%s MAC verification successful') % (self.ip))
                    reachable = True
                else:
                    self.logger.info(('%s MAC verification failed') % (self.ip))
                    self.mac_failed = True
            else: reachable = True
        else: self.logger.info(('%s is not reachable') % (self.ip))
        return reachable
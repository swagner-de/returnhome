import os
import sys
import re
import logging
import configparser

from device import Device

class Config:

    def __init__(self, configfile):
        logger = logging.getLogger()
        self.cfg = configparser.ConfigParser()
        try: self.cfg.read(configfile)
        except Exception as e:
            logger.error(e)
            sys.exit(1)
        self.loglevel = self.cfg['DEFAULT']['LogLevel']
        self.scriptdir = os.path.dirname(os.path.realpath(__file__))
        self.logfile = (self.scriptdir + self.cfg['DEFAULT']['LogFile'].strip('.') if './' in self.cfg['DEFAULT']['LogFile'] else self.cfg['DEFAULT']['LogFile'])
        #self.statefile = (self.scriptdir + self.cfg['DEFAULT']['StateFile']. strip('.') if './' in self.cfg['DEFAULT']['StateFile'] == '.' else self.cfg['DEFAULT']['StateFile'])
        self.devices = self._getDevices()
        self.action_success = self.cfg['ACTION']['success']
        self.action_failed = self.cfg['ACTION']['failed']
        self.service = self.cfg['ACTION']['service']


    def _getDevices(self):
        sections = [section for section in self.cfg.sections() if re.search('DEVICE\d+', section)]
        for section in sections:
            yield Device(
                self.cfg[section]['IP'],
                self.cfg[section].getboolean('verifyArp'),
                self.cfg[section].getint('RetryAttempts'),
                self.cfg[section].getint('RetryInterval'),
                self.cfg[section]['Mac'] if 'Mac' in self.cfg[section] else ''
            )
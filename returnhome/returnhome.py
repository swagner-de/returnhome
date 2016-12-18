#!/usr/bin/env python3

import logging
import os
import subprocess
import sys

from config import Config


def check_all_devices(config):
    for device in config.devices:
        if device.check(): return True
    return False

def act(action, config):
    logger = logging.getLogger()
    cmd = config.action_success if action else config.action_failed
    logger.debug('Executing ' + cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = [x.decode('utf8') for x in p.communicate()]
    if stdout: logger.debug('Executed success command. Stdout= ' + stdout.replace('\r', '\t\r'))
    if stderr: logger.error('Executed success command. Stderr= ' + stderr.replace('\r', '\t\r'))


def check_service(service):
    output = subprocess.check_output(['ps', '-A']).decode('utf8')
    logger = logging.getLogger()
    running = service in output
    logger.debug(('Service %s is %s') % (service, 'running' if running else 'stopped'))
    return running

def main(config):
    reachable = check_all_devices(config)
    service_running = check_service(config.service)
    if service_running == reachable:
        logger.info(('%s service %s') % ('Stopping' if service_running else 'Starting', config.service))
        act(service_running and reachable, config)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)) + '/..')
    configfile = 'returnhome.conf'
    config = Config(configfile)

    logger = logging.getLogger()
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s')
    try: logger.setLevel(config.loglevel)
    except ValueError as e : logger.error(e)
    try: fileLogHandler = logging.FileHandler(config.logfile)
    except FileNotFoundError as e:
        logger.error(e)
        sys.exit(1)
    fileLogHandler.setFormatter(formatter)
    logger.addHandler(fileLogHandler)

    main(config)

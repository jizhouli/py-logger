#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Justin<lijt@kuxun.com>
# 2015-04-01 (April Fool's Day)
'''
# USAGE

# import module
from pylogger import logger

logger.info('hello pylogger')

# modify logger configures any time any times you want
logger.config(log_dir='another_log', log_file='another_run.log', rotate_max_byte=1024*1024*512, rotate_backup_count=20)

logger.debug('logger config has been modified')
logger.info('I'm a new log')

# all log types
logger.debug('test debug')
logger.info('test info')
logger.warn('test warn')
logger.error('test error')
logger.critical('test critical')
'''

import os
import sys

import logging
#from logging import handlers
from logging.handlers import RotatingFileHandler

class PyLogger(object):
    '''
    an esay-to-use logging wrapper
    '''
    def __init__(self):
        self.logger = None
        self.handler = None
        self.log_file_path = ''
        self.rotate_max_byte = 0
        self.rotate_backup_count = 0

        self.logger = logging.getLogger()

    def __str__(self):
        s = 'PyLogger config reloaded\n'
        s += 'log file path: %s\n' % self.log_file_path
        s += 'rotate config: maxbyte %s, backupcount %s\n' % (self.rotate_max_byte, self.rotate_backup_count)
        return s

    def get_file_path(self):
        path = sys.path[0]
        if os.path.isdir(path):
            return path
        elif os.path.isfile(path):
            return os.path.dirname(path)
    
    def config(self, log_dir='log', log_file='run.log', rotate_max_byte=1024*1024*256, rotate_backup_count=10):
        self.rotate_max_byte = rotate_max_byte
        self.rotate_backup_count = rotate_backup_count

        # log directory path
        log_dir_path = '/'.join([self.get_file_path(), log_dir])
        if not os.path.exists(log_dir_path):
            os.mkdir(log_dir_path)
        # log file path
        self.log_file_path = '/'.join([log_dir_path, log_file])

        # IMPORTANT! Manually re-assign the handler according to stackoverflow solution
        # http://stackoverflow.com/questions/5296130/restart-logging-to-a-new-file-python
        if self.logger and self.handler:
            self.logger.handlers[0].stream.close()
            self.logger.removeHandler(self.logger.handlers[0])
        
        # create file handler and not set level
        self.handler = RotatingFileHandler(self.log_file_path, 
                maxBytes=self.rotate_max_byte, 
                backupCount=self.rotate_backup_count)
        
        formatter = logging.Formatter("%(asctime)s - %(levelname)s : %(message)s")
        self.handler.setFormatter(formatter)

        # add handler to logger
        self.logger.addHandler(self.handler)

        # set output level
        self.logger.setLevel(logging.INFO)

        # output logger summary
        self.logger.info(str(self).encode('utf8'))

    def debug(self, output):
        self.logger.debug(output.encode('utf8'))

    def info(self, output):
        self.logger.info(output.encode('utf8'))

    def warn(self, output):
        self.logger.warn(output.encode('utf8'))

    def error(self, output):
        self.logger.error(output.encode('utf8'))

    def critical(self, output):
        self.logger.critical(output.encode('utf8'))

# initialize as singleton instance
logger = PyLogger()
logger.config()

if __name__ == '__main__':
    logger.info('hello py-logger')
    logger.config(rotate_max_byte=1000*100, rotate_backup_count=10)
    for i in range(500000):
        # modify logger configures any time any times you want
        if i == 250000:
            logger.config(log_file='new.log', rotate_max_byte=1000*1000, rotate_backup_count=5)
        logger.info('%s this is a test log content so dont be aware' % i)


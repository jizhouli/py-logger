#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import *

from pylogger import logger

def test_logger():
    logger.info('hello py-logger')
    logger.config(rotate_max_byte=1000*100, rotate_backup_count=10)
    for i in range(100000):
        # modify logger configures any time any times you want
        #if i == 50000:
        #    logger.config(log_file='new.log', rotate_max_byte=1000*1000, rotate_backup_count=5)
        logger.info('%s this is a test log content so dont be aware' % i)
    assert_true(True)


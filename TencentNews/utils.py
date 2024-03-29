#-*- coding: utf-8 -*-

import logging
import traceback
import time
import datetime
import requests

logging.basicConfig(filename='crawl.log')

def log(message, level=logging.DEBUG, *args, **kwargs):
    
    logging.log(level, message, *args, **kwargs)

    if level == logging.WARNING or level == logging.ERROR:
        print('%s::[%s]\t%s' % 
            (
            datetime.datetime.now().isoformat()[:10],
            level,
            message
            )
        )
        if level == logging.ERROR:
            msg = "".join(traceback.format_stack())
            logging.log(level, msg, *args, **kwargs)
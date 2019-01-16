#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# ______   ______ _______ _     _ _______ __   _      _______ _______
# |     \ |_____/ |_____| |____/  |______ | \  |         |       |   
# |_____/ |    \_ |     | |    \_ |______ |  \_|         |       |                                                                    
#
#                     http://draken.hu
#
## \file debug.py
## \brief Debugger decorators
## \author Miklos Horvath <hmiki@blackpantheros.eu>
import logging

LOGFILE = "~/.opencallc/debug.log"

log_level = logging.DEBUG

print ("Log level: {}".format(log_level))

logging.basicConfig(filename=LOGFILE,level=log_level, format="---\n%(asctime)s - %(name)s.%(funcName)s\n%(message)s")
Logger = logging.getLogger(__name__)
Logger.addHandler(logging.StreamHandler())

def debug(func):
    """ This is a decorator function which write the exceptions into a LOGFILE.
    """
    def new_func(*args, **kwds):
        try:
            r = func(*args, **kwds)
            if (r is not None) or func.__name__ == "__init__":
                return r
        except Exception as e:
            Logger.error("Exception: {}\n{}".format(func.__name__, e))
        if func.__name__ != "__init__":
            return False
    return new_func

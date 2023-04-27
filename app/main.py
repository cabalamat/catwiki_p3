# main.py = main module for CatWiki

import datetime
import argparse

from flask import request, redirect

from ulib.butil import prn

import allpages
from allpages import *

import config

# pages:
import wiki
import sites
import history

#---------------------------------------------------------------------

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="""\
Start catwiki_p3
""")
    parser.add_argument("-d", "--debug",
        help="Run in debugging mode",
        action="store_true")
    parser.add_argument("-p", "--port",
        help="Port number to use",
        type=int,
        default=config.PORT)
    parser.add_argument("-v", "--verbose",
        help="Make output more verbose",
        action="store_true")
    commandLineArgs = parser.parse_args()
    prn("commandLineArgs=%r" % (commandLineArgs,))
    host = "127.0.0.1" if commandLineArgs.debug else "0.0.0.0"

    app.run(host=host,
        port=commandLineArgs.port,
        debug=commandLineArgs.debug)
    #print("Starting CatWiki (p3)...")

    #app.run(port=config.PORT, debug=True, threaded=True)


#end

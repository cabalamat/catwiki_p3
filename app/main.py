# main.py = main module for CatWiki

import datetime

from flask import request, redirect

import allpages
from allpages import *

import config

# pages:
import wiki
import sites
import history

#---------------------------------------------------------------------

if __name__ == '__main__':
    print("Starting CatWiki (p3)...")
    app.run(port=config.PORT, debug=True, threaded=True)


#end

# allpages.py = stuff relevant to all pages

import os.path
import collections
import html
import datetime
import inspect
import sys

import config

from flask import Flask, request
app = Flask(__name__)
#app.config["SECRET_KEY"] = "don't tell anyone" # not using
app.config["SESSION_COOKIE_NAME"] = "session_%d" % (config.PORT,)
app.config["WERKZEUG_DEBUG_PIN"] = "off"

from ulib import butil
from ulib.butil import printargs

#---------------------------------------------------------------------
# jinja2 environment

import jinja2
from jinja2 import Template

jinjaEnv = jinja2.Environment()
thisDir = os.path.dirname(os.path.realpath(__file__))
templateDir = butil.join(thisDir, "templates")
jinjaEnv.loader = jinja2.FileSystemLoader(templateDir)


#---------------------------------------------------------------------
# utility functions

def form(s, *args, **kwargs):
    return s.format(*args, **kwargs)

def minToHMS(m):
    """ convert a time in minutes into hh:mm:ss
    @param m [int|float]
    @return [str]
    """
    mn = m % 60
    hr = int(m/60.0)
    mn = m - hr*60
    mn2 = int(mn)
    sc = int((mn-mn2)*60)
    r = "{:d}:{:02d}:{:02d}".format(hr, mn2, sc)
    return r

def htmlEscape(s):
    return html.escape(s)
htmlEsc = htmlEscape

#---------------------------------------------------------------------
# debugging

def prt(formatStr="", *args):
    """ For debugging -- print a message, prepended with timestamp, function,
    line number.
    Uses old-style '%' format strings.
    @param formatStr::str
    @param args::[]
    """
    now = datetime.datetime.now()
    nowStr = now.strftime("%H:%M:%S.%f")
    caller = inspect.stack()[1]
    fileLine = caller[2]
    functionName = caller[3]

    if len(args)>0:
        s = formatStr % args
    else:
        s = formatStr
    t = "%s %s():%d: " % (nowStr, functionName, fileLine)
    sys.stderr.write(t + s + "\n")

#---------------------------------------------------------------------

#end

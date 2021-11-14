# butil.py = basic utilities

"""
Basic utilities for Python 3.x.
"""

from typing import *
import os
import os.path
import stat
import fnmatch
import sys
import html
import inspect
import functools
import pprint

#---------------------------------------------------------------------
# file functions

def normalizePath(p: str, *pathParts: List[str]) -> str:
    """ Normalize a file path, by expanding the user name and getting
    the absolute path.
    :param p: a path to a file or directory
    :param pathParts: optional path parts
    :return the same path, normalized
    """
    p1 = os.path.abspath(os.path.expanduser(p))
    if len(pathParts)>0:
        allPathParts = [ p1 ]
        allPathParts.extend(pathParts)
        p1 = os.path.join(*allPathParts)
    p2 = os.path.abspath(p1)
    return p2
normalisePath=normalizePath # alternate spelling
join=normalizePath # it works like os.path.join, but better

def fileExists(fn: str) -> bool:
    """ Does a file exist?
    @param fn  = a filename or pathname
    @return = True if (fn) is the filename of an existing file
        and it is readable.
    """
    fn = os.path.expanduser(fn)
    readable = os.access(fn, os.R_OK)
    # (if it doesn't exist, it can't be readable, so don't bother
    # testing that separately)

    if not readable: return False

    # now test if it's a file
    mode = os.stat(fn)[stat.ST_MODE]
    return stat.S_ISREG(mode)


def entityExists(fn: str) -> bool:
    """ Does a file-like entity (eg. file, symlink, directory) exist?
    @param fn = a filename or pathname
    @return = True if (fn) is the filename of an existing entity.
    """
    fn = os.path.expanduser(fn)
    exists = os.access(fn, os.F_OK)
    return exists

def getFilenames(dir: str, pattern:str="*") -> List[str]:
    """ Return a list of all the filenames in a directory that match a
    pattern. Note that this by default returns files and subdirectories.
    @param dir = a directory
    @param pattern = a Unix-style file wildcard pattern
    @return = the files that matched, sorted in ascii order
    """
    try:
        filenames = os.listdir(dir)
    except:
        filenames = []
    matching = []
    for fn in filenames:
        if fnmatch.fnmatch(fn, pattern):
            matching.append(fn)
    matching.sort()
    return matching


def getFilesDirs(topDir: str) -> Tuple[List[str],List[str]]:
    """ Return a list of all the subdirectories of a directory.
    @param topDir 
    @return = has two members (files, dirs) each of which
       are lists of strings. each member is the basename (i.e. the name
       under (topDir), not the full pathname)
    """
    filesAndDirs = os.listdir(topDir)
    files = []
    dirs = []
    for ford in filesAndDirs:
        fullPath = os.path.join(topDir, ford)
        if isDir(fullPath):
            dirs.append(ford)
        else:
            files.append(ford)
    files.sort()
    dirs.sort()
    return (files, dirs)


def isDir(s: str) -> bool:
    try:
        s = os.path.expanduser(s)
        mode = os.stat(s)[stat.ST_MODE]
        result = stat.S_ISDIR(mode)
        return result
    except:
        return False

#---------------------------------------------------------------------
# read and write files:

def readFile(filename: str) -> str:
    pn = normalizePath(filename)
    f = open(pn, 'r')
    s = f.read()
    f.close()
    return s


def writeFile(filename: str, newValue: str):
    pn = normalizePath(filename)
    # create directories if they don't exist
    dirName = os.path.dirname(pn)
    if dirName:
        if not entityExists(dirName):
            os.makedirs(dirName)
    f = open(pn, 'w')
    f.write(newValue)
    f.close()

#---------------------------------------------------------------------
# formatting functions

def form(fs:str, *args, **kwargs) -> str:
    """ an easier to use version of python's format(). It works the same
    except that %s is converted to {} and %r is converted to {!r}
    """
    if args or kwargs:
        fs2 = fs.replace("%s", "{}").replace("%r", "{!r}")
        r = fs2.format(*args, **kwargs)
    else:
        r = fs
    return r    

def pr(fs:str, *args, **kwargs):
    """ print to stdout """
    sys.stdout.write(form(fs, *args, **kwargs))

def epr(fs:str, *args, **kwargs):
    """ print to stderr """
    sys.stderr.write(form(fs, *args, **kwargs))

def prn(fs:str, *args, **kwargs):
    """ print to stdout, with \n at end """
    sys.stdout.write(form(fs, *args, **kwargs))
    sys.stdout.write("\n")
    
def eprn(fs:str, *args, **kwargs):
    """ print to stderr, with \n at end """
    sys.stderr.write(form(fs, *args, **kwargs))
    sys.stderr.write("\n")


#---------------------------------------------------------------------
# debugging functions

def dpr(formatStr, *args, **kwargs):
    """ debugging version of pr(), prn().
    Prints to stderr, prefixes with function name and line
    number, adds newline.
    """
    caller = inspect.stack()[1]
    fileLine = caller[2]
    functionName = caller[3]
    s = form(formatStr, *args, **kwargs)
    prefix = "%s():%d: " % (functionName, fileLine)
    sys.stderr.write(prefix + s + "\n")

_PRINTARGS_DEPTH = 0
_PRINTARGS_INDENT = "| "

def printargs(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        global _PRINTARGS_DEPTH
        argStr = ", ".join([repr(a) for a in args])
        kwargStr = ", ".join(["%s=%r"%(k,v) for v,k in enumerate(kwargs)])
        comma = ""
        if argStr and kwargStr: comma = ", "
        akStr = argStr + comma + kwargStr
        eprn('%s%s(%s)', _PRINTARGS_INDENT * _PRINTARGS_DEPTH,
           fn.__name__, akStr)
        _PRINTARGS_DEPTH += 1
        retVal = fn(*args, **kwargs)
        _PRINTARGS_DEPTH -= 1
        if retVal != None:
            eprn("%s%s(%s) => %r", _PRINTARGS_INDENT * _PRINTARGS_DEPTH,
               fn.__name__, akStr,
               retVal)
        return retVal
    return wrapper

def pretty(ob, indent:int=4) -> str:
    pp = pprint.PrettyPrinter(indent)
    s = pp.pformat(ob)
    return s


def _prVarsSelf(cLocals, vn):
    selfOb = cLocals['self']
    value = selfOb.__dict__[vn[5:]]
    r = " %s=%r" % (vn, value)
    return r

def dpvars(varNames =None):
    """ debug print values """
    if isinstance(varNames, str):
       vnList = varNames.split()   
    caller = inspect.stack()[1]
    cLocals = caller[0].f_locals # local variables of caller
    #print cLocals
    fileLine = caller[2]
    functionName = caller[3]
    filename = caller[0].f_code.co_filename
    output = "%s():%d" % (functionName, fileLine)
    outputForSelf = " "*len(output)
    printAllSelf = False
    if varNames==None:
        for vn in sorted(cLocals.keys()):
            output += " %s=%r" %(vn, cLocals[vn])
        if cLocals.has_key('self'): printAllSelf = True
    else:    
        for vn in vnList:
            if vn.startswith("self."):
               output += _prVarsSelf(cLocals, vn)     
            elif vn in cLocals:
               output += " %s=%r" %(vn, cLocals[vn]) 
               if vn=='self': printAllSelf = True
    if printAllSelf:
        selfOb = cLocals['self']
        for insVar in sorted(selfOb.__dict__.keys()):
           val = selfOb.__dict__[insVar]
           output += "\n" + outputForSelf + " self.%s=%r"%(insVar,val)
    sys.stderr.write(output + "\n")
   
#---------------------------------------------------------------------

#---------------------------------------------------------------------

def myStr(x):
    """ My version of the str() conversion function. This converts any
    type into a str. If x is a unicode, it is converted into a utf-8
    bytestream.
    @param x = a value of some type
    @return::str
    """
    if x is None:
        return ""
    elif type(x)==unicode:
        return x.encode('utf-8')
    else:
        return str(x)
    
HTML_DECODE = [ ('&#39;', "'"),
                ('&quot;', '"'),
                ('&lt;', '<'),
                ('&gt;', '>'),
                ('&amp;', '&') ]

def attrEsc(s, noneIs=''):
    """ Escapes a string for html attribute special characters
    @param s::str = a string
    @return::str = the equivalent string with chanracters escaped
    """
    if s==None: return noneIs
    if not (isinstance(s, str) or isinstance(s,unicode)):
        s = myStr(s)
    hdc = HTML_DECODE[-1:] + HTML_DECODE[:-1]
    for encoded, decoded in hdc:
        s = s.replace(decoded, encoded)
    return s


def htmlEsc(s: str) -> str:
    return html.escape(s)

def toBytes(b) -> bytes:
    """ convert anything to a byte array """
    if isinstance(b, bytes):
        return b
    elif isinstance(b, str):
        return bytes(b, 'utf-8')
    else:
        return bytes(str(b), 'utf-8')
      

#---------------------------------------------------------------------

class Struct:
    """ an anonymous object whose fields can be accessed using dot
    notation.
    See <http://norvig.com/python-iaq.html>
    """

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __repr__(self):
        keys = sorted(self.__dict__.keys())
        args = ["%s=%r" % (key, self.__dict__[key])
                for key in keys]
        return 'Struct(%s)' % ', '.join(args)

    def hasattr(self, key):
        return self.__dict__.has_key(key)

#---------------------------------------------------------------------


def exValue(f, orValue):
    """ Evaluate function f. If it returns a value, return it.
    If it throws an exception, return (orValue) instead
    @param f::function
    @param orValue
    """
    r = orValue
    try:
        r = f()
    except:
        r = orValue
    return r


#---------------------------------------------------------------------


#end

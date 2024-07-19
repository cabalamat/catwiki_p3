# wiki.py

import os.path, re, math, inspect, datetime, sys

from flask import request, redirect, Response

import markdown
from markdown.extensions.toc import TocExtension
from markdown.extensions.codehilite import CodeHiliteExtension

from ulib import butil
from ulib.butil import form, dpr, printargs

import config
import allpages
from allpages import *
import history
import dirindex


#---------------------------------------------------------------------

@app.route("/<siteName>/w/")
def wikiPageEmptyPath(siteName):
    return wikiPage(siteName, "")

#---------------------------------------------------------------------

@app.route("/<siteName>/w/<path:pathName>")
def wikiPage(siteName, pathName):
    mimeType = getMimeType(pathName)
    if mimeType:
        pan = getDirPan(siteName, pathName)
        data = open(pan, 'rb').read()
        return Response(data, mimetype=mimeType)

    if pathName=="" or pathName[-1:]=="/":

        sortBy = request.args.get('sort')
        # sortBy is 'newest'|'oldest'|None
        dpr("sortBy=%r", sortBy)

        tem = jinjaEnv.get_template("wiki_index.html")
        if sortBy is None:
            title, contents = dirindex.getIndex(siteName, pathName)
        else:
            title, contents = dirindex.getIndexSorted(siteName, pathName, sortBy)
    else:
        tem = jinjaEnv.get_template("wiki_page.html")
        title, contents = getArticleBody(siteName, pathName)

    h = tem.render(
        title = title,
        wikiText = contents,
        siteName = siteName,
        pathName = pathName,
        nav2 = locationSitePath(siteName, pathName),
    )
    return h

MIME_TYPES = [
   ('pdf', 'application/pdf'),
   ('gif', 'image/gif'),
   ('png', 'image/png'),
   ('jpg', 'image/jpeg'),
   ('jpeg', 'image/jpeg'),
   ('xls', 'application/vnd.ms-excel'),
   ('xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
   ('xlst', 'application/vnd.openxmlformats-officedocument.spreadsheetml.template'),
]

def getMimeType(pathName):
    """ Get the mime type of a pathname
    @param pathName::str
    @return::str containing mime type, or "" if none.
    """
    pnl = pathName.lower()
    for ext, mt in MIME_TYPES:
        ext2 = "." + ext
        if pnl[-len(ext2):]==ext2:
            return mt
    #//for
    return ""

#---------------------------------------------------------------------

def pathJoin(sp, ix):
    return "/".join(sp[0:ix+1])

def locationSitePath(siteName: str, pathName: str, xtra: str="") -> str:
    """ return html containing links for a wiki path. This goes at
    the top of the page and is used for navigation.
    @param siteName = which wiki site
    @param pathName = the path (in the url) to the page
    @param xtra = extra text going after the path
    @return a str containing HTML
    """

    useForDir = "<i class='fa fa-folder-open'></i>"
    #useForDir = "<i class='fa fa-chevron-right'></i>"
    #useForDir = "<b>/</b>"
    sp = pathName.split("/")
    h = ("<span class='loc-sitename'><a href='/_allSites'>"
         "<i class='fa fa-bank'></i></a>"
         "<a href='/{siteName}/info'>{siteName}</a></span>").format(
        siteName=siteName)
    h += ("\n<span class='loc-wiki-path'><a href='/%s/w/'>%s</a>"
         % (siteName, useForDir))
    for ix, part in enumerate(sp):
        item = ("<a href='/%s/w/%s'>%s</a>"
            %(siteName, pathJoin(sp,ix), part))
        if ix<len(sp)-1:
            item += ("<a href='/%s/w/%s/'>%s</a>"
                %(siteName, pathJoin(sp,ix), useForDir))
        h += item
    #//for
    if xtra:
        h += " <span class='loc-xtra'>" + xtra + "</span>"
    h += "</span>"
    return h

def getArticleDirname(pathName):
    """ move up to an article's directory """
    sp = pathName.split("/")
    upOne = "/".join(sp[:-1]) + "/"
    return upOne


#---------------------------------------------------------------------

markdownProcessor = markdown.Markdown(extensions=['extra',
    'sane_lists',
    'toc',
    CodeHiliteExtension(guess_lang=False),
    ])

def md(s):
    """ Convert markdown to html

    Uses the Python Markdown library to do this.
    See: <http://packages.python.org/Markdown/>
    """
    h = markdownProcessor.convert(s)
    return h

def convertQuickLinks(s):
    """ Converts [[xxx]] -> [xxx](xxx)
    NB: we are no longer using this, we're using the wikilinks
    extension instead.

    @param s [str] containing markdown source
    @return [str]
    """
    QUICKLINK_RE = r"\[\[([A-Za-z0-9_ -.]+)\]\]"
    REPLACE_WITH = r"[\1](\1)"
    r = re.sub(QUICKLINK_RE, REPLACE_WITH, s)
    return r


def getDirPan(siteName, pathName):
    """ return the pathname for a directory
    @param siteName::str = the site name
    @param pathName::str = the pathname within the site
    @return::str = the full pathname to the directory (which may or may
        not exist). If the site doesn't exist, returns "".
    """
    if not siteName: return ""
    for stub in config.SITE_STUBS:
        _, dirs = butil.getFilesDirs(stub)
        if siteName in dirs:
            return butil.join(stub, siteName, pathName)
    #//for
    return ""


def getArticleBody(siteName, pathName):
    """ given an article name, return the body of the article.
    @return ::(str,str) =title,html
    """
    articlePan = getArticlePan(siteName, pathName)
    if butil.fileExists(articlePan):
        src = butil.readFile(articlePan)
        src = convertQuickLinks(src)
        contents = md(src)
        return pathName, contents
    else:
        h = form("<p>({pathName} does not exist; "
            "<a href='/{siteName}/wikiedit/{pathName}'>create it</a>)</p>\n",
            siteName = htmlEscape(siteName),
            pathName = htmlEscape(pathName))
        return (pathName, h)

def getArticlePan(siteName, pathName):
    """ return the pathname for an article
    @param siteName::str = the site name
    @param pathName::str = the pathname within the site
    @return::str = the full pathname to the article (which may or may
        not exist). If the site doesn't exist, returns "".
    """
    if not siteName: return ""
    for stub in config.SITE_STUBS:
        _, dirs = butil.getFilesDirs(stub)
        if siteName in dirs:
            return getArticlePan2(stub, siteName, pathName)
            #return butil.join(stub, siteName, pathName + ".md")
    #//for
    return ""

def getArticlePan2(stub, siteName, pathName):
    """ return the pathname for an article, given the stub of the directory
    hierarchy to get it from.
    @param stub::str = the leftmost part of the pathname, to just before
        the siteName, e.g.:
        "/home/someuser/siteboxdata/sites"
    @param siteName::str = the site name
    @param pathName::str = the pathname within the site
    @return::str = the full pathname to the article (which may or may
        not exist). If the site doesn't exist, returns "".
    """
    pathNameParts = pathName.split("/")
    pnLastPart = pathNameParts[-1]
    normLP = normArticleName(pnLastPart)
    pathName2 = "/".join(pathNameParts[:-1] + [normLP])
    
    useDir = butil.join(stub, siteName, "/".join(pathNameParts[:-1]))
    if articleExists(useDir, normLP):
        return butil.join(useDir, normLP + ".md")
    
    # article doesn't exist under the normalised name, look elsewhere:
    articleNames = getArticleFilesWithoutExt(useDir)
    for an in articleNames:
        nan = normArticleName(an)
        if nan==normLP:
            return butil.join(useDir, an + ".md")
    #//for    
    
    # couldn't find it elsewhere, use the normalised name
    return butil.join(useDir, normLP + ".md")
    
    pn = butil.join(stub, siteName, pathName2 + ".md")
    return pn
     
def articleExists(d, an):
    """
    @param d::str = a full path to a directory
    @param an::str = a filename within that directory, but without the 
        ".md" extension 
    @return::bool = whether the article (an) exists    
    """
    pan = butil.join(d, an + ".md")
    return butil.fileExists(pan)

 
def getArticleFilesWithoutExt(d):
    """
    @param d::str = a full path to a directory
    @return::[str] where each string is an article in the directory without
        the ".md" extension
    """
    fns, _ = butil.getFilesDirs(d)
    arts = sorted([fn[:-3]
                   for fn in fns
                   if fn[-3:]==".md" and not fn[:1]=="~"])
    return arts



#---------------------------------------------------------------------

#---------------------------------------------------------------------
# functions for nirmalising wiki page names

def normArticleName(an):
    """ Normalise an article name e.g. "Hello" -> "hello"
    Characters [a-z0-9-] are passed through as is
    Characters [A-Z] are converted to lower case
    Any group of 1 or more other characters is replaced by a single "_"
    After this, beginning/ending "_" are removed.
    
    @param an::str = article name gtrom http request
    @return::str = normalised filename to look for
    """
    PASS_THROUGH = "abcdefghijklmnopqrstuvwxyz0123456789-"
    TO_LOWER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    r = ""
    for ch in an:
        if ch in PASS_THROUGH:
            r += ch
        elif ch in TO_LOWER:
            r += ch.lower()
        else:
            if r[-1:] != "_":
                r += "_"
    #//for
    r2 = r.strip("_")
    return r2



#---------------------------------------------------------------------

#end

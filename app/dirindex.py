# dirindex.py = pages for indexes for directories/folders

"""
Contains the getIndex(), getIndexSorted() functions, which were in <wiki.py>
"""

import os.path, re, math, inspect, datetime, sys

from flask import request, redirect, Response

from ulib import butil
from ulib.butil import form, dpr, printargs

import config
import allpages
from allpages import *


#---------------------------------------------------------------------

def getIndex(siteName, pathName):
    """ get an index of a directory.
    @param siteName::str
    @param pathName::str
    @return::(str,str) = title,html
    """
    from wiki import getDirPan

    def isArticle(fn):
        """ is a filename an article? """
        return (fn[-3:]==".md" and not fn[:1]=="~")

    if pathName[-1:] == "/":
        uPath = pathName[:-1]
    else:
        uPath = pathName
    dirPan = getDirPan(siteName, uPath)
    if not os.path.isdir(dirPan):
        h = "<p>Directory {} does not exist.</p>\n".format(pathName)
        return h

    fns, dirs = butil.getFilesDirs(dirPan)
    dirs = [d for d in dirs if d[:1] != "."]
    arts = sorted([fn[:-3]
                  for fn in fns
                  if isArticle(fn)])
    nonArticles = sorted([fn
                  for fn in fns
                  if not isArticle(fn)])
    dirs = sorted(dirs)
    h = ("<h1><i class='fa fa-list'></i> Index of articles in "
         " /{}</h1>\n").format(pathName)
    items = []
    nonArticleItems = []
    if arts:
        for fn in arts:
            text = getTitle(butil.join(dirPan, fn+".md"))
            if text==fn:
                text = ""
            else:
                text = " - " + text

            if fn=="home":
                item = form("<a href='{fn}'>"
                    "<span class='home-icon'><i class='fa fa-home'></i></span>"
                    " {fn}</a>{text}",
                    fn = fn,
                    text = text)
            else:
                item = form("<a href='{fn}'>"
                    "<i class='fa fa-file-text-o'></i> {fn}</a>{text}",
                    fn = fn,
                    text = text)

            items.append(item)
        #//for
        h += bsColumns(items, 3)
    if nonArticles:
        for fn in nonArticles:
            hf = form("<a href='{fn}'>"
                "<i class='fa fa-file-o'></i> "
                "{fn}</a>",
                fn = fn)
            if hasImageExtension(fn):
                hf += form("<br>\n<a href='{fn}'>"
                    "<img class='index_image' src='{fn}'>"
                    "</a>",
                    fn = fn)
            nonArticleItems.append(hf)
        #//for
        h += "<h3>Other files</h3>\n" + bsColumns(nonArticleItems, 3)
    if dirs:
        dirItems = []
        for d in dirs:
            dirItems.append(("<a href='{d}/'><i class='fa fa-folder'></i> "
                  "{text}</a>").format(
                d = d,
                text = d,
            ))
        #//for
        h += "<h3>Folders</h3>\n" + bsColumns(dirItems, 3)

    title = "Index of {}".format(pathName)
    return title, h

#---------------------------------------------------------------------

def getIndexSorted(siteName, pathName, sortBy):
    """ get an index of a directory.
    @param siteName::str
    @param pathName::str
    @param sortBy::'oldest'|'newest' = sort order
    @return::(str,str) = title,html
    """
    from wiki import getDirPan

    def isArticle(fn):
        """ is a filename an article? """
        return (fn[-3:]==".md" and not fn[:1]=="~")

    if pathName[-1:] == "/":
        uPath = pathName[:-1]
    else:
        uPath = pathName
    dirPan = getDirPan(siteName, uPath)
    if not os.path.isdir(dirPan):
        h = "<p>Directory {} does not exist.</p>\n".format(pathName)
        return h

    fns, dirs = butil.getFilesDirs(dirPan)
    #timestampedFns = [(fn, timestamp(fn)) for fn in fns]
    dirs = [d for d in dirs if d[:1] != "."]
    arts = sorted([fn[:-3]
                  for fn in fns
                  if isArticle(fn)])
    nonArticles = sorted([fn
                  for fn in fns
                  if not isArticle(fn)])
    dirs = sorted(dirs)
    h = ("<h1><i class='fa fa-list'></i> Index of articles in "
         " /{}</h1>\n").format(pathName)
    items = []
    nonArticleItems = []
    if arts:
        for fn in arts:
            text = getTitle(butil.join(dirPan, fn+".md"))
            if text==fn:
                text = ""
            else:
                text = " - " + text

            if fn=="home":
                item = form("<a href='{fn}'>"
                    "<span class='home-icon'><i class='fa fa-home'></i></span>"
                    " {fn}</a>{text}",
                    fn = fn,
                    text = text)
            else:
                item = form("<a href='{fn}'>"
                    "<i class='fa fa-file-text-o'></i> {fn}</a>{text}",
                    fn = fn,
                    text = text)

            items.append(item)
        #//for
        h += bsColumns(items, 3)
    if nonArticles:
        for fn in nonArticles:
            hf = form("<a href='{fn}'>"
                "<i class='fa fa-file-o'></i> "
                "{fn}</a>",
                fn = fn)
            if hasImageExtension(fn):
                hf += form("<br>\n<a href='{fn}'>"
                    "<img class='index_image' src='{fn}'>"
                    "</a>",
                    fn = fn)
            nonArticleItems.append(hf)
        #//for
        h += "<h3>Other files</h3>\n" + bsColumns(nonArticleItems, 3)
    if dirs:
        dirItems = []
        for d in dirs:
            dirItems.append(("<a href='{d}/'><i class='fa fa-folder'></i> "
                  "{text}</a>").format(
                d = d,
                text = d,
            ))
        #//for
        h += "<h3>Folders</h3>\n" + bsColumns(dirItems, 3)

    title = "Index of {}".format(pathName)
    return title, h

#---------------------------------------------------------------------
# helper functions

def getTitle(pan):
    """ get the title of an article
    @param pan [str] full pathname to the article
    """
    from wiki import md, convertQuickLinks
    #src = butil.readFile(pan).decode('utf-8', 'ignore')
    src = butil.readFile(pan)
    lines = src.split("\n")
    if len(lines)==0: return ""
    t = md(convertQuickLinks(lines[0].strip(" #")))
    if t.startswith("<p>"): t = t[3:]
    if t.endswith("</p>"): t = t[:-4]
    return t


def bsColumns(hs, numColumns, linSize='md'):
    """ Bootstrap multiple columns
    @param hs::[str] = each string contains html
    @param numColumns::int = number of columns. values are 2|3|4|6.
    @param linSize::str = linearize on size. Linearize means revert to a
        one-column setup when screen width gets below a certain size. Allowed
        values are:
       'xs' = never linearize
       'sm' = on <768 pixels
       'md' = on <992 pixels
       'lg' = on <1200 pixels
    @return::str containing html
    """
    if numColumns not in (2,3,4,6) or len(hs)<2*numColumns:
        h = ("""<div class='container-fluid'><div class='row'>
            <div class='col-md-12'>
            """
            + "<br>\n".join(hs)
            + "</div></div></div>\n")
        return h
    columnClass = "col-{}-{}".format(linSize, int(12/numColumns))
    itemsPerRow = int(math.ceil(len(hs)*1.0 / numColumns))

    h = "<div class='container-fluid'><div class='row'>\n"
    for rowIx in range(numColumns):
        f = itemsPerRow * rowIx
        useHs = hs[f:f+itemsPerRow]
        h += form("""<div class='{columnClass}'>
{elements}
</div>
""",
            columnClass = columnClass,
            elements = "<br>\n".join(useHs))
    #//for row
    h += "</div></div>\n"
    return h

def hasImageExtension(fn):
    """ Does a filename have an extension indicating it's an image?
    @param fn::str = the filename
    @return::bool
    """
    root, ext = os.path.splitext(fn)
    if ext[:1] != ".": return False # no extension, not an image

    IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif']
    ext2 = ext[1:].lower()
    if ext2 in IMAGE_EXTENSIONS:
        return True
    return False




#---------------------------------------------------------------------



#end

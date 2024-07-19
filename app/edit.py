# edit.py = editing a wiki page

import datetime
import os, os.path
import shutil

from flask import request, redirect, Response

from ulib.butil import form, dpr, printargs

import allpages
from allpages import *

import history
import wiki

#---------------------------------------------------------------------


@app.route("/<siteName>/wikiedit/<path:pathName>", methods=['POST', 'GET'])
def wikiedit(siteName, pathName):
    prt("siteName=%r pathName=%r", siteName, pathName)
    tem = jinjaEnv.get_template("wikiedit.html")

    if pathName=="" or pathName[-1:]=="/":
        # can't edit directories
        return redirect("/{siteName}/w/{pathName}".format(
                siteName = siteName,
                pathName = pathName,
            ), 301)
    else:
        source = getArticleSource(siteName, pathName)
        if source == "":
            source = "# " + pathName + "\n"
    if request.method=='POST':
        if request.form['delete'] == "1":
            # delete this article
            deleteArticle(siteName, pathName)
            articleDirectory = getArticleDirname(pathName)
            return redirect("/{siteName}/w/{pathName}".format(
                    siteName = siteName,
                    pathName = articleDirectory,
                 ), 303)
        else:
            dpr("Saving changes...")
            newSource = request.form['source']
            dpr("newSource=%r", newSource)
            saveArticleSource(siteName, pathName, newSource)

            return redirect("/{siteName}/w/{pathName}".format(
                    siteName = siteName,
                    pathName = pathName,
                 ), 303)
    #//if
    title = pathName

    h = tem.render(
        title = title,
        siteName = siteName,
        pathName = pathName,
        nav2 = wiki.locationSitePath(siteName, pathName,
            "<i class='fa fa-edit'></i> edit"),
        source = source,
    )
    prt("response length %d", len(h))
    return h

def deleteArticle(siteName, pathName):
    """ delete an article """
    pan = getDirPan(siteName, pathName)
    if pan:
        os.remove(pan + ".md")

#---------------------------------------------------------------------

def getArticleSource(siteName, pathName):
    articlePan = wiki.getArticlePan(siteName, pathName)
    if butil.fileExists(articlePan):
        src = butil.readFile(articlePan)
        return src
    else:
        return ""

def saveArticleSource(siteName, pathName, source):
    #pr("saving article %s:[%s] -----BODY:-----\n%s\n-----END-----",
    #    siteName, pathName, source)
    articlePan = wiki.getArticlePan(siteName, pathName)
    ensureHistExists(articlePan)
    butil.writeFile(articlePan, source)
    saveCopyToHist(articlePan)


#---------------------------------------------------------------------

def ensureHistExists(articlePan: str):
    """ ensure a .HIST/ directory exists under the directory in
    (pathName)
    """
    prt("articlePan=%r", articlePan)
    baseDir = os.path.dirname(articlePan)
    prt("baseDir=%r", baseDir)
    files, dirs = butil.getFilesDirs(baseDir)
    prt("files=%r dirs=%r", files, dirs)
    if ".HIST" not in dirs:
        makeHistDir(baseDir, populate=True)

def makeHistDir(baseDir: str, populate: bool = False):
    """ make a .HIST dir underneath (baseDir).
    if (populate), populate it with all the articles in baseDir.
    """
    histDir = butil.join(baseDir, ".HIST")
    os.makedirs(histDir)
    if not populate: return

    #>>>> populating .HIST
    files, _ = butil.getFilesDirs(baseDir)
    dpr("files=%r", files)
    mdFns = [fn for fn in files if fn.endswith(".md")]
    for mdFn in mdFns:
        dpr("mdFn=%r", mdFn)
        stub = mdFn[:-3]
        if not stub: continue
        normalisedName = wiki.normArticleName(stub)
        dpr("normalisedName=%r", normalisedName)
        lastAltered = getAlteredTimestamp(butil.join(baseDir, mdFn))

        histFn = "%s.%s.md" % (normalisedName, lastAltered)

        # copy the file into .HIST:
        shutil.copyfile(
            butil.join(baseDir, mdFn),
            butil.join(baseDir, ".HIST", histFn))

    #//for

def saveCopyToHist(articlePan: str):
    """ save a copy of (articelPan) to .HIST
    (which we presume exists)
    """
    baseDir, stub = os.path.split(articlePan)
    normalisedName = wiki.normArticleName(stub[:-3])
    lastAltered = getAlteredTimestamp(articlePan)
    histFn = "%s.%s.md" % (normalisedName, lastAltered)

    # copy the file into .HIST:
    shutil.copyfile(
        butil.join(articlePan),
        butil.join(baseDir, ".HIST", histFn))


def getAlteredTimestamp(pan: str) -> str:
    """ (pan) is a full pathname to a file.
    Returns the timestamp it was last altered,
    in the format "yyyymmdd_HHMMSS"
    """
    statinfo = os.stat(pan)
    lastAccess = statinfo.st_mtime
    dt = datetime.datetime.fromtimestamp(lastAccess)
    dts = dt.strftime("%Y%m%d_%H%M%S")
    dpr("lastAccess=%r dts=%r", lastAccess, dts)
    return dts

def readHist(siteName, pathName, histFn) -> str:
    """ read a history file """
    articlePan = wiki.getArticlePan(siteName, pathName)
    baseDir, _ = os.path.split(articlePan)
    histPan = butil.join(baseDir, ".HIST", histFn)
    data = butil.readFile(histPan)
    return data



#---------------------------------------------------------------------



# edit.py = aditing a wiki page

import datetime

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
            wiki.saveArticleSource(siteName, pathName, newSource)

            # update git repository
            history.commitChanges(siteName, pathName)

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
        nav2 = wiki.locationSitePath(siteName, pathName),
        source = source,
    )
    prt("response length %d", len(h))
    return h


def getArticleSource(siteName, pathName):
    articlePan = wiki.getArticlePan(siteName, pathName)
    if butil.fileExists(articlePan):
        src = butil.readFile(articlePan)
        return src
    else:
        return ""

#---------------------------------------------------------------------


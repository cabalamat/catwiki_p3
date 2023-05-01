# history.py

import os.path, datetime, time
import difflib


from flask import request, redirect, Response

from ulib import butil
from ulib.butil import form, dpr, dpvars

import allpages
from allpages import *

import wiki
import edit

#---------------------------------------------------------------------

@app.route("/<siteName>/history/<path:pathName>")
def history(siteName, pathName):
    dpr("siteName=%r pathName=%r", siteName, pathName)
    tem = jinjaEnv.get_template("history.html")

    diffFrom = request.args.get("diffFrom")
    diffTo = request.args.get("diffTo")
    dpr("diffFrom=%r diffTo=%r", diffFrom, diffTo)
    if diffFrom and diffTo and diffFrom != diffTo:
        # redirect to histdiff page
        if diffFrom > diffTo:
            diffFrom, diffTo = diffTo, diffFrom
        url = form("/{siteName}/histdiff/{pathName}"
            "?old={oldhfn}"
            "&new={newhfn}",
            siteName = siteName,
            pathName = pathName,
            oldhfn = diffFrom,
            newhfn = diffTo)
        return redirect(url)
    
    h = tem.render(
        title = pathName,
        siteName = siteName,
        pathName = pathName,
        nav2 = wiki.locationSitePath(siteName, pathName),
        table = getHistoryTable(siteName,pathName)
    )
    return h

class TRow:
    ix: int # row number, starts from 1
    isNewest: bool # is this the newest file?
    isOldest: bool # is this the oldest file?
    fn: str # filename of .HIST file
    ts2: str #fro timestamp
    size: int # size in disk in bytes


def getHistoryTable(siteName: str, pathName: str) -> str:
    dirName = wiki.getDirPan(siteName, pathName)
    baseDir, stub = os.path.split(dirName)
    dpr("baseDir=%r stub=%r",
        baseDir, stub)
    normalisedName = wiki.normArticleName(stub)
    dpr("normalisedName=%r", normalisedName)
    histDir = butil.join(baseDir, ".HIST")

    filenames, _ = butil.getFilesDirs(histDir)
    dpr("filenames=%r", filenames)
    fns = sorted(fn for fn in filenames
                 if fn.startswith(normalisedName + ".")
                    and fn.endswith(".md")
    )[::-1]
    dpr("fns=%r", fns)


    h = """<table class='report_table'>
<tr> 
    <th>Compare versions</th>
    <th>Timestamp</th>
    <th>Size</th>
    <th>Delta</th>
</tr>    
"""

    #>>>> make data structure for table
    rows = []
    ix = 0
    for fn in fns:
        row = TRow()
        row.ix = ix
        row.isNewest = (ix<=0)
        row.isOldest = (ix>=len(fns)-1)
        row.fn = fn
        normName, ts, ext = fn.split(".")
        ts2 = "%s-%s-%s %s:%s:%s" % (ts[:4], ts[4:6], ts[6:8],
            ts[9:11], ts[11:13], ts[13:15])
        row.ts2 = ts2
        row.size = os.stat(butil.join(histDir, fn)).st_size
        rows.append(row)
        ix += 1
    #//for fn


    for row in rows:
        delta = ""
        if not row.isOldest:
            deltaI = row.size - rows[row.ix+1].size
            if deltaI>0:
                delta = "<b style='color:#090'>+%s</b>" % (deltaI,)
            elif deltaI<0:
                delta = "<b style='color:#900'>%s</b>" % (deltaI,)
            else:
                delta = "%s" % (deltaI,)

        
        h += form("""<tr> 
    <td>{curPrev}</td>
    <td><tt>{timestamp}</tt></td>
    <td style='text-align:right'>{size}</td>
    <td style='text-align:right'>{delta}</td>
</tr>""",
            curPrev = getCurPrev(siteName, pathName, row, rows),
            timestamp=htmlEsc(row.ts2),
            size=row.size,
            delta=delta,
        )
    #//for fn


    h += "</table>\n"
    return h

def getCurPrev(siteName: str, pathName: str,
               row: TRow, rows: list[TRow]) -> str:
    cur = "cur"
    if not row.isNewest:
        cur = form("<a href='/{siteName}/histdiff/{pathName}"
            "?old={oldhfn}"
            "&new={newhfn}'>cur</a>",
            siteName = siteName,
            pathName = pathName,
            oldhfn = row.fn,
            newhfn = rows[0].fn)

    prev = "prev"
    if not row.isOldest:
        prev = form("<a href='/{siteName}/histdiff/{pathName}"
            "?old={oldhfn}"
            "&new={newhfn}'>prev</a>",
            siteName = siteName,
            pathName = pathName,
            oldhfn = rows[row.ix+1].fn,
            newhfn = row.fn)

    h = form("({cur} | {prev})"
             " <input type=radio name=diffFrom value='{fn}'>"
             " <input type=radio name=diffTo value='{fn}'>",
             cur = cur,
             prev = prev,
             fn = htmlEsc(row.fn))
    return h


#---------------------------------------------------------------------

@app.route("/<siteName>/histdiff/<path:pathName>")
def histdiff(siteName, pathName):
    tem = jinjaEnv.get_template("histdiff.html")
    oldhfn = request.args.get("old")
    newhfn = request.args.get("new")

    #>>>>> load old/new files (as lists of strings)
    oldData = (edit.readHist(siteName, pathName, oldhfn)
        .rstrip()
        .splitlines())
    newData = (edit.readHist(siteName, pathName, newhfn)
        .rstrip()
        .splitlines())

    #>>>>> create diff table
    differ = difflib.HtmlDiff(wrapcolumn=70)
    diffTableH = differ.make_table(
        fromlines = oldData,
        tolines = newData,
        fromdesc = htmlEsc(oldhfn),
        todesc = htmlEsc(newhfn),
        context = True,
        numlines = 5)

    h = tem.render(
        title = pathName,
        siteName = siteName,
        pathName = pathName,
        nav2 = wiki.locationSitePath(siteName, pathName),
        oldhfn = htmlEsc(oldhfn),
        newhfn = htmlEsc(newhfn),
        diffTable = diffTableH,
    )
    return h



#---------------------------------------------------------------------

#end

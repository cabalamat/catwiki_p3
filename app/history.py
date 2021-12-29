# history.py

import os.path, datetime, time

from flask import request, redirect, Response

import git

from ulib import butil
from ulib.butil import form, dpr, dpvars

import allpages
from allpages import *

import wiki

#---------------------------------------------------------------------

def getRepo(siteName: str, pathName: str) -> git.Repo:
    """
    siteName = the name of the wiki within catWiki
    pathName = the path to the page within the wiki
    @return = a git repository
    """
    dp = wiki.getDirPan(siteName, "")
    dpvars("dp")
    repo = git.Repo(dp)
    dpvars("dp repo")
    return repo

def commitChanges(siteName: str, pathName: str):
    """ Commit changes to a repository, when (pathname) has
    changed.
    """
    return
    repo = getRepo(siteName, pathName)
    fileName = pathName + ".md"
    dpvars("siteName, pathName fileName")
    repo.index.add([fileName])
    try:
        repo.git.commit(all=True, message="committed "+pathName)
    except:
        pass
    


#---------------------------------------------------------------------

@app.route("/<siteName>/history/<path:pathName>")
def history(siteName, pathName):
    dpr("siteName=%r pathName=%r", siteName, pathName)
    tem = jinjaEnv.get_template("history.html")
    
    repo = getRepo(siteName, pathName)
    #lsf = repo.git.log(form("--follow {}.md", pathName))
    commits = list(repo.iter_commits(paths=pathName+".md"))
    dpvars("commits")
    
    h = tem.render(
        title = pathName,
        siteName = siteName,
        pathName = pathName,
        nav2 = wiki.locationSitePath(siteName, pathName),
        table = getCommitsTable(pathName, commits)
    )
    return h

def getCommitsTable(pathName, commits):
    """
    @param commits::[git.Commit]
    @return::str containing html
    """
    h = """<table class='report_table'>
<tr> 
    <th>Date</th>
    <th>Author</th>
    <th>Message</th>
    <th>Size</th>
    <th>Hex SHA</th>
</tr>    
"""
    for co in commits:
        path = pathName+".md"
        
        fileData = (co.tree / path).data_stream.read()
        coTree = co.tree
        #dpvars("fileData coTree")
        
        
        h += form("""<tr> 
    <td><tt>{date}</tt></td>
    <td>{author}</td>
    <td>{message}</td>
    <td>{size}</td>
    <td><tt>{hexsha}</tt></td>
</tr>""",
            date=niceTime(co.authored_date),
            author=co.author.name,
            message=htmlEsc(co.message),
            size=len(fileData),
            hexsha=co.hexsha,
        )    
    #//for co
    h += "</table>\n"
    return h
    
def niceTime(t):
    """ Converts a time in seconds since epoch to a nice string """
    nt = time.strftime("%Y-%b-%d %H:%M",
        time.gmtime(t))
    return htmlEsc(nt)

#---------------------------------------------------------------------


#end

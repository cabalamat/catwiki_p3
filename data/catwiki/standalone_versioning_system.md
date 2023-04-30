# Standalone versioning system

[TOC]

This is a design for a standalone versioning system for Catwiki.

Consider where we have a wiki page `fred` in folder `foo`. This will be stored as `fred.md` in directory `foo`. The user edits this file. the file `foo/fred.md` is changed. This is how Catwiki currently works
(as of April 2023; in fact it has always worked this way).

The change is that on altering a new file is created in `foo/.HIST/`, where `.HIST` contains historical versions of files in `foo/`.
The filename will include the date stamp of when the change was made, of the form:

    {pageName}.{yyyymmdd}_{HHMMSS}.md

So e.g. `foo/.HIST/fred.20230131_160534.md` would mean it was created on 2023-Jan-31 at 16:05:34.

There will thus be one entry in .HIST for each version of each wiki page.

## The <i class='fa fa-history'></i> History button

This shows a list of all versions of the page.

## The diff URL

This is of the form:

    /{wiki}/histdiff/{wikidir}?old={oldhfn}&new={newhfn}

where:

* {wiki} is the wiki e.g. "catwiki"
* {wikidir} is the path in the URL to the directory the file sits in e.g. "development"
* {oldhfn} for "old history filename" is the filename within .HIST for the older of the files we're comparing
* {newhfn} for "new history filename" is the filename within .HIST for the newer of the files we're comparing

E.g. for this page a URL might look like:

    /catwiki/histdiff/standalone_versioning_system?old=standalone_versioning_system.20230429_004130.md&new=standalone_versioning_system.20230430_020517.md

[url](/catwiki/histdiff/standalone_versioning_system?old=standalone_versioning_system.20230429_004130.md&new=standalone_versioning_system.20230430_020517.md)

xxx



 

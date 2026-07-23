# Development documentation for CatWiki

See also:

* [To-do list](todo)
* [[long term development plan]]

[TOC]


## Data directories

These are:

* under `./data/` for CatWiki's internal wiki, where `./` means the top application directory.
* under `~/siteboxdata/sites/` for all wikis that aren't themselves part of the CatWiki project.

## URLs

* `/{site}/w/{path}` = view a wiki page or directory
* `/{site}/wikiedit/{path}` = view a wiki page or directory
* `/_allSites` = list all sites on this CatWiki installation
* `/{site}/info` = information about a site

Where:

* `{site}`
* `{path}`
* `{oldfn}`
* `{newfn}`

### URLs for history

* `/{site}/history/{path}` = view a list of versions of a page
* `/{site}/histdiff/{path}?old={oldfn}&new={newfn}` = view a list of versions of a page




## Wiki conventions

In any site or site subdirectory, `home` is the home page of that site/directory. (So the filename would be `home.md`).

In any directory, `contents` (file `contents.md`) lists the pages (and subdirectories) of that directory in order. This is used when making a printed book (or ebook, etc). 

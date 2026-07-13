# Standalone versioning system

This is a design for a standalone versioning system for Catwiki.

Consider where we have a wiki page `fred` in folder `foo`. This will be stored as `fred.md` in directory `foo`. The user edits this file. the file `foo/fred.md` is changed. This is ow Catwiki currently works
(as of April 2023; in fact it has always worked this way).

The change is that on altering a new file is created in `foo/.HIST/`, where `.HIST` contains historical versions of files in `foo/`.
The filename will include the date stamp of when the change was made, of the form:

    {pageName}.{yyyymmdd}_{HHMMSS}.md

So e.g. `foo/.HIST/fred.20230131_160534.md` would mean it was created on 2023-Jan-31 at 16:05:34.

There will thus be one entry in .HIST for each version of each wiki page.

## The History button

 

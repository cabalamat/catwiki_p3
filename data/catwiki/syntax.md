# Markdown syntax

*This page describes the version of markdown syntax used by Sitebox. See also [[extensions]].*

Below is a table of contents. It can be produced using the markup `[TOC]`.

[TOC]

## Images

Inline-style: 

    ![alt text](url/goes/here.png "The Title")

## Source code

Text with `tt` some computer `code` in it.

Python source code:

```python 
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
```

## Tables

Here is a table:

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell

And here's another:

| Function name | Description                    |
| ------------- | ------------------------------ |
| `help()`      | Display the help window.       |
| `destroy()`   | **Destroy your computer!**     |

## Markup within a paragraph

This includes *italic*, **bold**, and `monospaced` text. 
# About CatWiki 


<span style="float:right">![Catwiki colour icon](data/catwiki/cw_icon_b.png)</span>


**CatWiki** (aka Catwiki) is very simple wiki software that stores its articles as text files.

Catwiki was originally written for Python 2.8. This version (`catwiki_p3`) is Catwiki for 
Python 3.5 and later.

## Features

* Stores articles as text files, so they are easy to back up and manipulate. Even if the wiki software goes down, you can still get at your notes.
* Uses an enhanced version of the the Markdown markup language. 
* If your wiki pages contain source code, it is highlighted using [Pygments](https://pygments.org/).
* Allows multiple wikis per installation, each one in its own directory.
* Allows subdirectories. You can navigate through the directories using the web interface. If the directory includes image files, the web page shows thumbnails of them.
* You can add Font Awesome icons (both 4.7 and 5.15) in your wiki pages.

## Technology Used

CatWiki is written in Python and uses the Flask lightweight web framework.

## Screenshots

Here are some screenshots of CatWiki in action.

### An article

Here is an article in CatWiki:

![](data/catwiki/article.png)

### The article editor

Here is the same article in CatWiki's text editor:

![](data/catwiki/article_editor.png)

### Folder view

This shows all the articles, other files, and sub-folders in a folder.

![](data/catwiki/folder_view.png)


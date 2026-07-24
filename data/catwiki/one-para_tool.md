# One-Para tool

The One-Para tool appears on the [[Editing toolbar]] as:

> <i class='fa fa-paragraph'></i> 1-Para

Like most of the tools it operates on whatever text is selected before the tool is run (by clicking on it).

Its function is to replace the selected text with a single paragraph containing all the selected text but will all consecutive whitespace (i.e. spaces, tabs and newlines) characters replaced by a single space. Any whitespace at the start or end of the selection is also removed.

## Example

If in the editor you selected this source text, which is sped over multiple lines:

```
This 
 is   some 
 text

here
```

It would be changed to:

```
This is some text here
```

## Motivation

When cutting and pasting text from pdfs, it often appears similar to the example, with each word on a single line.

E.g. from <https://files.gotocon.com/uploads/files/138/d7-formatted_1778445542.pdf>, page 16:

```
1.
 
Emergency
 
supply
 
diversification
 
-
 
alternative
sources for withheld goods.
```

One-Para cleans this up as:

```
1. Emergency supply diversification - alternative sources for withheld goods.
```




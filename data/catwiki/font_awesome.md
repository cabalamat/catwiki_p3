# <i class='fa fa-font-awesome'></i> Font Awesome

CatWiki allows you to use Font Awesome icons in your wiki pages. In particular it comes with all the free icons from Font Awesome 4.7 and Font Awesome 5.15.4 built in.

[TOC]

## How to use a Font Awesome 4 icon

Imagine you want to use the Font Awesome 4.7 icon for a pencil. This has the identifier `fa-pencil`,
and looks like this: <i class='fa fa-pencil'></i>. To put it inside your document use the HTML code:

```html
<i class='fa fa-pencil'></i>
```

As you can see Font Awesome 4.7 icons are implemented as 2 CSS classes (`fa` and `fa-pencil`) inside an HTML `<i>` tag.

## How to use a Font Awesome 5 icon

Font Awesome 5 works similar to 4.7, except that the first CSS class isn't `fa`, instead it is one of `fas` (for solid), `far` (regular)
or `fab` (brands). Some examples:

* <i class='fas fa-user'></i> (code: `<i class='fas fa-user'></i>`) uses the solid style 
* <i class='far fa-user'></i> (code: `<i class='far fa-user'></i>`) uses the regular style
* <i class='fab fa-github'></i> (code: `<i class='fab fa-github'></i>`) uses the brands style 

Often you get both solid and regular versions of the same icon. For example, the Address Book icon (`fa-address-book`) has 
solid: <i class='fas fa-address-book'></i> (`fas`)
and regular: <i class='far fa-address-book'></i> (`far`) varients.

## Font Awesome icons are implemented as web fonts

Because Font Awesome icons are implemented as fonts, they can use different colours and font sizes, just like normal characters. 

For example, if you put this in your wiki source:

```html
<span style='color:#ff0; background:#900; font-size:20px; padding:2px'><i class='fas fa-exclamation-triangle'></i> don't press the self-destruct button.</span>
```

It looks like this:

<span style='color:#ff0; background:#900; font-size:20px; padding:2px'><i class='fas fa-exclamation-triangle'></i> don't press the self-destruct button.</span>


## See also

* [Font Awesome](https://fontawesome.com/) homepage
* List of [Font Awesome 5.15 free icons](https://fontawesome.com/v5.15/icons?d=gallery&p=2&m=free) and [usage](https://fontawesome.com/v5.15/how-to-use/on-the-web/referencing-icons/basic-use) instructions
* List of [Font Awesome 4.7.0 icons](https://fontawesome.com/v4.7/icons/) and [examples of usage](https://fontawesome.com/v4.7/examples/)
* [Font-Awesome](https://github.com/FortAwesome/Font-Awesome) on <i class='fa fa-github'></i> Github

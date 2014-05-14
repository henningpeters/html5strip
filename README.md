html5strip
==========

Strip empty leading and trailing tags from HTML fragments

### Some examples

html5strip removes unused ```<br>``` tags:

```<div><br>Hello, world!<br></div>``` => ```<div>Hello, world!</div>```

Likewise, it can handle other empty tags, too:

```<div><p> </p>Hello, world!<p> </p></div>``` => ```<div>Hello, world!</div>```

While preserving any "inside" tags:

```<div>Hello,<br>world!<div>``` => ```<div>Hello,<br>world!</div>```

Simply put in any HTML fragment:

```<p></p>Hello, world!``` => ```Hello, world!```

Or arbitrarily complex empty tag structures:

```<div><div><div><br><p> </p></div></div>Hello, world!</div>``` => ```<div>Hello, world!</div>```

html5strip is based on html5lib and hence repairs even broken HTML:

```<div>Hello, world!<br>``` => ```<div>Hello, world!</div>```

Or just use it to strip whitespace from text:

``` Hello, world! ``` => ```Hello, world!```

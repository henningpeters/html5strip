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

Simply put in any (X)HTML fragment:

```<p></p>Hello, world!``` => ```Hello, world!```

Or arbitrarily complex empty tag structures:

```<div><div><div><br><p> </p></div></div>Hello, world!</div>``` => ```<div>Hello, world!</div>```

html5strip is based on lxml and html5lib and hence repairs even broken HTML:

```<div>Hello, world!<br>``` => ```<div>Hello, world!</div>```

### Dependencies

```
pip install lxml html5lib
```

### Usage

```
from html5strip import HTML5Strip
HTML5Strip.strip("<div><br>Hello, world!<br></div>")  # <div>Hello, world!</div>
```

### Limitations

html5strip is not aware of any tag semantics, it only looks at whether a tag contains text or not. Hence, images, forms, SVGs, scripts and many other elements that might contain some content, but no text, might be stripped.

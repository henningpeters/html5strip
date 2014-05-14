# -*- coding: utf-8 -*-
import warnings

from lxml.html import html5parser, tostring


class HTML5Fragment(object):

    def __init__(self, root):
        self.root = root
        self.blacklist = self.get_blacklist()

    @classmethod
    def has_text(cls, text):
        return bool(text) and not text.isspace()

    @classmethod
    def discard_ancestors(cls, root, blacklist):
        for e in root.iterancestors():
            blacklist.discard(e)

    @classmethod
    def discard_children(cls, root, blacklist, until_element=None):
        for e in root.iterchildren():
            if until_element == e:
                break
            blacklist.discard(e)

    @classmethod
    def is_root(cls, element):
        root = element.getroottree().getroot()
        return element.getparent() == root

    def traverse_left(self, root, blacklist):
        if self.l:
            blacklist.discard(root)

        if HTML5Fragment.has_text(root.text or root.tail):
            self.l = True
            self.last = root
            self.empty = False

        if HTML5Fragment.has_text(root.text):
            blacklist.discard(root)
            self.discard_ancestors(root, blacklist)
            blacklist.difference(set(root.iter()))

        elif HTML5Fragment.has_text(root.tail):
            self.discard_ancestors(root, blacklist)
            blacklist.difference(set(root.iter()))

        for e in root.iterchildren():
            self.traverse_left(e, blacklist)

    def traverse_right(self, root, blacklist):
        if self.r:
            blacklist.discard(root)

        if root == self.last:
            if HTML5Fragment.has_text(self.last.tail):
                self.discard_children(root, blacklist)
            self.r = False

        for e in root.iterchildren():
            self.traverse_right(e, blacklist)

    def get_blacklist(self):
        self.empty = True

        # root can be a string
        if isinstance(self.root, basestring):
            return set()

        self.l = False
        self.r = True
        self.last = None

        blacklist_l = set(self.root.iter())
        blacklist_r = set(self.root.iter())

        self.traverse_left(self.root, blacklist_l)
        self.traverse_right(self.root, blacklist_r)

        return blacklist_l.union(blacklist_r)

    def strip(self, blacklist=None):
        # root can be a string
        if isinstance(self.root, basestring):
            return self.root

        # remove blacklisted tags
        remove = False

        if blacklist is None:
            blacklist = self.blacklist

        res = ""
        for e in blacklist:
            p = e.getparent()
            remove = HTML5Fragment.is_root(e)  # remove root?
            if e.tail:
                prev = e.getprevious()
                if remove:
                    res += e.tail
                elif prev is not None:
                    prev.tail = (prev.tail or "") + e.tail
                else:
                    p.text = (p.text or "") + e.tail
                e.tail = None

            p.remove(e)

        # skip if blacklisted tag is root
        return res if remove else tostring(self.root, encoding="unicode")

    def tostring(self):
        if isinstance(self.root, basestring):
            return self.root
        return tostring(self.root, encoding="unicode")


class HTML5Strip(object):

    @classmethod
    def parse(self, markup):
        parser = html5parser.HTMLParser(namespaceHTMLElements=False)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return html5parser.fragments_fromstring(markup,
                                                    guess_charset=False,
                                                    parser=parser)

    @classmethod
    def strip(self, markup):
        roots = self.parse(markup)
        fragments = [HTML5Fragment(r) for r in roots]

        tmp = [f for f in fragments if not f.empty]
        l = tmp and tmp[0]
        r = tmp and tmp[-1]

        blacklist = None
        res = ""
        for fragment in fragments:
            if fragment == r:
                blacklist = None

            res += fragment.strip(blacklist)

            if fragment == l and l != r:
                blacklist = set()

        return res.strip()

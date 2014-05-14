# -*- coding: utf-8 -*-
import unittest

from html5strip import HTML5Strip, HTML5Fragment


class TestHTML5Strip(unittest.TestCase):

    def test_parse(self):
        roots = HTML5Strip.parse("<p>hello, world</p>")
        self.assertEqual(roots[0].text, "hello, world")

    def test_parse_fragments(self):
        roots = HTML5Strip.parse("<p>hello</p><p>world</p>")
        self.assertEqual([r.text for r in roots], ["hello", "world"])

    def test_strip_root(self):
        fragment = HTML5Fragment(HTML5Strip.parse("<p>hello, world</p>")[0])
        res = fragment.strip(set([fragment.root]))
        self.assertEqual(res, "")

    def test_strip_element(self):
        fragment = HTML5Fragment(HTML5Strip.parse("<p>hello, world<br></p>")[0])
        res = fragment.strip(set(fragment.root.findall("br")))
        self.assertEqual(res, "<p>hello, world</p>")

    def test_strip_string(self):
        res = HTML5Fragment("hello, world").strip()
        self.assertEqual(res, "hello, world")

    def test_strip_tail(self):
        fragment = HTML5Fragment(HTML5Strip.parse("<p>hello,<br>world</p>")[0])
        res = fragment.strip(set(fragment.root.findall("br")))
        self.assertEqual(res, "<p>hello,world</p>")

    def test_has_text(self):
        self.assertTrue(HTML5Fragment.has_text("hello, world"))
        self.assertTrue(HTML5Fragment.has_text(u"金魚"))
        self.assertFalse(HTML5Fragment.has_text(u"\u2000"))  # some unicode space
        self.assertFalse(HTML5Fragment.has_text(" "))

    def test_has_text_on_html(self):
        roots = HTML5Strip.parse(u"<p>hello, world</p>")
        self.assertTrue(HTML5Fragment.has_text(roots[0].text))

    def test_has_no_text_on_html(self):
        roots = HTML5Strip.parse(u"<p>\u2000</p>")
        self.assertFalse(HTML5Fragment.has_text(roots[0].text))

    def test_get_blacklist(self):
        roots = HTML5Strip.parse("<p>hello, world<br></p>")
        fragment = HTML5Fragment(roots[0])
        self.assertEqual(fragment.blacklist, set(roots[0].findall("br")))

    def test_get_blacklist_on_string(self):
        blacklist = HTML5Fragment("hello, world").get_blacklist()
        self.assertEqual(blacklist, set())

    def test_clean(self):
        self.assertEqual(HTML5Strip.strip("<a> X <b><c></c> X </b></a>"), "<a> X <b><c></c> X </b></a>")
        self.assertEqual(HTML5Strip.strip("<a> X <b><c></c></b> X </a>"), "<a> X <b><c></c></b> X </a>")
        self.assertEqual(HTML5Strip.strip("<a><b><c></c></b> X </a>"), "<a> X </a>")
        self.assertEqual(HTML5Strip.strip("<a> X <b><c></c></b></a>"), "<a> X </a>")

        self.assertEqual(HTML5Strip.strip("<div> X <div> X <div></div></div></div>"), "<div> X <div> X </div></div>")
        self.assertEqual(HTML5Strip.strip(" <p>hello, world</p> "), "<p>hello, world</p>")
        self.assertEqual(HTML5Strip.strip("<p>hello, world<br></p>"), "<p>hello, world</p>")
        self.assertEqual(HTML5Strip.strip("<br><p>hello, world</p><br>"), "<p>hello, world</p>")

        self.assertEqual(HTML5Strip.strip("<a><b><c><d></d></c> X </b></a>"), "<a><b> X </b></a>")
        self.assertEqual(HTML5Strip.strip("<a> <b> X </b> </a>"), "<a> <b> X </b> </a>")
        self.assertEqual(HTML5Strip.strip("<a> <b> <c> <d> <e>X</e> </d> </c> </b> </a>"), "<a> <b> <c> <d> <e>X</e> </d> </c> </b> </a>")
        self.assertEqual(HTML5Strip.strip("<a> <x></x> <b> X </b> </a>"), "<a>  <b> X </b> </a>") # preserve spaces
        self.assertEqual(HTML5Strip.strip("<a> </a> <b> </b> <c> X </c> <b> </b> <a> </a>"), "<c> X </c>")
        self.assertEqual(HTML5Strip.strip("<a> </a> <b> </b> <c> </c> <b> </b> </a>"), "")

        self.assertEqual(HTML5Strip.strip("<p>a<br><br>b</p>"), "<p>a<br><br>b</p>")
        self.assertEqual(HTML5Strip.strip("<p><br><br>b</p>"), "<p>b</p>")
        self.assertEqual(HTML5Strip.strip("<p>b<br><br></p>"), "<p>b</p>")

        self.assertEqual(HTML5Strip.strip("<a><b> x </b><br><br> c </a>"), "<a><b> x </b><br><br> c </a>")
        self.assertEqual(HTML5Strip.strip("<a><br><br><b> x </b><br><br> c </a>"), "<a><b> x </b><br><br> c </a>")
        self.assertEqual(HTML5Strip.strip("<a> a <br><br><b> x </b></a>"), "<a> a <br><br><b> x </b></a>")

        self.assertEqual(HTML5Strip.strip("<a></a>x"), "x")
        self.assertEqual(HTML5Strip.strip("x<a></a>"), "x")
        self.assertEqual(HTML5Strip.strip("x<a></a>y"), "xy")

        self.assertEqual(HTML5Strip.strip("<p>a</p> <p></p> <p></p> <p>a<br></p>"), "<p>a</p> <p></p> <p></p> <p>a</p>")
        self.assertEqual(HTML5Strip.strip("<p></p> <p><br>a</p> <p></p> <p>a<br></p> <p></p>"), "<p>a</p> <p></p> <p>a</p>")
        self.assertEqual(HTML5Strip.strip("<p></p> <p><br>a</p> <p><br>a</p> <p></p> <p>a</p>"), "<p>a</p> <p><br>a</p> <p></p> <p>a</p>")
        self.assertEqual(HTML5Strip.strip("<p></p> <p>a</p> <p></p> <p>a<br></p> <p>a<br></p>"), "<p>a</p> <p></p> <p>a<br></p> <p>a</p>")

 
if __name__ == '__main__':
    unittest.main()

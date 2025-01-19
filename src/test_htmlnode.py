import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HtmlNode("a", "This is link", [], {"href": "https://www.google.com"})
        testinput = node.props_to_html()
        expected_output = ' href="https://www.google.com"'
        self.assertEqual(testinput, expected_output)

    def test_props_to_html2(self):
        node = HtmlNode("a", "This is link", [], {"href": "https://www.google.com", "target": "_blank", "class": "button"})
        testinput = node.props_to_html()
        expected_output = ' href="https://www.google.com" target="_blank" class="button"'
        self.assertEqual(testinput, expected_output)

    def test_props_to_html3(self):
        node = HtmlNode("a", "This is link",)
        testinput = node.props_to_html()
        expected_output = ""
        self.assertEqual(testinput, expected_output)

    def test_repr(self):
        node = HtmlNode(tag="a", value="This is link", children=[], props={"href": "https://www.google.com"})
        expected_output = "a, This is link, [], {'href': 'https://www.google.com'}"
        self.assertEqual(repr(node), expected_output)

#### LeafNode tests:

    def test_leaf_to_html(self):
        node = LeafNode("a", "This is link", {"href": "https://www.google.com"})
        testinput = node.to_html()
        expected_output = '<a href="https://www.google.com">This is link</a>'
        self.assertEqual(testinput, expected_output)

    def test_leaf_to_html2(self):
        node = LeafNode("a", "This is link", {"href": "https://www.google.com", "target": "_blank", "class": "button"})
        testinput = node.to_html()
        expected_output = '<a href="https://www.google.com" target="_blank" class="button">This is link</a>'
        self.assertEqual(testinput, expected_output)

    def test_leaf_to_html3(self):
        node = LeafNode("p", "This is text")
        testinput = node.to_html()
        expected_output = "<p>This is text</p>"
        self.assertEqual(testinput, expected_output)

    def test_leaf_invalid_props(self):
        node = LeafNode("p", "This is text", "randomtext")
        testinput = node.to_html()
        expected_output = '<p>This is text</p>'
        self.assertEqual(testinput, expected_output)

    def test_leaf_value_error(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)

#### ParentNode tests:

    def test_parent_to_html(self):
        node = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "Italic text"),
                    LeafNode(None, "Normal text"),
                ]
            )
        testinput = node.to_html()
        expected_output = '<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p>'
        self.assertEqual(testinput, expected_output)

    def test_nested_parents_to_html(self):
        node = ParentNode(
                "tr",
                [
                ParentNode(
                    "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "Italic text"),
                    LeafNode(None, "Normal text"),
                ]
                
                )
                ]
            )
        testinput = node.to_html()
        expected_output = '<tr><p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p></tr>'
        self.assertEqual(testinput, expected_output)

    def test_nochildren_value_error(self):
        with self.assertRaises(ValueError):
            ParentNode("p", [])

if __name__ == "__main__":
    unittest.main()

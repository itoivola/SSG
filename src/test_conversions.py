import unittest

from conversions import text_node_to_html_node
from textnode import TextNode, TextType
from htmlnode import LeafNode


class TestConversionNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        result = text_node_to_html_node(node)
        expected = LeafNode(None, "This is a text node")
        self.assertEqual(result, expected)

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        result = text_node_to_html_node(node)
        expected = LeafNode("b", "This is a text node")
        self.assertEqual(result, expected)

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, url="www.google.com")
        result = text_node_to_html_node(node)
        expected = LeafNode("a", "This is a text node", {"href": "www.google.com"})
        self.assertEqual(result, expected)

    def test_img(self):
        node = TextNode("This is a text node", TextType.IMAGE, url="www.google.com")
        result = text_node_to_html_node(node)
        expected = LeafNode("img", " ", {"src": "www.google.com", "alt": "This is a text node"})
        self.assertEqual(result, expected)

    def test_wrong_text_type(self):
        with self.assertRaises(Exception):
            node = TextNode("This is a text", "bold")
            result = text_node_to_html_node(node)



if __name__ == "__main__":
    unittest.main()

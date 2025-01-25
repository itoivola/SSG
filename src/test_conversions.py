import unittest

from conversions import extract_markdown_images, extract_markdown_links, text_node_to_html_node, split_nodes_delimiter
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


class TestSplitNodes(unittest.TestCase):
    def test1(self):
        nodes = [
            TextNode("This is text with a `code block` word", TextType.NORMAL),
            TextNode("Test2", TextType.NORMAL)
            ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.NORMAL, None),
            TextNode("code block", TextType.CODE, None),
            TextNode(" word", TextType.NORMAL, None),
            TextNode("Test2", TextType.NORMAL, None)
            ]
        self.assertEqual(result, expected)

    def test2(self):
        nodes = [
            TextNode("This is `code` and a `code block` word", TextType.NORMAL),
            TextNode("`code` at start", TextType.NORMAL),
            TextNode("ending with `code`", TextType.NORMAL)
            ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("This is ", TextType.NORMAL, None),
            TextNode("code", TextType.CODE, None),
            TextNode(" and a ", TextType.NORMAL, None),
            TextNode("code block", TextType.CODE, None),
            TextNode(" word", TextType.NORMAL, None),
            TextNode("code", TextType.CODE, None),
            TextNode(" at start", TextType.NORMAL, None),
            TextNode("ending with ", TextType.NORMAL, None),
            TextNode("code", TextType.CODE, None)
            ]
        self.assertEqual(result, expected)

    def test3(self):
        nodes = [
            TextNode("This is text with a *bold* word", TextType.NORMAL),
            TextNode("This is text with *double* *bold* word", TextType.NORMAL)
            ]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.NORMAL, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode(" word", TextType.NORMAL, None),
            TextNode("This is text with ", TextType.NORMAL, None),
            TextNode("double", TextType.BOLD, None),
            TextNode(" ", TextType.NORMAL, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode(" word", TextType.NORMAL, None),
            ]
        self.assertEqual(result, expected)

    def test4(self):
        nodes = [
            TextNode("This is text with a *bold* word", TextType.NORMAL),
            TextNode("This is text with *double**bold* word", TextType.NORMAL)
            ]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.NORMAL, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode(" word", TextType.NORMAL, None),
            TextNode("This is text with ", TextType.NORMAL, None),
            TextNode("double", TextType.BOLD, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode(" word", TextType.NORMAL, None),
            ]
        self.assertEqual(result, expected)

    def test5(self):
        nodes = [
            TextNode("This is text with a `code block` word", TextType.CODE)
            ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("This is text with a `code block` word", TextType.CODE)
            ]
        self.assertEqual(result, expected)

# Test regex images and links
class TestRegexImgLinks(unittest.TestCase):
    def test_img(self):
        imgtext = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(imgtext)
        expected = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        self.assertEqual(result, expected)

    def test_link(self):
        linktext = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(linktext)
        expected = [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')]
        self.assertEqual(result, expected)

    def test_empty_string(self):
        linktext = ""
        result = extract_markdown_links(linktext)
        expected = []
        self.assertEqual(result, expected)

    def test_wrong_format(self):
        linktext = []
        result = extract_markdown_links(linktext)
        expected = []
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()

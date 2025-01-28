import unittest

from conversions import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_node_to_html_node, split_nodes_delimiter, text_to_textnodes
from textnode import TextNode, TextType
from htmlnode import LeafNode
from blocks import markdown_to_blocks



class TestTextToBlock(unittest.TestCase):
    def test_text(self):
        text = """
   Test test test
   asdsadsad
   sadsadsad

   * asdfasfsaf
   * safsafsaf

   asflksafjsaf
   jskalfjalkfs
   alskfjlsakf
                   """

        result = markdown_to_blocks(text)
        expected = [
                'Test test test\nasdsadsad\nsadsadsad',
                '* asdfasfsaf\n* safsafsaf',
                'asflksafjsaf\njskalfjalkfs\nalskfjlsakf'
            ]
        self.assertEqual(result, expected)


class TestTextToBlock2(unittest.TestCase):
    def test_text(self):
        text = """


                   Test test test
                   asdsadsad
                   sadsadsad


                   * asdfasfsaf
                   * safsafsaf

                   asflksafjsaf
                   jskalfjalkfs
                   alskfjlsakf


                   """
        result = markdown_to_blocks(text)
        expected = [
                'Test test test\nasdsadsad\nsadsadsad',
                '* asdfasfsaf\n* safsafsaf',
                'asflksafjsaf\njskalfjalkfs\nalskfjlsakf'
            ]
        self.assertEqual(result, expected)

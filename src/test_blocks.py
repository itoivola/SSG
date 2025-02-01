import unittest

from blocks import markdown_to_blocks, block_to_block_type



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

class BlockToBlockType(unittest.TestCase):
    def test_code(self):
        text = """```1. TEST1
2. TEST2
3. TEST3
5. TEST5```"""

        result = block_to_block_type(text)
        expected = "code"
        self.assertEqual(result, expected)

    def test_quote(self):
        text = """>1. TEST1
>2. TEST2
>3. TEST3
>5. TEST5"""

        result = block_to_block_type(text)
        expected = "quote"
        self.assertEqual(result, expected)

    def test_ul(self):
        text = """* TEST1
* TEST2
* TEST3
* TEST5"""

        result = block_to_block_type(text)
        expected = "unordered list"
        self.assertEqual(result, expected)

    def test_ol(self):
        text = """1. TEST1
2. TEST2
3. TEST3
4. TEST5"""

        result = block_to_block_type(text)
        expected = "ordered list"
        self.assertEqual(result, expected)

print(block_to_block_type("""```1. TEST1
2. TEST2
3. TEST3
5. TEST5```"""))


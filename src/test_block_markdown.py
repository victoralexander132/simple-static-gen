import unittest
from textnode import BlockType
from block_markdown import block_to_block_type

class TestBlockMarkdown(unittest.TestCase):
    def test_heading_h1(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_h6(self):
        block = "###### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_heading_with_multiple_words(self):
        block = "## This is a longer heading with many words"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_not_heading_no_space(self):
        block = "#No space after hash"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_not_heading_too_many_hashes(self):
        block = "####### Too many hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_code_block(self):
        block = "```\ncode here\nmore code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_code_block_multiline(self):
        block = "```\ndef hello():\n    print('world')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_not_code_block_missing_end(self):
        block = "```\ncode here"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_quote_single_line(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_quote_multiline(self):
        block = "> This is a quote\n> with multiple lines\n> all quoted"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_not_quote_missing_marker(self):
        block = "> First line\nSecond line without marker"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_unordered_list_single_item(self):
        block = "- Item one"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_unordered_list_multiple_items(self):
        block = "- Item one\n- Item two\n- Item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_not_unordered_list_missing_marker(self):
        block = "- Item one\nItem two without marker"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_ordered_list_single_item(self):
        block = "1. First item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_ordered_list_multiple_items(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_not_ordered_list_wrong_number(self):
        block = "1. First item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_not_ordered_list_starts_at_zero(self):
        block = "0. First item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_not_ordered_list_starts_at_two(self):
        block = "2. Second item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_paragraph_plain_text(self):
        block = "This is just a normal paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_paragraph_multiline(self):
        block = "This is a paragraph\nwith multiple lines\nbut no special markers"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
import unittest
from textnode import BlockType
from block_markdown import block_to_block_type, markdown_to_html_node, extract_title

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

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph text in a p tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """
# This is a heading

## This is a smaller heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><h2>This is a smaller heading</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

This is paragraph text
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a\nblockquote block</blockquote><p>This is paragraph text</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_extract_title(self):
        md = "# Hello"
        title = extract_title(md)
        self.assertEqual(title, "Hello")

    def test_extract_title_with_whitespace(self):
        md = "#  Hello World  "
        title = extract_title(md)
        self.assertEqual(title, "Hello World")

    def test_extract_title_with_content(self):
        md = """
# My Title

This is some content
"""
        title = extract_title(md)
        self.assertEqual(title, "My Title")

    def test_extract_title_no_h1(self):
        md = """
## This is h2

This is content
"""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_empty(self):
        md = ""
        with self.assertRaises(Exception):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()
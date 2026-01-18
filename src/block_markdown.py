import re
from textnode import BlockType, TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes, markdown_to_blocks

def block_to_block_type(block):
    # Check for heading (1-6 # characters followed by space)
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING
    
    # Check for code block (starts with ``` and newline, ends with ```)
    if block.startswith('```') and block.endswith('```'):
        lines = block.split('\n')
        if len(lines) >= 3 and lines[0] == '```' and lines[-1] == '```':
            return BlockType.CODE
    
    # Check for quote block (every line starts with "> " or is just ">")
    lines = block.split('\n')
    if all(line.startswith('> ') or line == '>' for line in lines):
        return BlockType.QUOTE
    
    # Check for unordered list (every line starts with "- ")
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list (lines start with "1. ", "2. ", etc.)
    if all(re.match(rf'^{i}\. ', line) for i, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST
    
    # Default to paragraph
    return BlockType.PARAGRAPH


def text_to_children(text):
    """
    Convert text with inline markdown to a list of HTMLNode children.
    This function handles bold, italic, code, links, and images.
    """
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    """Convert a paragraph block to an HTMLNode."""
    lines = block.split("\n")
    paragraph_text = " ".join(lines)
    children = text_to_children(paragraph_text)
    return ParentNode("p", children)


def heading_to_html_node(block):
    """Convert a heading block to an HTMLNode."""
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    
    if level < 1 or level > 6:
        raise ValueError(f"Invalid heading level: {level}")
    
    text = block[level + 1:]  # Skip the # characters and the space
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    """Convert a code block to an HTMLNode."""
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    
    text = block[4:-3]  # Remove ``` from start and end, including newline after first ```
    return ParentNode("pre", [LeafNode("code", text)])


def quote_to_html_node(block):
    """Convert a quote block to an HTMLNode."""
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if line == ">":
            new_lines.append("")
        elif line.startswith("> "):
            new_lines.append(line[2:])
        else:
            raise ValueError("Invalid quote line")
    
    content = "\n".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    """Convert an unordered list block to an HTMLNode."""
    items = []
    lines = block.split("\n")
    for line in lines:
        text = line[2:]  # Remove "- " from each line
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ul", items)


def ordered_list_to_html_node(block):
    """Convert an ordered list block to an HTMLNode."""
    items = []
    lines = block.split("\n")
    for line in lines:
        text = line.split(". ", 1)[1]  # Remove "1. ", "2. ", etc.
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ol", items)


def block_to_html_node(block):
    """Convert a single block to an HTMLNode based on its type."""
    block_type = block_to_block_type(block)
    
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case _:
            raise ValueError(f"Invalid block type: {block_type}")


def markdown_to_html_node(markdown):
    """
    Convert a full markdown document into a single parent HTMLNode.
    The parent HTMLNode contains child HTMLNode objects representing the nested elements.
    """
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    
    return ParentNode("div", children)


def extract_title(markdown):
    """
    Extract the h1 header from a markdown document.
    Returns the title text without the # and any leading/trailing whitespace.
    Raises an exception if no h1 header is found.
    """
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 header found in markdown")
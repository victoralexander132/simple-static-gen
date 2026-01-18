import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    It takes a list of "old nodes", a delimiter, and a text type. It should return a new list of nodes, where any "text" type nodes in the input list are (potentially) split into multiple nodes based on the syntax. For example, given the following input:

    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    new_nodes becomes:

    [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
    ]

    The beauty of this function is that it will take care of inline code, bold, and italic text, all in one! The logic is identical, the delimiter and matching text_type are the only thing that changes, e.g. ** for bold, _ for italic, and a backtick for code. Also, because it operates on an input list, we can call it multiple times to handle different types of delimiters. The order in which you check for different delimiters matters, which actually simplifies implementation.

    I don't want to give you full pseudocode, but here are some pointers:
    If an "old node" is not a TextType.TEXT type, just add it to the new list as-is, we only attempt to split "text" type objects (not bold, italic, etc).
    If a matching closing delimiter is not found, just raise an exception with a helpful error message, that's invalid Markdown syntax.
    The .split() string method was useful
    The .extend() list method was useful
    Write a bunch of tests. Be sure to test various types of delimiters.
    """


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_nodes = []
        sections = old_node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise Exception("Invalid markdown, formatted section not closed")

        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)

    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):

    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        old_text = old_node.text
        images = extract_markdown_images(old_text)

        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for image in images:
            sections = old_text.split(f"![{image[0]}]({image[1]})")
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            old_text = sections[1]

        if old_text != "":
            new_nodes.append(TextNode(old_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        old_text = old_node.text
        links = extract_markdown_links(old_text)

        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        for link in links:
            sections = old_text.split(f"[{link[0]}]({link[1]})")
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            old_text = sections[1]

        if old_text != "":
            new_nodes.append(TextNode(old_text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    """
    It takes a string of text and returns a list of TextNode objects, which is the output of the function.
    Input: This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)
    Output: [
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
    ]
    """
    text = text.strip()
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

#Create a new function called markdown_to_blocks(markdown). It takes a raw Markdown string (representing a full document) as input and returns a list of "block" strings. The example above would be split into these three strings:
#The .split() method can be used to split a string into blocks based on a delimiter (\n\n is a double newline).
#You should .strip() any leading or trailing whitespace from each block.
# Remove any "empty" blocks due to excessive newlines.
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    blocks = [block for block in blocks if block != ""]
    return blocks

import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_default_props(self):
        node = HTMLNode("p", "Hello, world!")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello, world!")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr(self):
        node = HTMLNode("p", "Hello, world!")
        self.assertEqual(
            repr(node),
            "HTMLNode(tag=p, value=Hello, world!, children=None, props=None)",
        )

    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "Click me!",
            None,
            {"href": "XXXXXXXXXXXXXXXXXXXXXX", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="XXXXXXXXXXXXXXXXXXXXXX" target="_blank"',
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p_with_props(self):
        node = LeafNode(
            "a",
            "Click me!",
            {"href": "XXXXXXXXXXXXXXXXXXXXXX", "target": "_blank"},
        )
        self.assertEqual(
            node.to_html(),
            '<a href="XXXXXXXXXXXXXXXXXXXXXX" target="_blank">Click me!</a>',
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()

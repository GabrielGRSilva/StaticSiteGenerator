import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestParentNode(unittest.TestCase):
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
            "<div><span><b>grandchild</b></span></div>",)

    def test_to_html_child_not_equal(self):
        grandchild_node = LeafNode("b", "grandchild")
        parent_node = ParentNode("div", [grandchild_node])
        self.assertNotEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", None)
        self.assertRaises(ValueError, parent_node.to_html)


    def test_to_html_with_no_value(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_multinest(self):
        grandgrandgrandchildren_node = LeafNode("div", "big family")
        grandgrandchildren_node = ParentNode("span", [grandgrandgrandchildren_node])
        grandchildren_node = ParentNode("div", [grandgrandchildren_node])
        child_node = ParentNode("b", [grandchildren_node])
        parent_node = ParentNode("d", [child_node])
        grandpa_node = ParentNode("div", [parent_node])
        self.assertEqual(
            grandpa_node.to_html(),
            "<div><d><b><div><span><div>big family</div></span></div></b></d></div>")


if __name__ == "__main__":
        unittest.main()

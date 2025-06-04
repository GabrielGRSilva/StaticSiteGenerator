import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_no_url(self):
        node = TextNode("This is a no url node", TextType.NORMAL, None)
        node2 = TextNode("This is a url node", TextType.NORMAL, "google.com")
        self.assertNotEqual(node, node2)

    def test_different_url(self):
            node = TextNode("This is a url node", TextType.NORMAL, "google.com")
            node2 = TextNode("This is a url node", TextType.NORMAL, "boot.dev")
            self.assertNotEqual(node, node2)

    def test_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)



if __name__ == "__main__":
    unittest.main()

from htmlnode import *
import unittest
from textnode import *

# Test 1
test_props = {"href": "https://www.google.com", "target": "_blank"}
node = HTMLNode("p", "this is a props test", None, test_props)
node2 = HTMLNode("p", "this is a props test", None, None)
print("Test 1 - props_to_html():", node.props_to_html())

# Test 2
node2 = HTMLNode("b", "this is a node test", None, {"href": "www.google.com"})
print("Test 2 - node:", node2)

# Test 3
node3 = HTMLNode(None, "this is a value")
print("Test 3 - just value:", node3)

# Test 4
node4 = LeafNode("p", "Hello, world!")                #Test Child Class
print("Test 4 - LeafNode:", node4.to_html())

# Test 5
node = TextNode("The bold is on the last word: **here**", TextType.NORMAL)
new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
print ("Test 5 - Nodes Delimiter", new_nodes)

# Test 6
text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
print("Test 6 - Extract Markdown Images:", extract_markdown_images(text))


#UnitTest Tests
class TestNodeToHTMLFunction(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_link(self):
        node = TextNode("Click me!", TextType.LINK)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")

    def test_text_image(self):
        node = TextNode(None, TextType.IMAGE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)

    def test_invalid_text_type(self):
        with self.assertRaises(TypeError):
            node = TextNode("I have no type!", None)
            split_nodes_delimiter(node)

class Test_Split_Nodes_Delimiter_Function(unittest.TestCase):
    def test_standard_input(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.NORMAL),TextNode("code block", TextType.CODE),TextNode(" word", TextType.NORMAL),])

    def test_odd_delimiter_error(self):
        with self.assertRaises(TypeError):
            node = TextNode("This is text with a `code block word", TextType.NORMAL)
            split_nodes_delimiter(node)

    def test_input_delimiter_on_last_string(self):
        node = TextNode("The bold is on the last word: **here**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("The bold is on the last word: ", TextType.NORMAL),TextNode("here", TextType.BOLD), TextNode("", TextType.NORMAL),])

class Test_Extract_Markdown_Images_and_Text_Functions(unittest.TestCase):
    def test_standard_img_input(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])

    def test_standard_text_input(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_both(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link [to boot dev](https://www.boot.dev)"
        self.assertEqual(extract_markdown_images(text),[('rick roll', 'https://i.imgur.com/aKaOqIh.gif')])
        self.assertEqual(extract_markdown_links(text), [('to boot dev', 'https://www.boot.dev')])

class Test_Split_Nodes_Im0age(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        #print (f"Veja os new_nodes no TESTE: {new_nodes}")
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

if __name__ == "__main__":
        unittest.main()

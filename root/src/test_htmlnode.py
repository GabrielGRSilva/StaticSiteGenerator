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

#Test 7
text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
print("Test 7 - text_to_textnodes:", text_to_textnodes(text))

#Test 8
text = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
print ("Test 8 - markdown_to_blocks:", markdown_to_blocks(text))

#Test 9
block = f"### heading block"
print ("Test 9 - heading block:", block_to_block_type(block))

#Test 10
text = "Testando um com **bold** e _italic_, com um pouco de `código python`"
print ("Test 10 - Text to Child:", text_to_children(text))

#Test 11
single_link = [TextNode("Visit [Google](http://google.com)", TextType.NORMAL)]
multiple_links = [TextNode("Go to [Google](http://google.com) and [Yahoo](http://yahoo.com)", TextType.NORMAL)]
no_links = [TextNode("Just plain text", TextType.NORMAL)]
print ("Test 11 - split_nodes_link: ", split_nodes_link(single_link), split_nodes_link(multiple_links), split_nodes_link(no_links))

#Test 12
test_text = "This is **bolded** paragraph text"
nodes = text_to_textnodes(test_text)
print(f"Test 12: {nodes}")

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

class Test_Split_Nodes_Image(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])

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

class Test_Markdown_to_Blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_2(self):
        md = """
    Let's try another test, ok?
    This one is a _bit_ different

    Let's try **a bit of bold** here

    And maaaaybe a bit of _italic_ here as well
    Maybe even
    A three line paragraph
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Let's try another test, ok?\nThis one is a _bit_ different",
                "Let's try **a bit of bold** here",
                "And maaaaybe a bit of _italic_ here as well\nMaybe even\nA three line paragraph",
            ],
        )

class Test_BlockType_Func(unittest.TestCase):
    def test_paragraph(self):
        block = "this is a normal paragraph, ok?"
        test_block = block_to_block_type(block)
        self.assertEqual(BlockType.paragraph, test_block)

    def test_heading(self):
        block = "###this is a heading!"
        test_block = block_to_block_type(block)
        self.assertEqual(BlockType.heading, test_block)

    def test_code(self):
        block = "```this is a code text```"
        test_block = block_to_block_type(block)
        self.assertEqual(BlockType.code, test_block)

    def test_quote(self):
        block = ">heeeere's a quote block"
        test_block = block_to_block_type(block)
        self.assertEqual(BlockType.quote, test_block)

    def test_unordered_list(self):
        block = "- starting an unordered list"
        test_block = block_to_block_type(block)
        self.assertEqual(BlockType.unordered_list, test_block)

        def test_ordered_list(self):
            block = "2. ordered list block"
            test_block = block_to_block_type(block)
            self.assertEqual(BlockType.ordered_list, test_block)

class Test_markdown_to_html_node(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

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

if __name__ == "__main__":
        unittest.main()

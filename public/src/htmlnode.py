from textnode import *
import re

def extract_markdown_images(text):
    return re.findall(r'!\[(.*?)\]\((.*?)\)', text)


def extract_markdown_links(text):
   return re.findall(r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)',text)


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)

        case TextType.BOLD:
            return LeafNode("b", text_node.text)

        case TextType.ITALIC:
            return LeafNode("i", text_node.text)

        case TextType.CODE:
            return LeafNode("code", text_node.text)

        case TextType.LINK: ##Change LINK later!
            return LeafNode("a", text_node.text, {"href": "https://www.google.com"})

        case TextType.IMAGE:
            return LeafNode("img", None, {"src": "SRC", "alt": "ALTTEXT"})

        case _:
            raise Exception("Invalid Text_Node type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):                     #Separate nodes into list of TextNodes based on a delimiter, like '
    new_node_list = []
    for each_old_node in old_nodes:
        if each_old_node.text_type != TextType.NORMAL:
            new_node_list.append(each_old_node)
            continue

        if each_old_node.text.count(delimiter) % 2 != 0:                       #Checks if the string contains an odd number of delimiters
            raise Exception("Invalid Markdown Syntax: You need to open AND close with the delimiter!")
        else:
            new_strings = each_old_node.text.split(delimiter)
            i = 0                                       #i is important because odd "i" is INSIDE the delimter, with text_type, while even "i" is OUTSIDE with TextType.Normal
            for each_string in new_strings:
                if i % 2 == 0 or i == 0:
                    i += 1
                    new_node_list.append(TextNode(each_string, TextType.NORMAL))

                else:
                    i += 1
                    new_node_list.append(TextNode(each_string, text_type))

    return new_node_list

def split_nodes_image(old_nodes):
    new_node_list = []
#oldnode: [TextNode(This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png), TextType.NORMAL)]
    for each_old_node in old_nodes:
        image_parts = extract_markdown_images(each_old_node.text)   #('image', 'https://i.imgur.com/zjjcJKZ.png'), ('second image', 'https://i.imgur.com/3elNhQu.png')
        text_parts = re.findall(r'(?:^|(?<=\)))([^!\[\]()]+)',each_old_node.text) #['This is text with an ', ' and another ']
        i = 0                                       #see I explanation in above function
        for image in image_parts:
           for text in text_parts:
            if i % 2 == 0 or i == 0:                        #ITERAÇÃO TÁ PEGANDO O MESMO TEXT 2 VEZES
                i += 1
                new_node_list.append(TextNode(text, TextType.NORMAL))

            else:
                i += 1
                new_node_list.append(TextNode(image[0], TextType.IMAGE, image[1]))

    print (f"NEWNODELIST == {new_node_list}")
    return new_node_list


    # example img node TextNode(This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
    # Extract Markdown Images: [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
    # TextNode ("This is a text with a ", TextType.TEXT)
    # TextNode ("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif")
    # TextNode (" and ", TextType.TEXT)
    # TextNode ("obi wan", TextType.IMAGE,(https://i.imgur.com/fJRm4Vk.jpeg) )


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        prop_string_list = []
        for i in self.props:
            each_prop_string = f'{i}="{self.props[i]}"'
            prop_string_list.append(each_prop_string)
        prop_string = " ".join(prop_string_list)
        print (prop_string)
        return prop_string

    def __repr__(self):
        children_repr = len(self.children) if self.children is not None else 0
        return f"tag = {self.tag}, value = {self.value}, children = {children_repr}, props = {self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Value can't be None")
        if self.tag is None:
            return str(self.value)
        else:
            if self.props != None:
                formatted_props = self.props_to_html()
                return f'<{self.tag}{formatted_props}>{self.value}</{self.tag}>'
            else:
                return f'<{self.tag}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag can't be None")
        elif self.children is None:
            raise ValueError("No Children object found")
        else:
            child_string_list = []
            for child in self.children:
                child_html = child.to_html()
                child_string_list.append(child_html)
        child_strings = "".join(child_string_list)
        return f'<{self.tag}>{child_strings}</{self.tag}>'

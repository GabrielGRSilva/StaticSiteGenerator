from textnode import *
import re

def extract_markdown_images(text):
    return re.findall(r'!\[(.*?)\]\((.*?)\)', text)


def extract_markdown_links(text):
   return re.findall(r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)',text)


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            node = LeafNode(None, text_node.text)
        case TextType.BOLD:
            node = LeafNode("b", text_node.text)
        case TextType.ITALIC:
            node = LeafNode("i", text_node.text)
        case TextType.CODE:
            node = LeafNode("code", text_node.text)
        case TextType.LINK:
            node = LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            node = LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Invalid Text_Node type")

    return node

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
                if i % 2 == 0:
                    new_node_list.append(TextNode(each_string, TextType.NORMAL))
                else:
                    new_node_list.append(TextNode(each_string, text_type))
                i += 1

    return new_node_list

def split_nodes_image(old_nodes):
    new_node_list = []
    for each_old_node in old_nodes:
        image_parts = extract_markdown_images(each_old_node.text)
        if len(image_parts) == 0:
            new_node_list.append(each_old_node)
        else:
            text_parts = re.findall(r'(?:^|(?<=\)))([^!\[\]()]+)',each_old_node.text) #This regex selects everything OUTSIDE of parentheses
            i = 0                                       #see I explanation in above function
            for image in image_parts:
                new_node_list.append(TextNode(text_parts[i], each_old_node.text_type))     #loop alternates between OUTSIDE parentheses (text_parts) and INSIDE (image)
                new_node_list.append(TextNode(image[0], TextType.IMAGE, image[1]))
                i += 1

            for text in text_parts:                             #This should handle cases where there is more text after the IMG markdown
                new_text_node = TextNode(text, each_old_node.text_type)
                if new_text_node not in new_node_list:
                    new_node_list.append(new_text_node)

    return new_node_list

def split_nodes_link(old_nodes): #example input: "Visit [Google](http://google.com) for search"
    new_node_list = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if links:   # if there are links to process
            current_text = node.text
            markdown_link = f"[{links[0][0]}]({links[0][1]})"
            parts = current_text.split(markdown_link)
            if parts[0]:
                new_text_node = TextNode(parts[0], node.text_type)
                new_node_list.append(new_text_node)
            new_link_node = TextNode(links[0][0], TextType.LINK, links[0][1])
            new_node_list.append(new_link_node)
            if parts[1]:                                            #Check if there are other links in the function after the first
                remaining_node = TextNode(parts[1], node.text_type)
                recursive_nodes = split_nodes_link([remaining_node])
                new_node_list.extend(recursive_nodes)
        else:
            new_node_list.append(node)
    return new_node_list

def text_to_textnodes(text):
    start_node = TextNode(text, TextType.NORMAL)

    bold_split = split_nodes_delimiter([start_node], "**", TextType.BOLD)

    italic_split = split_nodes_delimiter(bold_split,"_", TextType.ITALIC)

    code_split = split_nodes_delimiter(italic_split, "`", TextType.CODE)

    image_split = split_nodes_image(code_split)

    link_split = split_nodes_link(image_split)

    return link_split

def markdown_to_blocks(markdown):
    block_strings = markdown.split("\n\n")
    block_list = []
    for item in block_strings:
        clean_string = item.strip()
        no_excess_whitespace = clean_string.replace("    ", "")
        if no_excess_whitespace:
            block_list.append(no_excess_whitespace)

    return block_list

BlockType = Enum('BlockType', ['paragraph','heading','code','quote','unordered_list','ordered_list'])

def block_to_block_type(block):
    if block == "":
        return BlockType.paragraph
    else:
        if block.split('\n')[0].startswith('#'):
            return BlockType.heading

        elif block.split('\n')[0].startswith('```'):
            return BlockType.code

        elif block.split('\n')[0].startswith('>'):
            return BlockType.quote

        elif block.split('\n')[0].startswith('-'):
            return BlockType.unordered_list

        elif block.split('\n')[0].split()[0].endswith('.') and block.split('\n')[0].split()[0][:-1].isdigit():
            #splits then checks if the first item in block ends is a number with dot and space, like "1. " or "23. "
            return BlockType.ordered_list

        else:
            return BlockType.paragraph

def add_tags_for_blocks(block, type):
    match type:
        case BlockType.heading:
            count_hash = block.count('#')
            remove_div = block.strip('#').strip(' ')
            return f"<h{count_hash}>{remove_div}</h{count_hash}>", count_hash

        case BlockType.code:
            remove_div = block.strip('`').strip(' ')
            return f"<pre><code>{remove_div}</code></pre>"

        case BlockType.quote:
            remove_div = block.strip('>').strip(' ')
            return f"<blockquote>{remove_div}</blockquote>"

        case BlockType.unordered_list:
            html_list = []
            list_items = block.split("-")
            for item in list_items:
                if item != "":
                    item_with_tag = f"<li>{item}</li>"
                    html_list.append(item_with_tag)
            final_string = "".join(html_list)
            return f"<ul>{final_string}</ul>"

        case BlockType.ordered_list:
            html_list = []
            list_items = re.split((r'(\d. )+'), block)  #this splits the block on each number
            del list_items[0]    #remove the empty string from the beginning
            i = 0
            for item in list_items:
                items_with_tag = f"<li>{list_items[i]}" + f"{list_items[i+1]}</li>"
                html_list.append(items_with_tag)
                if i+3 < len(list_items):       #this prevents IndexError if we try to find an i or i+1 which is greater than len(list_items)
                    i += 2
            final_string = "".join(html_list)
            return f"<ol>{final_string}</ol>"

        case BlockType.paragraph:
            return f"<p>{block}</p>"

        case _:
            raise ValueError("Invalid block type")

def text_to_children(text):
    text_node_objects = text_to_textnodes(text)
    children_list = []
    for node in text_node_objects:
        new_node = text_node_to_html_node(node)
        children_list.append(new_node)
    return children_list


def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    new_html_nodes_list = []
    for block in block_list:
        block_type = block_to_block_type(block)
        if block_type == BlockType.heading:
            h_number = block.count('#')
            clean_text = block.lstrip('# ')
            new_node = ParentNode(f"h{h_number}", text_to_children(clean_text))
            new_html_nodes_list.append(new_node)
        elif block_type == BlockType.code:
            process_text_node = TextNode(block.strip('```').lstrip(), TextType.CODE)
            inner_node = [text_node_to_html_node(process_text_node)]
            new_node = ParentNode("pre", inner_node)  #Should be equivalent to HTMLNode ("pre", "", inner_node)
            new_html_nodes_list.append(new_node)
        elif block_type == BlockType.quote:
            clean_text = block.lstrip('> ')
            new_node = ParentNode("blockquote",text_to_children(clean_text))
            new_html_nodes_list.append(new_node)
        elif block_type == BlockType.unordered_list:
            children_nodes_list = []
            list_items = block.split("-")
            for item in list_items:
                if item != "":
                    clean_item = item.strip()
                    item_with_tag = ParentNode("li", text_to_children(clean_item))          #Not LeafNode - They may contain markdown stuff
                    children_nodes_list.append(item_with_tag)
            new_node = ParentNode("ul", children_nodes_list)
            new_html_nodes_list.append(new_node)
        elif block_type == BlockType.ordered_list:
            children_nodes_list = []
            list_items = block.split("\n")
            for item in list_items:
                if item != "":
                    clean_item_index = item.find(". ")
                    item_with_tag = ParentNode("li", text_to_children(item[clean_item_index+2:]))     #clean_item_index+2 guarantees you will find the dot and the space and skip past both
                    children_nodes_list.append(item_with_tag)
            new_node = ParentNode("ol", children_nodes_list)
            new_html_nodes_list.append(new_node)
        elif block_type == BlockType.paragraph:
            clean_text = block.replace("\n", " ")
            new_node = ParentNode("p", text_to_children(clean_text))
            new_html_nodes_list.append(new_node)
        else:
            raise ValueError("Invalid block type")
    return ParentNode("div", new_html_nodes_list)


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

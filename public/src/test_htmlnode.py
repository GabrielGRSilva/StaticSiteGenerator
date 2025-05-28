from htmlnode import HTMLNode, LeafNode
import unittest

# Test 1
test_props = {"href": "https://www.google.com", "target": "_blank"}
node = HTMLNode("p", "this is a props test", None, test_props)
node2 = HTMLNode("p", "this is a props test", None, None)
print("Test 1 - props_to_html():", node.props_to_html())
#print("Test 1 - props_to_html():", node2.props_to_html())

# Test 2
node2 = HTMLNode("b", "this is a node test", None, {"href": "www.google.com"})
print("Test 2 - node:", node2)

# Test 3
node3 = HTMLNode(None, "this is a value")
print("Test 3 - just value:", node3)

# Test 4
node4 = LeafNode("p", "Hello, world!")                #Test Child Class
print("Test 4 - LeafNode:", node4.to_html())

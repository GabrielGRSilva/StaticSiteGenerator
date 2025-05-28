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

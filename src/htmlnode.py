class HtmlNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        value = ""
        if self.props != None and isinstance(self.props, dict): 
            for prop in self.props:
                value += f' {prop}="{self.props[prop]}"'
        return value

    def __repr__(self):
        return f"{self.tag}, {self.value}, {self.children}, {self.props}"


class LeafNode(HtmlNode):
    def __init__(self, tag, value, props=None):
        if value is None or value == "":
            raise ValueError("self.value required")
        super().__init__(tag, value, None, props)

    def __eq__(self, other):
        return (
                self.tag == other.tag and
                self.value == other.value and
                self.props == other.props
                )


    def to_html(self):
        if not self.tag:
            return str(self.value)
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'


class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        if not tag:
            raise ValueError("Tag required")
        if not children:
            raise ValueError("Children required")
        super().__init__(tag, None, children, props)

    def to_html(self):
        output = ""
        if self.children and isinstance(self.children, list):
            for child in self.children:
                output += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{output}</{self.tag}>"




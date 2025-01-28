import re
from textnode import TextType, TextNode
from htmlnode import LeafNode

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
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", " ", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Wrong text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text == "":
            continue
        if old_node.text_type != TextType.NORMAL and old_node.text.split(delimiter)[0] != "":
            new_nodes.append(old_node)
            continue
        if not delimiter in old_node.text and old_node.text.split(delimiter)[0] != "":
            new_nodes.append(old_node)
            continue
        splitted = old_node.text.split(delimiter, maxsplit=2)
        if len(splitted) == 2:
            raise Exception("Parsing error, no matching delimiter")
        if len(splitted) == 1:
            new_nodes.append(old_node)
            continue
        if splitted[0] != "":
            new_nodes.append(TextNode(splitted[0], TextType.NORMAL))
        new_nodes.append(TextNode(splitted[1], text_type))
        new_nodes.extend(split_nodes_delimiter([TextNode(splitted[2], TextType.NORMAL)], delimiter, text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        matches = extract_markdown_images(old_node.text)
        if old_node.text == "":
            continue
        if matches == []:
            new_nodes.append(old_node)
            continue
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        image_alt, image_link = matches[0]
        delimiter = f"![{image_alt}]({image_link})"

        splitted = old_node.text.split(delimiter, maxsplit=1)
        if splitted[0] == "":
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, url=image_link))
            new_nodes.extend(split_nodes_image([TextNode(splitted[1], TextType.NORMAL)]))
        else:
            new_nodes.append(TextNode(splitted[0], TextType.NORMAL))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, url=image_link))
            new_nodes.extend(split_nodes_image([TextNode(splitted[1], TextType.NORMAL)]))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        matches = extract_markdown_links(old_node.text)
        if old_node.text == "":
            continue
        if matches == []:
            new_nodes.append(old_node)
            continue
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        link_text, link_url = matches[0]
        delimiter = f"[{link_text}]({link_url})"

        splitted = old_node.text.split(delimiter, maxsplit=1)
        if splitted[0] == "":
            new_nodes.append(TextNode(link_text, TextType.LINK, url=link_url))
            new_nodes.extend(split_nodes_link([TextNode(splitted[1], TextType.NORMAL)]))
        else:
            new_nodes.append(TextNode(splitted[0], TextType.NORMAL))
            new_nodes.append(TextNode(link_text, TextType.LINK, url=link_url))
            new_nodes.extend(split_nodes_link([TextNode(splitted[1], TextType.NORMAL)]))
    return new_nodes

def text_to_textnodes(text):
    textnodes = [TextNode(text, TextType.NORMAL)]
    textnodes = split_nodes_delimiter(textnodes, "`", TextType.CODE)
    textnodes = split_nodes_delimiter(textnodes, "**", TextType.BOLD)
    textnodes = split_nodes_delimiter(textnodes, "*", TextType.ITALIC)
    textnodes = split_nodes_image(textnodes)
    textnodes = split_nodes_link(textnodes)
    return textnodes
    

def extract_markdown_images(text):
    result = []
    if isinstance(text, str):
        matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
        if matches:
            for m in matches:
                result.append(m)
    return result

def extract_markdown_links(text):
    result = []
    if isinstance(text, str):
        matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
        if matches:
            for m in matches:
                result.append(m)
    return result


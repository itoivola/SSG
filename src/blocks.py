import re


def markdown_to_blocks(markdown):
    stripped = ""
    for line in markdown.split("\n"):
        stripped += line.strip()+"\n"
    markdown_blocks = stripped.split("\n\n")

    cleaned = []
    for x in markdown_blocks:
        if x:
            cleaned.append(x.strip())
    return cleaned


def block_to_block_type(block):

    if re.search(r"^\#{1,6} .+$", block):
        return "heading"

    if re.search(r"^```.*?```$", block, re.DOTALL):
        return "code"

    for line in block.split("\n"):
        if line[0] == ">":
            pass
        else:
            break
    else:
        return "quote"

    for line in block.split("\n"):
        if line[0] == "*" or line[0] == "-":
            pass
        else:
            break
    else:
        return "unordered list"

    olcounter = 1

    for line in block.split("\n"):
        if re.search(r"^\d+\. ", line) and str(olcounter) in line:
            olcounter += 1
        else:
            break
    else:
        return "ordered list"

    return "paragraph"

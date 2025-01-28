

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

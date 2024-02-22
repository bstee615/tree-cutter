import argparse
from tree_sitter_languages import get_parser
from fastcore.basics import store_attr

def parse_args():
    parser = argparse.ArgumentParser(description='Inline functions in a C program')
    parser.add_argument('source_file', type=str, help='Path to the C source file')
    return parser.parse_args()

def get_comments(tree):
    queue = [tree.root_node]
    while len(queue) > 0:
        node = queue.pop(0)
        if node.type == "comment":
            yield node
        queue.extend(node.children)

class Replacement:
    def __init__(self, begin, end, new_text): 
        store_attr()

    def __iter__(self):
        return iter(((self.begin, self.end), self.new_text))

def do_replacements(text, replacements):
    # sort replacements last to first
    replacements = sorted(replacements, key=lambda p: p.begin, reverse=True)
    # apply to text in order
    for (begin, end), new_text in replacements:
        if isinstance(new_text, str):
            new_text = new_text.encode()
        text = text[:begin] + new_text + text[end:]
    return text

def remove_comments(code):
    parser = get_parser("c")

    tree = parser.parse(bytes(code, 'utf-8'))

    comments = get_comments(tree)
    replacements = []
    for node in comments:
        replacements.append(Replacement(node.start_byte, node.end_byte, ""))

    new_text = do_replacements(tree.text, replacements).decode()
    return new_text

def main():
    args = parse_args()
    with open(args.source_file, 'r') as file:
        code = file.read()

    new_text = remove_comments(code)
    print(new_text)

if __name__ == '__main__':
    main()

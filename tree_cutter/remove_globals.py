import argparse
from tree_sitter_languages import get_parser
from fastcore.basics import store_attr

def parse_args():
    parser = argparse.ArgumentParser(description='Inline functions in a C program')
    parser.add_argument('source_file', type=str, help='Path to the C source file')
    return parser.parse_args()

def get_funcdefs(tree):
    queue = [tree.root_node]
    while len(queue) > 0:
        node = queue.pop(0)
        if node.type == 'function_definition':
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

def remove_globals(code):
    parser = get_parser("c")

    code_bytes = bytes(code, 'utf-8')
    tree = parser.parse(code_bytes)

    funcs = list(get_funcdefs(tree))
    funcs = sorted(funcs, key=lambda f: f.start_byte)
    replacements = []
    for i in range(len(funcs)):
        node = funcs[i]
        if i == 0:
            repl_start = 0
        else:
            repl_start = funcs[i-1].end_byte+1
        text_between = code_bytes[repl_start:node.start_byte]
        text_between = bytes([c for c in text_between if c == "\n"])
        replacements.append(Replacement(repl_start, node.start_byte, text_between))

    new_text = do_replacements(tree.text, replacements).decode()
    return new_text

def main():
    args = parse_args()
    with open(args.source_file, 'r') as file:
        code = file.read()

    new_text = remove_globals(code)
    print(new_text)

if __name__ == '__main__':
    main()

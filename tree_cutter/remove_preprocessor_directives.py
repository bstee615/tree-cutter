import argparse
from tree_sitter_languages import get_parser
from fastcore.basics import store_attr

def parse_args():
    parser = argparse.ArgumentParser(description='Inline functions in a C program')
    parser.add_argument('source_file', type=str, help='Path to the C source file')
    return parser.parse_args()

def get_preprocs(tree):
    queue = [tree.root_node]
    while len(queue) > 0:
        node = queue.pop(0)

        if node.type in [
            "preproc_if",
            "preproc_ifdef",
            "preproc_include",
            "preproc_def",
            "preproc_function_def",
            "preproc_call",
        ]:
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

def remove_preprocessor_directives(code):
    parser = get_parser("c")

    tree = parser.parse(bytes(code, 'utf-8'))

    preprocs = get_preprocs(tree)
    replacements = []
    for node in preprocs:
        replacements.append(Replacement(node.start_byte, node.end_byte, ""))

    new_text = do_replacements(tree.text, replacements).decode()
    return new_text

def main():
    args = parse_args()
    with open(args.source_file, 'r') as file:
        code = file.read()

    new_text = remove_preprocessor_directives(code)
    print(new_text)

if __name__ == '__main__':
    main()

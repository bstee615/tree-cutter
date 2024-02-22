import argparse
from tree_sitter_languages import get_parser
from fastcore.basics import store_attr

def parse_args():
    parser = argparse.ArgumentParser(description='Inline functions in a C program')
    parser.add_argument('source_file', type=str, help='Path to the C source file')
    return parser.parse_args()

def remove_blank_lines(code):
    return "".join(line for line in code.splitlines(keepends=True) if line.strip())

def main():
    args = parse_args()
    with open(args.source_file, 'r') as file:
        code = file.read()
    new_text = remove_blank_lines(code)
    print(new_text)

if __name__ == '__main__':
    main()

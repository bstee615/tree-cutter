import argparse
from tree_cutter import TRANSFORM_MAP

def parse_args():
    parser = argparse.ArgumentParser(description='Inline functions in a C program')
    parser.add_argument('source_file', type=str, help='Path to the C source file')
    parser.add_argument('transforms', nargs="+", help='Transforms to apply', choices=TRANSFORM_MAP.keys())
    return parser.parse_args()

def process(code, transforms):
    for transform in transforms:
        code = TRANSFORM_MAP[transform](code)
    return code

def main():
    args = parse_args()
    with open(args.source_file, 'r') as file:
        code = file.read()
    code = process(code, args.transforms)
    print(code)

if __name__ == '__main__':
    main()

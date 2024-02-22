# tree-cutter: utilities for transforming programs using tree-sitter

## inline.py: Inline function calls

Limitations:
- Does not handle expressions which mutate values as arguments
- May produce name clashes between identifiers in the caller and callee code
- Produces ugly transformed code
- Only tested on toy programs so far

### Usage

Run the tool and compile the test programs:

```bash
python tree_cutter/inline.py test.c foo > test_inline.c
gcc test.c -o test
gcc test_inline.c -o test_inline
```

Expected output:

```bash
$ ./test
1 + 2 = 3
$ ./test_inline
1 + 2 = 3
```
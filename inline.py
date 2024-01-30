import argparse
from tree_sitter_languages import get_parser

def parse_args():
    parser = argparse.ArgumentParser(description='Inline functions in a C program')
    parser.add_argument('source_file', type=str, help='Path to the C source file')
    parser.add_argument('function_name', type=str, help='Name of the function to inline')
    return parser.parse_args()

def get_function_node(tree, function_name):
    for node in tree.root_node.children:
        if node.type == 'function_definition':
            funcdecl = node.child_by_field_name("declarator")
            funcdecl_name = funcdecl.child_by_field_name("declarator")
            if function_name == funcdecl_name.text.decode():
                return node
    return None

def get_function_calls(tree, function_name):
    queue = [tree.root_node]
    while len(queue) > 0:
        node = queue.pop(0)
        if node.type == "call_expression":
            funcref_name = node.child_by_field_name("function")
            if function_name == funcref_name.text.decode():
                yield node
        queue.extend(node.children)

def get_parent_stmt(node):
    while node is not None:
        if node.type.endswith("statement"):
            return node
        node = node.parent

def generate_replacement(call_node, funcdef_node):
    # get statement holding the call node
    parent_stmt = get_parent_stmt(call_node)
    replacement_span = (parent_stmt.start_byte, parent_stmt.end_byte)
    transformed_call = parent_stmt.text.decode()
    relative_call_span_length = call_node.end_byte - call_node.start_byte
    relative_call_span_start = call_node.start_byte - parent_stmt.start_byte
    relative_call_span = (relative_call_span_start, relative_call_span_start+relative_call_span_length)
    # replace span of function call with reference to temporary variable
    before, after = transformed_call[:relative_call_span[0]], transformed_call[relative_call_span[1]:]
    tempvar = "FOO"
    transformed_call = before + tempvar + after
    # generate temporary variable before the call node to hold the function call result
    function_return_type = funcdef_node.child_by_field_name("type").text.decode()
    tempvar_decl = f"{function_return_type} {tempvar};"
    # prepend body of function before the call
    body_node = funcdef_node.child_by_field_name("body")
    transformed_body = body_node.text.decode()
    queue = [body_node]
    body_replacements = []
    while len(queue) > 0:
        node = queue.pop(0)
        if node.type == "return_statement":
            expr = [c for c in node.children if c.is_named and not c.type == "comment"][0]
            body_replacements.append(((node.start_byte-body_node.start_byte, expr.start_byte-body_node.start_byte), f"{tempvar} = ".encode()))
            expr_stmt = get_parent_stmt(expr)
            body_replacements.append(((expr_stmt.end_byte-body_node.start_byte, expr_stmt.end_byte-body_node.start_byte), "\ngoto inline_end;".encode()))
        queue.extend(node.children)
    transformed_body = do_replacements(transformed_body.encode(), body_replacements).decode()
    parameter_decls = []
    parameters = [c for c in funcdef_node.child_by_field_name("declarator").child_by_field_name("parameters").children if c.is_named and not c.type == "comment"]
    arguments = [c for c in call_node.child_by_field_name("arguments").children if c.is_named and not c.type == "comment"]
    for parameter, argument in zip(parameters, arguments):
        parameter_decl = f"{parameter.text.decode()} = {argument.text.decode()};"
        parameter_decls.append(parameter_decl)
    transformed_body = "\n".join((*parameter_decls, transformed_body))
    # assemble the transformed code
    start_comment = "// BEGIN INLINE"
    end_comment = "// END INLINE"
    label = "inline_end:"
    replacement_text = "\n".join((start_comment, tempvar_decl, transformed_body, label, transformed_call, end_comment))
    return (replacement_span, replacement_text.encode())

def do_replacements(text, replacements):
    # sort replacements last to first
    replacements = sorted(replacements, key=lambda p: p[0][0], reverse=True)
    # apply to text in order
    for (begin, end), new_text in replacements:
        # print("REPLACEMENT", (begin, end))
        # print(new_text)
        # print("ENDREPLACEMENT")
        text = text[:begin] + new_text + text[end:]
    return text

def main():
    args = parse_args()

    parser = get_parser("c")

    with open(args.source_file, 'r') as file:
        code = file.read()

    tree = parser.parse(bytes(code, 'utf-8'))

    funcdef_node = get_function_node(tree, args.function_name)

    replacements = []
    if funcdef_node:
        calls = get_function_calls(tree, args.function_name)
        for call in calls:
            replacements.append(generate_replacement(call, funcdef_node))

    new_text = do_replacements(tree.text, replacements).decode()
    print(new_text)

if __name__ == '__main__':
    main()

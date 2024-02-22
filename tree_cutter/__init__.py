from tree_cutter.inline_function import inline_function
from tree_cutter.remove_blank_lines import remove_blank_lines
from tree_cutter.remove_comments import remove_comments
from tree_cutter.remove_preprocessor_directives import remove_preprocessor_directives
from tree_cutter.remove_globals import remove_globals

TRANSFORM_MAP = {f.__name__: f for f in [inline_function, remove_blank_lines, remove_comments, remove_preprocessor_directives, remove_globals]}

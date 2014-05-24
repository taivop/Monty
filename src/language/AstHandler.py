import ast

class AstHandler():

    def __init__(self):
        foo = 0


    @staticmethod
    def astToCode():
        """ Input: Python AST.
            Output: string that contains the code corresponding to the AST.
        """

    @staticmethod
    def blocksToAst(blocks):
        """ Input: list of blocks.
            Output: Python AST.
        """

        # create an AST root node
        root = ast.Module()
        root.body = []

        # get the AST node of each block and add it to the body
        for block in blocks:
            node = block.getAstNode()
            root.body.append(node)

        # fix missing locations so Python doesn't complain
        root2 = ast.fix_missing_locations(root)

        return root2

    @staticmethod
    def codeToAst(code):
        # Make the output go to file-like string objects
        error = None

        try:
            # Try to parse, the code to a tree
            tree = ast.parse(code)

        except Exception as e:
            # If an exception occurred, remember it
            error = e.__class__.__name__

        return tree, error


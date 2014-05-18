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


from gui.Blocks import *
from language.astpp import dump
import ast

# Create an assignment block and a print block
assign_block = AssignBlock("x", 7)
assign_block2 = AssignBlock("y", 11)
assign_block3 = AssignBlock("z", "x+y")
print_block = PrintBlock("z")

bloxx = [assign_block, assign_block2, assign_block3, print_block]

# pretty-print the ast node of the block
#print(dump(assign_block.getAstNode()))

# create an AST
root = ast.Module()

# append the nodes from the block to the list of nodes
root.body = []
for block in bloxx:
    root.body.append(block.getAstNode())

# fix missing locations so Python does not complain
root2 = ast.fix_missing_locations(root)

# compile and execute the AST that we just created from scratchs
exec(compile(root, "<test>", "exec"))


# now do the same thing with the AstHandler class
print('now using AstHandler')
from language.asthandler import AstHandler

blocks = [assign_block, print_block]
root = AstHandler.blocksToAst(blocks)
exec(compile(root, "<test>", "exec"))


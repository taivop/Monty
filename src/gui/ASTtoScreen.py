import ast

import pygame

from language import astpp


program = """
x = 3
y = 4
x+y
"""

# parse program to AST
tree = ast.parse(program)
b = tree.body

# initialise pygame stuff
pygame.init()
screen = pygame.display.set_mode( (1000, 600) )
pygame.display.set_caption("AST overview display")
screen.fill( (126,206,214) )
myfont = pygame.font.SysFont("Courier New", 20)

# for each element in the main body (roughly every line in the program)
for i in range(0,len(b)):
    # get the node
    node = b[i]

    # make label using the pretty-print function
    label = "body[{0}] -> {1}".format(i, astpp.dump(node)) #str(type(node)))

    # make label object and display
    label_obj = myfont.render(label, 1, (0, 0, 0))
    screen.blit(label_obj, (30, 50+i*100))
    pygame.display.flip()


while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
pygame.quit()
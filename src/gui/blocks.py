import pygame
import os
import ast

class Block(pygame.sprite.Sprite): # Something we can create and manipulate
    def __init__(self,color,pos,width,height): # initialze the properties of the object
        pygame.sprite.Sprite.__init__(self)
        self.color=color
        self.pos=pos
        self.width=width
        self.height=height
        self.image = pygame.image.load((os.path.sep).join(os.getcwd().split(os.path.sep)[:-2])+os.path.sep+"resources"+os.path.sep+"blockimg.png")
        self.rect = self.image.get_rect()
        self.rect.x , self.rect.y = pos
        self.child = None

    def hasChild(self):
        return self.child is not None

    def Render(self,screen):
        blockimg = pygame.image.load("../../resources/blockimg.png")
        screen.blit(blockimg,(self.pos))

class AssignBlock():
    """ Class for assignment statements, e.g. x = 4. Right now x = y + 5 type assignment not supported.
    """
    var_name = None
    value = None
    def __init__(self, var_name, value):
        #Block.__init__(self)
        self.var_name = var_name
        self.value = value
        # do something

    def getAstNode(self):
        node = ast.Assign()
        node.targets = [ast.Name(id=self.var_name, ctx=ast.Store())]
        node.value = ast.Num(n=self.value)

        return node




class PrintBlock():
    """ Class for print statements, e.g. print(x). Right now supports only printing variable values.
    """
    expression = None
    def __init__(self, expression):
        #Block.__init__(self)
        self.expression = expression

    def getAstNode(self):
        node = ast.Expr()
        node.value = ast.Call(func=ast.Name(id='print', ctx=ast.Load()), keywords=[], starargs=None, kwargs=None)
        node.value.args = [ast.Name(id=self.expression, ctx=ast.Load())]

        return node
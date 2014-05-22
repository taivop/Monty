import pygame
from random import randint # for testing purposes, random color of 3 on every block

import os
from gui.eztext import Textbox
from language.asthandler import AstHandler
from gui.DebugHelper import DebugHelper

class Block(pygame.sprite.Sprite): # Something we can create and manipulate

    def __init__(self,color,pos,width,height): # initialze the properties of the object
        pygame.sprite.Sprite.__init__(self)
        self.color=color
        self.pos=pos
        self.width=width
        self.height=height
        self.image = pygame.image.load((os.path.sep).join(os.getcwd().split(os.path.sep)[:-2])+os.path.sep+"resources"+os.path.sep+"block"+str(randint(1,3))+".png")
        self.rect = self.image.get_rect()
        self.rect.x , self.rect.y = pos
        self.child = None
        self.parent = None
        self.textbox = Textbox()
        self.textbox2= Textbox(True)
        self.deltax=0
        self.deltay=0

    def hasParent(self):
        return self.parent is not None

    def hasChild(self):
        return self.child is not None

    def Render(self,screen):
        DebugHelper.drawDebugRect(self.rect, screen)

        blockimg = self.image
        screen.blit(blockimg,(self.pos))

        #Textbox
        self.textbox.Render(screen, self.pos[0]+2,self.pos[1]+12,60,20)

        #Operator
        font = pygame.font.Font(None, 30)
        text = font.render("=",1,(255,255,255))
        screen.blit(text, (self.pos[0]+70,self.pos[1]+10))

        #Textbox
        self.textbox2.Render(screen, self.pos[0]+92,self.pos[1]+12,60,20)

class AssignBlock():
    """ Class for assignment statements. Tested for x = 1, y = x+5, z = x+y (and analogous assignments)
    """
    var_name = None
    value = None
    text = None
    def __init__(self, var_name, value):
        #Block.__init__(self)
        self.var_name = var_name
        self.value = value

    def getAstNode(self):
        # TODO: handle error if not a legal assignment
        # TODO: security risk if var_name or value contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())

        return tree.body[0]

    def makeText(self):
        # create code corresponding to this block
        self.text = "{0} = {1}".format(self.var_name, self.value)

    def getText(self):
        # get the code corresponding to this block
        self.makeText()
        return self.text

        return node




class PrintBlock():
    """ Class for print statements, e.g. print(x). Tested for print(x), print(x+5) (and analogous prints)
    """
    expression = None
    def __init__(self, expression):
        #Block.__init__(self)
        self.expression = expression

    def getAstNode(self):
        # TODO: handle error if not a legal print
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())

        return tree.body[0]


    def makeText(self):
        # create code corresponding to this block
        self.text = "print({0})".format(self.expression)

    def getText(self):
        # get the code corresponding to this block
        self.makeText()
        return self.text


        return node

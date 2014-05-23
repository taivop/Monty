import pygame
from random import randint # for testing purposes, random color of 3 on every block

import os
from gui.eztext import Textbox
from language.asthandler import AstHandler
from gui.DebugHelper import DebugHelper

class Block(pygame.sprite.Sprite): # Something we can create and manipulate

    def __init__(self, pos, path): # initialze the properties of the object
        pygame.sprite.Sprite.__init__(self)
        self.pos=pos
        self.image = pygame.image.load(path)
        #self.image = pygame.image.load((os.path.sep).join(os.getcwd().split(os.path.sep)[:-2])+os.path.sep+"resources"+os.path.sep+"block"+str(randint(1,3))+".png")
        self.rect = self.image.get_rect()
        self.rect.x , self.rect.y = pos
        self.width = 200
        self.height = 40
        self.child = None
        self.parent = None
        self.textbox = None
        self.textbox2= None
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

    def getChildren(self, list):
        list.append(self)
        if self.hasChild():
            self.child.getChildren(list)

class AssignBlock(Block):
    """ Class for assignment statements. Tested for x = 1, y = x+5, z = x+y (and analogous assignments)
    """
    var_name = None
    value = None
    text = None
    def __init__(self, pos):
        super().__init__(pos, "block1.png")
        self.var_name = "Default"
        self.value = "Default"
        self.textbox = Textbox(7)
        self.textbox2 = Textbox(7)

    def getAstNode(self):
        # TODO: handle error if not a legal assignment
        # TODO: security risk if var_name or value contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())

        return tree.body[0]

    def makeText(self):
        # create code corresponding to this block
        self.var_name = self.textbox.getValue()
        self.value = self.textbox2.getValue()
        self.text = "{0} = {1}".format(self.var_name, self.value)

    def getText(self):
        # get the code corresponding to this block
        self.makeText()
        return self.text

        return node

    def Render(self, screen):
        super().Render(screen)
        #Textbox
        self.textbox.Render(screen, self.pos[0]+2,self.pos[1]+12,84,20)

        #Operator
        font = self.title_font = pygame.font.Font("OpenSans-Regular.ttf", 25)
        text = font.render("=",1,(0,0,0))
        screen.blit(text, (self.pos[0]+89,self.pos[1]+10))

        #Textbox
        self.textbox2.Render(screen, self.pos[0]+104,self.pos[1]+12,84,20)




class PrintBlock(Block):
    """ Class for print statements, e.g. print(x). Tested for print(x), print(x+5) (and analogous prints)
    """
    expression = None
    def __init__(self, pos):
        super().__init__(pos, "block2.png")
        self.expression = "Default"
        self.textbox = Textbox(12)

    def getAstNode(self):
        # TODO: handle error if not a legal print
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())

        return tree.body[0]


    def makeText(self):
        # create code corresponding to this block
        self.expression = self.textbox.getValue()
        self.text = "print({0})".format(self.expression)

    def getText(self):
        # get the code corresponding to this block
        self.makeText()
        return self.text


        return node

    def Render(self, screen):
        super().Render(screen)
        #Operator
        font = self.title_font = pygame.font.Font("OpenSans-Regular.ttf", 18, bold=True)
        text = font.render("Print",1,(0,0,0))
        screen.blit(text, (self.pos[0]+2,self.pos[1]+12))
        self.textbox.Render(screen, self.pos[0]+60,self.pos[1]+10,135,20)

import pygame
from random import randint # for testing purposes, random color of 3 on every block

import os
from gui.eztext import Textbox
from language.asthandler import AstHandler
from gui.DebugHelper import DebugHelper

class Block(pygame.sprite.Sprite): # Something we can create and manipulate

    def __init__(self, pos, path, moveRight, moveLeft, block_string): # initialze the properties of the object
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
        self.deltax=0
        self.deltay=0
        self.moveRight = moveRight
        self.moveLeft = moveLeft
        self.textboxes = []
        self.title_font = pygame.font.Font("OpenSans-Regular.ttf", 18, bold=True)
        self.title_text = self.title_font.render(block_string,1,(0,0,0))

    def getTextboxes(self):
        return self.textboxes

    def hasParent(self):
        return self.parent is not None

    def hasChild(self):
        return self.child is not None

    def Render(self,screen):
        DebugHelper.drawDebugRect(self.rect, screen)
        blockimg = self.image
        screen.blit(blockimg,(self.pos))

    def getChildren(self, list): # Current block + Children
        list.append(self)
        if self.hasChild():
            self.child.getChildren(list)

    def getText(self):
        # get the code corresponding to this block
        return self.makeText()


        return node

    def connect(self, block_group):
        children = []
        self.getChildren(children)
        lastChild = children[len(children)-1]
        for item in block_group:
            if item != self and pygame.sprite.collide_rect(item, self):
                self.connectBlocks(item)
            elif item != lastChild and pygame.sprite.collide_rect(item, lastChild):
                lastChild.connectBlocks(item)

    def connectBlocks(self, block):
        if self.pos[1]<block.pos[1]:
            upperblock = self
            bottomblock = block
        else:
            upperblock = block
            bottomblock = self

        if upperblock.hasChild() or bottomblock.hasParent():
            return
        upperblock.child = bottomblock
        bottomblock.parent = upperblock
        upperblock.moveChildren()

        print("connected blocks")

    def moveChildren(self):
        children = []
        self.getChildren(children)
        for i in range(1, len(children)):
            child = children[i]
            parent = children[i-1]
            child.pos = parent.pos[0]+parent.moveRight-child.moveLeft, parent.pos[1]+parent.height
            child.rect.x = parent.pos[0]+ parent.moveRight- child.moveLeft
            child.rect.y = parent.pos[1]+parent.height


class OneBoxBlock(Block):
    def __init__(self, pos, path, codebox_string, block_string, box_length, box_x, box_y, moveRight=0, moveLeft=0):
        super().__init__(pos, path, moveRight, moveLeft, block_string)
        self.textboxes.append(Textbox(box_length))
        self.codebox_string = codebox_string
        self.block_string = block_string
        self.box_x = box_x
        self.box_y = box_y

    def makeText(self):
        # create code corresponding to this block
        expression = self.textboxes[0].getValue()
        return self.codebox_string.format(expression)


    def Render(self, screen):
        super().Render(screen)
        screen.blit(self.title_text, (self.pos[0]+2,self.pos[1]+7))
        self.textboxes[0].Render(screen, self.pos[0]+self.box_x, self.pos[1]+self.box_y)


class TwoBoxBlock(Block):
    def __init__(self, pos, path, codebox_string, block_string, box_length1, box_length2, moveRight=0, moveLeft=0):
        super().__init__(pos, path, moveRight, moveLeft, block_string)
        self.textboxes.append(Textbox(box_length1))
        self.textboxes.append(Textbox(box_length2))
        self.codebox_string = codebox_string
        self.block_string = block_string
        #self.box_x = box_x
        #self.box_y = box_y

    def makeText(self):
        # create code corresponding to this block
        var_name = self.textboxes[0].getValue()
        value = self.textboxes[1].getValue()
        return self.codebox_string.format(var_name, value)


    def Render(self, screen):
        super().Render(screen)
        #Textbox
        self.textboxes[0].Render(screen, self.pos[0]+2,self.pos[1]+12)

        #Operator
        screen.blit(self.title_text, (self.pos[0]+89,self.pos[1]+5))

        #Textbox
        self.textboxes[1].Render(screen, self.pos[0]+104,self.pos[1]+12)

class NoBoxBlock(Block):
    def __init__(self, pos, path, codeboxString, blockString, moveRight=0, moveLeft=0):
        super().__init__(pos, path, moveRight, moveLeft, blockString)
        self.blockString = blockString

    def Render(self, screen):
        super().Render(screen)
        screen.blit(self.title_text, (self.pos[0]+2,self.pos[1]+7))

    def makeText(self):
        return ""


class AssignBlock(TwoBoxBlock):
    """ Class for assignment statements. Tested for x = 1, y = x+5, z = x+y (and analogous assignments)
    """
    def __init__(self, pos):
        super().__init__(pos, "block1.png", "{0} = {1}", "=", 7, 7)


    def getAstNode(self):
        # TODO: handle error if not a legal assignment
        # TODO: security risk if var_name or value contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())

        return tree.body[0]


class PrintBlock(OneBoxBlock):
    """ Class for print statements, e.g. print(x). Tested for print(x), print(x+5) (and analogous prints)
    """
    def __init__(self, pos):
        super().__init__(pos, "block2.png", "print({0})", "Trüki", 12, 60, 10)

    def getAstNode(self):
        # TODO: handle error if not a legal print
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())

        return tree.body[0]

class ForwardBlock(OneBoxBlock):
    def __init__(self, pos):
        super().__init__(pos, "block3.png", "fd({0})", "Edasi",12,60, 10)

    def getAstNode(self):
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())
        return tree.body[0]

class LeftBlock(OneBoxBlock):
    def __init__(self, pos):
        super().__init__(pos, "block3.png", "lt({0})", "Vasak",12, 60, 10)

    def getAstNode(self):
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())
        return tree.body[0]

class RightBlock(OneBoxBlock):
    def __init__(self, pos):
        super().__init__(pos, "block3.png", "rt({0})", "Parem", 12,60, 10)

    def getAstNode(self):
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())
        return tree.body[0]

class IfBlock(OneBoxBlock):
    def __init__(self, pos):
        super().__init__(pos, "block4.png", "if {0}:", "Kas", 12, 60, 10, moveRight=18)

    def getAstNode(self):
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())
        return tree.body[0]

class EndIfBlock(NoBoxBlock):
    def __init__(self, pos):
        super().__init__(pos, "block5.png", "", "Kui ei, jätkame siit", moveLeft=18)

    def getAstNode(self):
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())
        return tree.body[0]
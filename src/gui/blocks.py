import pygame
from random import randint # for testing purposes, random color of 3 on every block

import os
from gui.eztext import Textbox
from language.AstHandler import AstHandler
from gui.DebugHelper import DebugHelper

class Block(pygame.sprite.Sprite): # Something we can create and manipulate

    def __init__(self, pos, path, codebox_string, elements, move_right=0, move_left=0): # initialze the properties of the object
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
        self.move_right = move_right
        self.move_left = move_left
        self.codebox_string = codebox_string
        self.elements = elements


    def hasParent(self):
        return self.parent is not None

    def hasChild(self):
        return self.child is not None

    def Render(self,screen):
        DebugHelper.drawDebugRect(self.rect, screen)
        blockimg = self.image
        screen.blit(blockimg,(self.pos))
        for item in self.elements.textboxes:
            item.Render(screen, self.pos[0], self.pos[1])
        for item in self.elements.texts:
            item.Render(screen, self.pos[0], self.pos[1])

    def makeText(self):
        # create code corresponding to this block
        return self.codebox_string.format(*self.elements.getTextboxValues())


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
            child.pos = parent.pos[0]+parent.move_right-child.move_left, parent.pos[1]+parent.height
            child.rect.x = parent.pos[0]+ parent.move_right- child.move_left
            child.rect.y = parent.pos[1]+parent.height

class BlockElementList():
    def __init__(self, list):
        self.textboxes = []
        self.texts = []
        for item in list:
            if isinstance(item[0], int):
                self.textboxes.append(TextboxElement(item[0],item[1],item[2]))
            else:
                self.texts.append(TextElement(item[0],item[1],item[2]))

    def getTextboxValues(self):
        result = []
        for item in self.textboxes:
            result.append(item.getValue())
        return result

    def getTextBox(self, i):
        return self.textboxes[i]

class BlockElement():
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y

    def getElement(self):
        return self.pointer


class TextboxElement(BlockElement):
    def __init__(self, value, x, y):
        super().__init__(value, x, y)
        self.pointer = Textbox(self.value)

    def Render(self, screen, x, y):
        self.pointer.Render(screen, x+self.x, y+self.y)

    def getValue(self):
        return self.pointer.getValue()

class TextElement(BlockElement):
    def __init__(self, value, x, y):
        super().__init__(value, x, y)
        title_font = pygame.font.Font("OpenSans-Regular.ttf", 18, bold=True)
        self.pointer = title_font.render(self.value, 1, (0,0,0))

    def Render(self, screen, x, y):
        screen.blit(self.pointer, (x+self.x, y+self.y))

class AssignBlock(Block):
    """ Class for assignment statements. Tested for x = 1, y = x+5, z = x+y (and analogous assignments)
    """
    def __init__(self, pos):
        list = BlockElementList(((7,2,12),(7,104,12), ("=",89,8)))
        super().__init__(pos, "block1.png", "{0} = {1}", list)


    def getAstNode(self):
        # TODO: handle error if not a legal assignment
        # TODO: security risk if var_name or value contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())

        return tree.body[0]


class PrintBlock(Block):
    """ Class for print statements, e.g. print(x). Tested for print(x), print(x+5) (and analogous prints)
    """
    def __init__(self, pos):
        list = BlockElementList(((12,60,10),("Trüki",2,7)))
        super().__init__(pos, "block2.png", "print({0})", list)

    def getAstNode(self):
        # TODO: handle error if not a legal print
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())

        return tree.body[0]

class ForwardBlock(Block):
    def __init__(self, pos):
        list = BlockElementList(((12,60,10),("Edasi",2,7)))
        super().__init__(pos, "block3.png", "fd({0})", list)

    def getAstNode(self):
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())
        return tree.body[0]

class LeftBlock(Block):
    def __init__(self, pos):
        list = BlockElementList(((12,60,10),("Vasak",2,7)))
        super().__init__(pos, "block3.png", "lt({0})", list)

    def getAstNode(self):
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())
        return tree.body[0]

class RightBlock(Block):
    def __init__(self, pos):
        list = BlockElementList(((12,60,10),("Parem",2,7)))
        super().__init__(pos, "block3.png", "rt({0})", list)

    def getAstNode(self):
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())
        return tree.body[0]

class IfBlock(Block):
    def __init__(self, pos):
        list = BlockElementList((("Kas",2,7),(12,40,10),("?",185,7)))
        super().__init__(pos, "block4.png", "if {0}:", list, move_right=18)

    def getAstNode(self):
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())
        return tree.body[0]

class EndIfBlock(Block):
    def __init__(self, pos):
        list = BlockElementList((("Kui ei, jätkame siit",2,7),))
        super().__init__(pos, "block5.png", "", list, move_left=18)

    def getAstNode(self):
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())
        return tree.body[0]
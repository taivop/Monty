import pygame

import os
from gui.eztext import Textbox
from language.AstHandler import AstHandler
from gui.DebugHelper import DebugHelper
from gui.StartTriangle import StartTriangle


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

    def changeTextbox(self, targettext, anc=False): # eeldame, et textboxid tehti samas järjekorras, mis nad blocki peal on
        boxes = self.elements.textboxes
        for i in range(len(boxes)):
            if self.elements.getTextbox(i) == targettext:
                if i < len(boxes)-1:
                    return self.elements.getTextbox(i+1), self
        result, ite = self.rek()
        if result != None:
             return result, ite
        else:
            ancestors = []
            self.getAncestors(ancestors)
            first = ancestors[len(ancestors)-1]
            #if isinstance(first, StartTriangle):
            #    first = ancestors[len(ancestors)-2]
            if len(first.elements.textboxes) != 0:
                return first.elements.getTextbox(0), first
            return first.rek()
        return None, None

    def rek(self):
        if self.hasChild():
            if len(self.child.elements.textboxes) != 0:
                return self.child.elements.getTextbox(0), self.child
            else:
                return self.child.rek()
        return None, None

    def getAncestors(self, list):
        list.append(self)
        if self.hasParent() and not isinstance(self.parent, StartTriangle):
            self.parent.getAncestors(list)

class HelperBlock(pygame.sprite.Sprite):
    def __init__(self,top_left_pos,path):
        pygame.sprite.Sprite.__init__(self)
        self.x = top_left_pos[0]
        self.y = top_left_pos[1]
        self.pos = top_left_pos
        self.image = pygame.image.load(path)

    def Render(self,screen):
        screen.blit(self.image,self.pos)
    
class BlockElementList():
    def __init__(self, list):
        self.textboxes = []
        self.texts = []
        for item in list:
            if isinstance(item[0], int):
                self.textboxes.append(TextboxElement(item))
            else:
                self.texts.append(TextElement(item))

    def getTextboxValues(self):
        result = []
        for item in self.textboxes:
            result.append(item.getValue())
        return result

    def getTextbox(self, i):
        if i >= 0 and i < len(self.textboxes):
            return self.textboxes[i].pointer

class BlockElement():
    def __init__(self, item):
        self.value = item[0]
        self.x = item[1]
        self.y = item[2]
        self.info = ""
        if len(item) > 3:
            self.info = item[3]

    def getElement(self):
        return self.pointer


class TextboxElement(BlockElement):
    def __init__(self, item):
        super().__init__(item)
        self.pointer = Textbox(self.value, self.info)

    def Render(self, screen, x, y):
        self.pointer.Render(screen, x+self.x, y+self.y)

    def getValue(self):
        return self.pointer.getValue()

class TextElement(BlockElement):
    def __init__(self, item):
        super().__init__(item)
        title_font = pygame.font.Font("resources/OpenSans-Regular.ttf", 18, bold=True)
        self.pointer = title_font.render(self.value, 1, (0,0,0))

    def Render(self, screen, x, y):
        screen.blit(self.pointer, (x+self.x, y+self.y))

class AssignBlock(Block):
    """ Class for assignment statements. Tested for x = 1, y = x+5, z = x+y (and analogous assignments)
    """
    def __init__(self, pos):
        list = BlockElementList(((7,2,12, "varbox"),(7,104,12), ("=",89,8)))
        super().__init__(pos, "resources/assignblock.png", "{0} = {1}", list)


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
        super().__init__(pos, "resources/printblock.png", "print({0})", list)

    def getAstNode(self):
        # TODO: handle error if not a legal print
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())

        return tree.body[0]

class ForwardBlock(Block):
    def __init__(self, pos):
        list = BlockElementList(((12,60,10),("Edasi",2,7)))
        super().__init__(pos, "resources/turtleblock.png", "fd({0})", list)

    def getAstNode(self):
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())
        return tree.body[0]

class BackBlock(Block):
    def __init__(self, pos):
        list = BlockElementList(((12,60,10),("Tagasi",2,7)))
        super().__init__(pos, "resources/turtleblock.png", "bk({0})", list)

    def getAstNode(self):
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())
        return tree.body[0]

class LeftBlock(Block):
    def __init__(self, pos):
        list = BlockElementList(((12,60,10),("Vasak",2,7)))
        super().__init__(pos, "resources/turtleblock.png", "lt({0})", list)

    def getAstNode(self):
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())
        return tree.body[0]

class RightBlock(Block):
    def __init__(self, pos):
        list = BlockElementList(((12,60,10),("Parem",2,7)))
        super().__init__(pos, "resources/turtleblock.png", "rt({0})", list)

    def getAstNode(self):
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())
        return tree.body[0]

class IfBlock(Block):
    def __init__(self, pos):
        list = BlockElementList((("Kas",2,7),(12,40,10,"ifbox"),("?",185,7)))
        super().__init__(pos, "resources/ifblock.png", "if {0}:", list, move_right=18)

    def getAstNode(self):
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())
        return tree.body[0]

class EndIfBlock(Block):
    def __init__(self, pos):
        list = BlockElementList((("Kui ei, jätkame siit",2,7),))
        super().__init__(pos, "resources/endifblock.png", "", list, move_left=18)

    def getAstNode(self):
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())
        return tree.body[0]

class WhileBlock(Block):
    def __init__(self, pos):
        list = BlockElementList((("Kuni",2,7),(10,43,10,"ifbox"),(", tee",160,7)))
        super().__init__(pos, "resources/whileblock.png", "while {0}:", list, move_right=18)

    def getAstNode(self):
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())
        return tree.body[0]

class EndWhileBlock(Block):
    def __init__(self, pos):
        list = BlockElementList((("Kui tehtud jätkame siit",2,7),))
        super().__init__(pos, "resources/endwhileblock.png", "", list, move_left=18)

    def getAstNode(self):
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())
        return tree.body[0]


class FunctionBlock(Block):
    def __init__(self, pos):
        list = BlockElementList((("Tagasta",2,7),(10,75,10,"argbox")))
        super().__init__(pos, "resources/endfunctionblock.png", "return {0}", list, move_left=18)

    def getAstNode(self):
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())
        return tree.body[0]

class EndFunctionBlock(Block):
    def __init__(self, pos):
        list = BlockElementList((("Funktsiooni lõpp",2,7),))
        super().__init__(pos, "resources/endfunctionblock.png", "", list, move_left=18)

    def getAstNode(self):
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())
        return tree.body[0]

class EmptyBlock(Block):
    def __init__(self, pos):
        list = BlockElementList(((17,2,10,"argbox"),))
        super().__init__(pos, "resources/emptyblock.png", "{0}", list)

    def getAstNode(self):
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())
        return tree.body[0]

class ForBlock(Block):
    def __init__(self, pos):
        list = BlockElementList(((9,40,10),("Tee",2,7),("korda",146,7)))
        super().__init__(pos, "resources/forblock.png", "for _ in range({0}):", list, move_right=18)

    def getAstNode(self):
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())
        return tree.body[0]

class EndForBlock(Block):
    def __init__(self, pos):
        list = BlockElementList((("Kui tehtud jätkame siit",2,7),))
        super().__init__(pos, "resources/endforblock.png", "", list, move_left=18)
    def getAstNode(self):
        # TODO: security risk if expressions contains unwanted code => should sanitise/restrict input!
        (tree, error) = AstHandler.codeToAst(self.getText())
        return tree.body[0]

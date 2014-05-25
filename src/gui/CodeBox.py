import pygame
from gui.DebugHelper import DebugHelper
from gui.blocks import *
from language.CodeRunner import CodeRunner


class CodeBox(pygame.sprite.Sprite):

    pos = (700,0)

    x = pos[0]                     # x of top left corner of codebox
    y = pos[1]                       # y of top left corner of codebox
    width = 1000-pos[0]                 # width of codebox
    height = 400                # height of codebox

    title_height = 50           # height of title box

    top_padding = 60            # top-padding of first line of text
    left_padding = 10           # left-padding of every line of text
    line_height = 23            # height of each line of text

    rect = pygame.Rect(x, y, width, height)

    font = None
    title_font = None

    lineList = []
    blockList = []
    start_triangle_child_count = -1

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("Courier New", 18)
        self.title_font = pygame.font.Font("OpenSans-Regular.ttf", 26)


    def Render(self,screen):

        pygame.draw.rect(screen, (255,255,255), (self.x,self.y,self.width,self.height)) # main white box
        pygame.draw.rect(screen, (124,201,255), (self.x,self.y,self.width,self.title_height)) # title box
        DebugHelper.drawDebugRect(self.rect, screen)

        # Title line
        label_obj = self.title_font.render("Programmi kood:", 1, (0, 0, 0))
        blit = screen.blit(label_obj, (self.x+self.left_padding, self.y+5))
        DebugHelper.drawDebugRect(blit, screen)


        # Draw lines of code
        self.updateLineList()
        for i in range(0, len(self.lineList)):
            line = self.lineList[i]
            label_obj = self.font.render(line, 1, (0, 0, 0))
            blit = screen.blit(label_obj, (self.x+self.left_padding, self.y+self.top_padding+i*self.line_height))
            DebugHelper.drawDebugRect(blit, screen)

    def updateLineList(self):
        self.lineList = []
        indent = 0
        for block in self.blockList:
            self.lineList.append(indent * "  " + block.getText())
            if block.__class__.__name__ == "IfBlock" or block.__class__.__name__ == "WhileBlock" or block.__class__.__name__ == "FunctionBlock"\
                    or block.__class__.__name__ == "ForBlock":
                indent += 1
            elif block.__class__.__name__ == "EndIfBlock" or block.__class__.__name__ == "EndWhileBlock" or block.__class__.__name__== "EndFunctionBlock"\
                    or block.__class__.__name__ == "EndForBlock":
                indent -= 1

    def update(self, triangle_group):
        self.blockList = []
        children = []
        for triangle in triangle_group:
            if triangle.child != None:
                children = []
                triangle.child.getChildren(children)
                #if self.start_triangle_child_count != len(children):
                self.blockList.extend(children)
        self.start_triangle_child_count = len(children)



class RunBox(pygame.sprite.Sprite):

    x = CodeBox.x                   # x of code running box
    y = 400                         # y of code running box
    width = CodeBox.width           # width of code running box
    height = 600-y       # height of code running box

    title_height = CodeBox.title_height           # height of title box

    top_padding = CodeBox.top_padding            # top-padding of first line of text
    left_padding = CodeBox.left_padding           # left-padding of every line of text
    line_height = CodeBox.line_height            # height of each line of text

    rect = pygame.Rect(x, y, width, height)

    codebox = None

    font = None
    title_font = None

    coderunner = None
    run_output = ""
    run_error = ""

    errorExplanations = {
        "SyntaxError":  "Süntaksi viga\n* kontrolli programm üle!\n*kas kastid on täidetud?",
        "NameError": "Nimeerind\n*kas kasutatavad muutujad\non ikka väärtustatud?",
        "IndentationError" : "Taandeerind\n* ega mõni tsükkel või\nvalik tühi pole?"
    }

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("Courier New", 18)
        self.title_font = pygame.font.Font("OpenSans-Regular.ttf", 26)
        self.coderunner = CodeRunner()

    def getProgramText(self):
       # Get program text
        programText = ""

        # If we have any turtle statements, add turtle import
        addTurtle = False
        for block in self.codebox.blockList:
            name = block.__class__.__name__
            if name == "ForwardBlock" or name == "RightBlock" or name == "LeftBlock" or name == "BackBlock":
                addTurtle = True

        if addTurtle:
            programText += "from turtle import *\n"

        # Add all program lines
        for line in self.codebox.lineList:
            programText += line + "\n"

        if addTurtle:
            programText += "exitonclick()\n"

        return programText

    def updateRunResult(self):
       # Get program text
        programText = ""
        function_names = []
        arguments = []

        # If we have any turtle statements, add turtle import
        addTurtle = False
        for block in self.codebox.blockList:
            name = block.__class__.__name__
            if name == "ForwardBlock" or name == "RightBlock" or name == "LeftBlock" or name == "BackBlock":
                addTurtle = True
            elif name == "FunctionBlock":
                function_names.append(block.elements.getTextbox(0).getValue())


        if addTurtle:
            programText += "from turtle import *\n"
            arguments.extend(["fd","bk","lt","rt","exitonclick"])
        if len(function_names) != 0:
            programText += "global " + ",".join(function_names)+"\n"

        programText += "def main(" + ",".join(arguments) + "):\n"

        # Add all program lines
        for line in self.codebox.lineList:
            programText += "  "+ line + "\n"

        if addTurtle:
            programText += "  exitonclick()\n"

        programText += "main(" + ",".join(arguments) + ")\n"

        result = self.coderunner.execute(programText)
        self.run_output = result[0]
        self.run_error = result[1]
        print(self.run_error)

    def clear(self):
        self.run_output = ""

    def Render(self,screen):

        pygame.draw.rect(screen, (255,255,255), (self.x,self.y,self.width,self.height)) # main white box
        pygame.draw.rect(screen, (124,201,255), (self.x,self.y,self.width,self.title_height)) # title box
        DebugHelper.drawDebugRect(self.rect, screen)

        # Title line
        label_obj = self.title_font.render("Väljund:", 1, (0, 0, 0))
        blit = screen.blit(label_obj, (self.x+self.left_padding, self.y+5))
        DebugHelper.drawDebugRect(blit, screen)

        if self.run_error is None:
            # No error -> show program output
            lines = self.run_output.split('\n')
            for i in range(0, len(lines)):
                line = lines[i]
                label_obj = self.font.render(line, 1, (0, 0, 0))
                blit = screen.blit(label_obj, (self.x+self.left_padding, self.y+self.top_padding+i*self.line_height))
                DebugHelper.drawDebugRect(blit, screen)
        else:
            # Error -> show error
            rawErrorText = self.run_error

            displayedErrorText = rawErrorText
            # If we have a translation/explanation for the error, show it
            if rawErrorText in self.errorExplanations:
                displayedErrorText = self.errorExplanations[rawErrorText]

            displayedErrorTextLines = displayedErrorText.split("\n")
            for i in range(len(displayedErrorTextLines)):
                label_obj = self.font.render(displayedErrorTextLines[i], 1, (255, 0, 0))
                blit = screen.blit(label_obj, (self.x+self.left_padding, self.y+self.top_padding+self.line_height*i))
            DebugHelper.drawDebugRect(blit, screen)


        # Errors


class RunButton(pygame.sprite.Sprite):

    def __init__(self): # initialze the properties of the object
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font("OpenSans-Regular.ttf", 18)
        self.color = (255,255,255)
        self.borderColor = (0,0,0)
        self.text = self.font.render("Käivita!", 1, self.color)
        self.rect = self.text.get_rect()
        self.rect.width = 75
        self.rect.height = 30
        self.width = self.rect.width
        self.height = self.rect.height
        self.pos = (RunBox.x+220,RunBox.y+12)
        self.rect.x = self.pos[0]-5
        self.rect.y = self.pos[1]-2

    def Render(self, screen):
        rect = pygame.draw.rect(screen, self.borderColor, self.rect, 0)
        blit = screen.blit(self.text, (self.pos[0], self.pos[1]))

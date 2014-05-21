import pygame
from gui.DebugHelper import DebugHelper


class CodeBox(pygame.sprite.Sprite):

    pos = (600,0)

    x = pos[0]                     # x of top left corner of codebox
    y = pos[1]                       # y of top left corner of codebox
    width = 200                 # width of codebox
    height = 800                # height of codebox

    top_padding = 40            # top-padding of first line of text
    left_padding = 10           # left-padding of every line of text
    line_height = 30            # height of each line of text

    rect = pygame.Rect(x, y, width, height)

    font = None
    title_font = None

    lineList = []

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("Courier New", 20)
        self.title_font = pygame.font.SysFont("Arial Bold", 30)


    def Render(self,screen):

        pygame.draw.rect(screen, (255,255,255), (self.x,self.y,self.width,self.height))
        DebugHelper.drawDebugRect(self.rect, screen)

        # Title line
        label_obj = self.title_font.render("Program text:", 1, (0, 0, 0))
        blit = screen.blit(label_obj, (self.x+self.left_padding, self.y+10))
        DebugHelper.drawDebugRect(blit, screen)

        for i in range(0, len(self.lineList)):
            line = self.lineList[i]
            label_obj = self.font.render(line, 1, (0, 0, 0))
            blit = screen.blit(label_obj, (self.x+self.left_padding, self.y+self.top_padding+i*self.line_height))
            DebugHelper.drawDebugRect(blit, screen)

    def setLineList(self, lines):
        self.lineList = lines
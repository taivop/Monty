import pygame
from gui.blocks import *
__author__ = 'Anti'
class BlockButton(pygame.sprite.Sprite):

    def __init__(self, string, x, y): # initialze the properties of the object
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font("OpenSans-Regular.ttf", 18)
        self.color = (0,0,0)
        self.borderColor = (0,0,0)
        self.text = self.font.render(string, 1, self.color)
        self.rect = self.text.get_rect()
        self.rect.width = 60
        self.rect.height = 25
        self.width = self.rect.width
        self.height = self.rect.height
        self.pos = (x,y)
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def Render(self, screen):
        screen.blit(self.text, (self.pos[0], self.pos[1]))
        pygame.draw.rect(screen, self.borderColor, self.rect, 2)

class AssignButton(BlockButton):
    def __init__(self, x, y):
        super().__init__("Assign",x ,y)

    def newBlock(self):
        return AssignBlock((self.pos[0]-210, self.pos[1]))

class PrintButton(BlockButton):
    def __init__(self, x, y):
        super().__init__("Print",x ,y)

    def newBlock(self):
        return PrintBlock((self.pos[0]-210, self.pos[1]))
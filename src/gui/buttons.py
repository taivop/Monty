import pygame
from pygame.locals import *
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
        self.rect.width = 90
        self.rect.height = 25
        self.width = self.rect.width
        self.height = self.rect.height
        self.pos = (x,y)
        self.rect.x = self.pos[0]-4
        self.rect.y = self.pos[1]
        self.block_delta_x = 150

    def Render(self, screen):
        screen.blit(self.text, (self.pos[0], self.pos[1]))
        pygame.draw.rect(screen, self.borderColor, self.rect, 2)

class AssignButton(BlockButton):
    def __init__(self, x, y):
        super().__init__("Omista",x ,y)
        self.hotkey = K_F1

    def newBlocks(self):
        return [AssignBlock((self.pos[0]-self.block_delta_x, self.pos[1]))]

class PrintButton(BlockButton):
    def __init__(self, x, y):
        super().__init__("Trüki",x ,y)
        self.hotkey = K_F2

    def newBlocks(self):
        return [PrintBlock((self.pos[0]-self.block_delta_x, self.pos[1]))]

class IfButton(BlockButton):
    def __init__(self, x, y):
        super().__init__("Tingimus", x, y)
        self.hotkey = K_F3

    def newBlocks(self):
        return [IfBlock((self.pos[0]-self.block_delta_x, self.pos[1])),
                EndIfBlock((self.pos[0]-self.block_delta_x, self.pos[1]+30))]

class WhileButton(BlockButton):
    def __init__(self, x, y):
        super().__init__("Kordus", x, y)
        self.hotkey = K_F4

    def newBlocks(self):
        return [WhileBlock((self.pos[0]-self.block_delta_x, self.pos[1])),
                EndWhileBlock((self.pos[0]-self.block_delta_x, self.pos[1]+30))]

class ForwardButton(BlockButton):
    def __init__(self, x, y):
        super().__init__("Edasi", x, y)
        self.hotkey = K_F5

    def newBlocks(self):
        return [ForwardBlock((self.pos[0]-self.block_delta_x, self.pos[1]))]

class BackButton(BlockButton):
    def __init__(self, x, y):
        super().__init__("Tagasi", x, y)
        self.hotkey = K_F6

    def newBlocks(self):
        return [BackBlock((self.pos[0]-self.block_delta_x, self.pos[1]))]

class LeftButton(BlockButton):
    def __init__(self, x, y):
        super().__init__("Vasakule", x, y)
        self.hotkey = K_F7

    def newBlocks(self):
        return [LeftBlock((self.pos[0]-self.block_delta_x, self.pos[1]))]

class RightButton(BlockButton):
    def __init__(self, x, y):
        super().__init__("Paremale", x, y)
        self.hotkey = K_F8

    def newBlocks(self):
        return [RightBlock((self.pos[0]-self.block_delta_x, self.pos[1]))]

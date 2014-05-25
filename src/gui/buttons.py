import pygame
from pygame.locals import *
from gui.blocks import *
__author__ = 'Anti'

class Button(pygame.sprite.Sprite):
    def __init__(self, string, x, y, width= 105, height=25): # initialze the properties of the object
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font("OpenSans-Regular.ttf", 18)
        self.color = (0,0,0)
        self.borderColor = (0,0,0)
        self.text = self.font.render(string, 1, self.color)
        self.rect = self.text.get_rect()
        self.rect.width = width
        self.rect.height = height
        self.width = self.rect.width
        self.height = self.rect.height
        self.pos = (x,y)
        self.rect.x = self.pos[0]-4
        self.rect.y = self.pos[1]
        self.block_delta_x = 150

    def Render(self, screen):
        screen.blit(self.text, (self.pos[0], self.pos[1]))
        pygame.draw.rect(screen, self.borderColor, self.rect, 2)

class BlockButton(Button):
    def __init__(self, string, x, y): # initialze the properties of the object
        super().__init__(string, x, y)
        self.block_delta_x = -120

class SceneButtons(Button):
    def __init__(self, x, y):
        super().__init__("Stseen 1", x, y)
        self.backup_sprites = []
        self.backup_sprites.append([])
        self.backup_sprites.append([])
        self.backup_sprites.append([])
        self.current_scene = 1

    def onClick(self, block_group):
        i = self.current_scene-1
        self.backup_sprites[i] = block_group.sprites()
        block_group.empty()
        if i == len(self.backup_sprites)-1:
            self.current_scene = 1
        else:
            self.current_scene += 1
        self.text = self.font.render("Stseen "+str(self.current_scene), 1, self.color)
        for item in self.backup_sprites[self.current_scene-1]:
            block_group.add(item)
            item.connect(block_group)

class ClearButton(Button):
    def __init__(self, string, x, y):
        super().__init__(string, x, y)

class ExitButton(Button):
    def __init__(self, string, x, y):
        super().__init__(string, x, y)


class UndoButton(Button):
    def __init__(self, string, x, y):
        super().__init__(string, x, y)
        self.backup_sprite = []
        self.backup_sprite.append([])
        self.backup_sprite.append([])
        self.backup_sprite.append([])

    def addBlock(self, block, scene):
        self.backup_sprite[scene-1].append(block)

    def undo(self,block_group, scene):
        if len(self.backup_sprite[scene-1]) > 0:
            item = self.backup_sprite[scene-1].pop()
            block_group.add(item)
            item.connect(block_group)
            return item

class SaveCodeButton(Button):
    def __init__(self, string, x, y):
        super().__init__(string, x, y)


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
class ForButton(BlockButton):
    def __init__(self, x, y):
        super().__init__("Kordus", x, y)
        self.hotkey = K_F5

    def newBlocks(self):
        return [ForBlock((self.pos[0]-self.block_delta_x, self.pos[1])),
                EndForBlock((self.pos[0]-self.block_delta_x, self.pos[1]+30))]

class FunctionButton(BlockButton):
    def __init__(self, x, y):
        super().__init__("Funktsioon", x, y)
        self.hotkey = K_F6

    def newBlocks(self):
        return [FunctionBlock((self.pos[0]-self.block_delta_x, self.pos[1])),
                EndFunctionBlock((self.pos[0]-self.block_delta_x, self.pos[1]+30))]

class EmptyButton(BlockButton):
    def __init__(self, x, y):
        super().__init__("Tühi", x, y)
        self.hotkey = K_F7

    def newBlocks(self):
        return [EmptyBlock((self.pos[0]-self.block_delta_x, self.pos[1]))]

class ForwardButton(BlockButton):
    def __init__(self, x, y):
        super().__init__("Edasi", x, y)
        self.hotkey = K_F8

    def newBlocks(self):
        return [ForwardBlock((self.pos[0]-self.block_delta_x, self.pos[1]))]

class BackButton(BlockButton):
    def __init__(self, x, y):
        super().__init__("Tagasi", x, y)
        self.hotkey = K_F9

    def newBlocks(self):
        return [BackBlock((self.pos[0]-self.block_delta_x, self.pos[1]))]

class LeftButton(BlockButton):
    def __init__(self, x, y):
        super().__init__("Vasakule", x, y)
        self.hotkey = K_F10

    def newBlocks(self):
        return [LeftBlock((self.pos[0]-self.block_delta_x, self.pos[1]))]

class RightButton(BlockButton):
    def __init__(self, x, y):
        super().__init__("Paremale", x, y)
        self.hotkey = K_F11

    def newBlocks(self):
        return [RightBlock((self.pos[0]-self.block_delta_x, self.pos[1]))]

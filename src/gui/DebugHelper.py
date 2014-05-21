
from gui.Settings import Settings
import pygame

class DebugHelper:

    @staticmethod
    def drawDebugRect(rect, screen):
        if Settings.debugging:
            pygame.draw.rect(screen, (255, 0, 0), rect, 3)
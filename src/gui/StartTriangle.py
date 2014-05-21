import pygame

class StartTriangle(pygame.sprite.Sprite):
    def __init__(self,color,top_left_pos,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.x = top_left_pos[0]
        self.y = top_left_pos[1]
        self.pos = top_left_pos
        self.height = height
        self.width = width
        self.rect = pygame.Rect(top_left_pos[0], top_left_pos[1], width, height)
        self.child = None

    def Render(self,screen):
        point_top_left = [self.x, self.y]
        point_top_right = [self.x + self.width, self.y]
        point_bottom = [self.x + self.width / 2, self.y + self.height]
        points = [point_top_left, point_top_right,point_bottom]
        pygame.draw.polygon(screen, self.color, points, 0)

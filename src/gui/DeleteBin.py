import pygame

class DeleteBin(pygame.sprite.Sprite):
    def __init__(self,top_left_pos,path):
        pygame.sprite.Sprite.__init__(self)
        self.x = top_left_pos[0]
        self.y = top_left_pos[1]
        self.pos = top_left_pos
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.rect.x , self.rect.y = top_left_pos

    def Render(self,screen):
        screen.blit(self.image,self.pos)

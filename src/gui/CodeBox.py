import pygame



class CodeBox(pygame.sprite.Sprite):

    x = 600                     # x of top left corner of codebox
    y = 0                       # y of top left corner of codebox
    width = 200                 # width of codebox
    height = 800                # height of codebox

    top_padding = 40            # top-padding of first line of text
    left_padding = 10           # left-padding of every line of text
    line_height = 30            # height of each line of text



    font = None
    title_font = None

    lineList = []

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("Courier New", 20)
        self.title_font = pygame.font.SysFont("Arial Bold", 30)


    def Render(self,screen):
        pygame.draw.rect(screen, (255,255,255), (self.x,self.y,self.width,self.height))

        # Title line
        label_obj = self.title_font.render("Program text:", 1, (0, 0, 0))
        screen.blit(label_obj, (self.x+self.left_padding, self.y+10))

        for i in range(0, len(self.lineList)):
            line = self.lineList[i]
            label_obj = self.font.render(line, 1, (0, 0, 0))
            screen.blit(label_obj, (self.x+self.left_padding, self.y+self.top_padding+i*self.line_height))

    def setLineList(self, lines):
        self.lineList = lines
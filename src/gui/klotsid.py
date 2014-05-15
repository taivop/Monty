import pygame

class Block(pygame.sprite.Sprite): # Something we can create and manipulate
    def __init__(self,color,pos,size): # initialze the properties of the object
        pygame.sprite.Sprite.__init__(self)
        self.color=color
        self.pos=pos
        self.size=size
    
    def Render(self,screen):
        blockimg = pygame.image.load("../resources/blockimg.png")
        screen.blit(blockimg,(self.pos))

def main(): # Where we start
    screen=pygame.display.set_mode((600,400))
    running=True
    RenderList=[] # list of objects
    MousePressed=False # Pressed down THIS FRAME
    MouseDown=False # mouse is held down
    MouseReleased=False # Released THIS FRAME
    Target=None # target of Drag/Drop
    while running:
        screen.fill((0,0,0)) # clear screen
        pos=pygame.mouse.get_pos()
        for Event in pygame.event.get():
            if Event.type == pygame.QUIT:
                running=False
                break # get out now
            
            if Event.type == pygame.MOUSEBUTTONDOWN:
                MousePressed=True 
                MouseDown=True 
               
            if Event.type == pygame.MOUSEBUTTONUP:
                MouseReleased=True
                MouseDown=False
             
        if MousePressed==True:
            for item in RenderList: # search all items
                if (pos[0]>=(item.pos[0]-item.size) and 
                    pos[0]<=(item.pos[0]+item.size) and 
                    pos[1]>=(item.pos[1]-item.size) and 
                    pos[1]<=(item.pos[1]+item.size) ): # inside the bounding box
                    Target=item # "pick up" item
            
            if Target is None: # didn't find any?
                Target=Block((0,0,255),pos,50) # create a new one
                RenderList.append(Target) # add to list of things to draw
            
        if MouseDown and Target is not None: # if we are dragging something
            Target.pos=pos # move the target with us
        
        if MouseReleased:
            Target=None # Drop item, if we have any
            
        for item in RenderList:
            item.Render(screen) # Draw all items
            
        MousePressed=False # Reset these to False
        MouseReleased=False # Ditto        
        pygame.display.flip()
    return # End of function
    
if __name__ == '__main__': # Are we RUNNING from this module?
    main() # Execute our main function

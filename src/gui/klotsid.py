import pygame
from gui.blocks import Block
from gui.CodeBox import CodeBox


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
        
def connectBlocks(blockone, blocktwo):
    if blockone.pos[1]<blocktwo.pos[1]:
        upperblock = blockone
        bottomblock = blocktwo
    else:
        upperblock = blocktwo
        bottomblock = blockone
        
    upperblock.child = bottomblock
    
    if isinstance(upperblock,Block):
        bottomblock.pos=upperblock.pos[0], upperblock.pos[1]+42
    else:
        print(bottomblock.pos)
        print(upperblock.pos)
        bottomblock.pos=0, upperblock.pos[1]+upperblock.height-5
        
    bottomblock.rect.x, bottomblock.rect.y = bottomblock.pos

    print("connected blocks")

def disconnectBlocks(parent, child):
    # TODO: does not work this way? (PyCharm says that the value of 'child' is not used).
    parent.child = None
    print("disconnected blocks")

def main(): # Where we start
    pygame.init()
    screen=pygame.display.set_mode((800,600))
    running=True
    MousePressed=False # Pressed down THIS FRAME
    MouseDown=False # mouse is held down
    MouseReleased=False # Released THIS FRAME
    Target=None # target of Drag/Drop
    block_group = pygame.sprite.Group()

    triangle=StartTriangle((0,255,0),[11,0], 20,9) # create a new one
    block_group.add(triangle) # add to list of things to draw

    codebox = CodeBox()
    codebox.setLineList(["foo = bar()", "print(moot)", "a line of code"])
    block_group.add(codebox)
    
    while running:
        screen.fill((0,0,0)) # clear screen
        pos=pygame.mouse.get_pos()
        events = pygame.event.get()
        for Event in events:
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
            for item in block_group: # search all items
                if item.__class__.__name__ == 'Block':
                    if (pos[0]>=(item.pos[0]-item.width) and
                        pos[0]<=(item.pos[0]+item.width) and
                        pos[1]>=(item.pos[1]-item.height) and
                        pos[1]<=(item.pos[1]+item.height) ): # inside the bounding box
                        Target=item # "pick up" item
            
            if Target is None: # didn't find any?
                Target=Block((0,0,255),pos,200,40)
                block_group.add(Target) # create a new one
                
        if MouseDown and Target is not None: # if we are dragging something
            Target.pos=pos
            Target.rect.x, Target.rect.y = pos# move the target with us

        if MouseReleased:
            Target=None # Drop item, if we have any
            for item in block_group:
                if item.__class__.__name__ == "Block":
                    for item2 in block_group:
                        if item2.__class__.__name__ == "Block":
                            if item.child == item2 and not pygame.sprite.collide_rect(item,item2):
                                disconnectBlocks(item,item2)
            
            for item in block_group:
                item.Render(screen) # Draw all items'
                for item2 in block_group:
                    if item.__class__.__name__ == "Block" and item2.__class__.__name__ == "Block":
                        if item != item2 and pygame.sprite.collide_rect(item,item2) and item.child!=item2 and item2.child!=item:
                            connectBlocks(item,item2)

        for item in block_group:
            item.Render(screen) # Draw all items
            if isinstance(item, Block):
                item.textbox.Update(events)
            
        MousePressed=False # Reset these to False
        MouseReleased=False # Ditto        
        pygame.display.flip()
    return # End of function
    
if __name__ == '__main__': # Are we RUNNING from this module?
    main() # Execute our main function

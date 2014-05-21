import pygame
import os, sys
sys.path.append(os.path.abspath(".."))

from gui.StartTriangle import StartTriangle
from gui.blocks import Block
from gui.CodeBox import CodeBox


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
    parent.child = None
    print("disconnected blocks")

def mouseIsOn(item, mouse_pos):
    """ Check if mouse (at mouse_pos) is on the item.
    """
    if (item.pos[0]) <= mouse_pos[0] <= (item.pos[0]+item.width) and\
                            (item.pos[1]+item.height) >= mouse_pos[1] >= (item.pos[1]):
        return True
    return False

def moveChildren(target, pos, i=1):
    if target.hasChild():
        target.child.pos=pos[0],pos[1]+target.height*i
        target.child.rect.x=pos[0]
        target.child.rect.y=pos[1]+target.height*i
        i+=1
        moveChildren(target.child, pos, i)

def main(): # Where we start

    pygame.init()
    screen=pygame.display.set_mode((800,600))
    running=True
    MousePressed=False # Pressed down THIS FRAME
    MouseDown=False # mouse is held down
    MouseReleased=False # Released THIS FRAME
    Target=None # target of Drag/Drop

    block_group = pygame.sprite.Group()     # group for keeping Block objects
    other_group = pygame.sprite.Group()     # group for keeping any other renderable objects

    triangle=StartTriangle((0,255,0),[11,0], 20,9) # create a new one
    other_group.add(triangle) # add to list of things to draw

    codebox = CodeBox()
    codebox.setLineList(["foo = bar()", "print(moot)", "a line of code"])
    other_group.add(codebox)
    
    while running:
        screen.fill((0,0,0)) # clear screen
        pos = pygame.mouse.get_pos()
        events = pygame.event.get()
        for Event in events:
            if Event.type == pygame.QUIT:
                running = False
                break  # get out now
            
            if Event.type == pygame.MOUSEBUTTONDOWN:
                MousePressed = True
                MouseDown = True
               
            if Event.type == pygame.MOUSEBUTTONUP:
                MouseReleased = True
                MouseDown = False
             
        if MousePressed == True:
            should_create_block = True              # do we want to create a new block?

            for item in block_group:
                if mouseIsOn(item, pos):            # inside the bounding box
                    Target=item                     # "pick up" item

            for item in other_group:
                if mouseIsOn(item, pos):            # inside the bounding box
                    should_create_block = False     # do not want to create a block

            
            if Target is None and should_create_block:  # didn't click on a block or other object
                Target=Block((0,0,255),pos,200,40)
                block_group.add(Target)                 # create a new block
                
        if MouseDown and Target is not None: # if we are dragging something
            Target.pos=pos
            Target.rect.x, Target.rect.y = pos# move the target with us
            moveChildren(Target, pos)


        if MouseReleased:
            Target=None # Drop item, if we have any
            for item in block_group:
                for item2 in block_group:
                    if item.child == item2: #and not pygame.sprite.collide_rect(item,item2):
                        disconnectBlocks(item,item2)
            
            for item in block_group:
                item.Render(screen) # Draw all items'
                for item2 in block_group:
                    if item != item2 and pygame.sprite.collide_rect(item,item2) and item.child!=item2 and item2.child!=item:
                        connectBlocks(item,item2)

        # RENDERING

        for item in block_group:
            item.Render(screen) # Draw all items
            item.textbox.Update(events)

        for item in other_group:
            item.Render(screen)

        pygame.display.flip()

        # RESETTING some values

        MousePressed = False # Reset these to False
        MouseReleased = False # Ditto
    return # End of function
    
if __name__ == '__main__': # Are we RUNNING from this module?
    main() # Execute our main function

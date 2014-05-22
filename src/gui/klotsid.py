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

    if upperblock.hasChild() or bottomblock.hasParent():
        return
    upperblock.child = bottomblock
    bottomblock.parent = upperblock

    moveChildren(upperblock,upperblock.pos)

    print("connected blocks")

def disconnectBlocks(block):
    if block.hasParent():
        block.parent.child = None
    block.parent = None
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

def connect(target, block_group, first = True):
    if first:
        for item in block_group:
            if item != target and pygame.sprite.collide_rect(item,target):
                connectBlocks(target, item)
    if target.hasChild():
        connect(target.child, block_group, False)
    else:
        for item in block_group:
            if item != target and pygame.sprite.collide_rect(item,target):
                connectBlocks(target, item)


def main(): # Where we start

    pygame.init()
    screen=pygame.display.set_mode((800,600))
    running=True
    MousePressed=False # Pressed down THIS FRAME
    MouseDown=False # mouse is held down
    MouseReleased=False # Released THIS FRAME
    Target=None # target of Drag/Drop
    targettext=None

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
        event = pygame.event.wait()
        #for Event in events:
        if event.type == pygame.QUIT:
            running = False
            break  # get out now

        if event.type == pygame.MOUSEBUTTONDOWN:
            MousePressed = True
            MouseDown = True

        if event.type == pygame.MOUSEBUTTONUP:
            MouseReleased = True
            MouseDown = False
             
        if MousePressed == True:
            should_create_block = True              # do we want to create a new block?

            for item in block_group:
                if mouseIsOn(item, pos):            # inside the bounding box
                    Target=item                     # "pick up" item
                    targettext=item.textbox


            for item in other_group:
                if mouseIsOn(item, pos):            # inside the bounding box
                    should_create_block = False     # do not want to create a block

            
            if Target is None and should_create_block:  # didn't click on a block or other object
                Target=Block((0,0,255),pos,200,40)
                block_group.add(Target)                 # create a new block
                targettext=Target.textbox

            Target.deltax=pos[0]-Target.pos[0]
            Target.deltay=pos[1]-Target.pos[1]

                
        if MouseDown and Target is not None: # if we are dragging something


            Target.pos = pos[0]-Target.deltax, pos[1]-Target.deltay
            Target.rect.x, Target.rect.y = Target.pos
            moveChildren(Target, Target.pos)


        if MouseReleased:
            disconnectBlocks(Target)
            connect(Target, block_group)
            Target=None # Drop item, if we have any

        # RENDERING

        for item in block_group:
            item.Render(screen) # Draw all items
            if targettext == item.textbox:
                item.textbox.Update(event)

        for item in other_group:
            item.Render(screen)

        pygame.display.flip()

        # RESETTING some values

        MousePressed = False # Reset these to False
        MouseReleased = False # Ditto
    return # End of function
    
if __name__ == '__main__': # Are we RUNNING from this module?
    main() # Execute our main function

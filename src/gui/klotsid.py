import pygame
from pygame.locals import *
import os, sys
sys.path.append(os.path.abspath(".."))

from gui.StartTriangle import StartTriangle
from gui.blocks import Block
from gui.CodeBox import *
from gui.buttons import *


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

def connectToStart(target,triangle): # connecting to the start triangle
    if pygame.sprite.collide_rect(target,triangle):
        if not triangle.hasChild():
            triangle.child = target
            target.parent = triangle
            target.pos = triangle.x-10, triangle.y
            target.rect.x, target.rect.y = target.pos
            print("connected to start")
            target.moveChildren()


def bringTargetToFront(target,group): # bringing the selected block and its children to front

    group.remove(target)
    group.add(target)
    if target.hasChild():
        bringTargetToFront(target.child,group)
    
def setTargettext(targettext, item,  pos):
    if targettext != None:
        targettext.borderColor = (0,0,0)
    count = len(item.elements.textboxes)
    if count != 0:
        result =  item.elements.getTextbox(pos//(int(item.width/count)))
        #eeldame, et textboxid on võrdse pikkusega, võrdsetel kaugustel
        result.borderColor = (255,255,255)
    else:
        result = None
    return result

def main(): # Where we start

    pygame.init()
    screen=pygame.display.set_mode((1000,600))
    running=True
    MousePressed=False # Pressed down THIS FRAME
    MouseDown=False # mouse is held down
    MouseReleased=False # Released THIS FRAME
    Target=None # target of Drag/Drop
    last_target=None
    targettext=None
    targetbutton=None

    block_group = pygame.sprite.LayeredUpdates()     # group for keeping Block objects (IN ORDER)
    other_group = pygame.sprite.Group()     # group for keeping any other renderable objects
    button_group = pygame.sprite.Group()

    triangle=StartTriangle((0,255,0),[10,0], 20,9) # create a new one
    other_group.add(triangle) # add to list of things to draw

    # Create run box and code box
    runbox = RunBox()
    other_group.add(runbox)

    codebox = CodeBox()
    #codebox.setLineList(["foo = bar()", "print(moot)", "a line of code"])
    other_group.add(codebox)

    runbox.codebox = codebox

    # Create run button
    runbutton = RunButton()

    button_x = 600
    assignButton = AssignButton(button_x, 40)
    printButton = PrintButton(button_x, 70)
    ifButton = IfButton(button_x, 100)
    whileButton = WhileButton(button_x, 130)

    forwardButton = ForwardButton(button_x, 200)
    backButton = BackButton(button_x, 230)
    leftButton = LeftButton(button_x, 260)
    rightButton = RightButton(button_x, 290)

    button_group.add(assignButton)
    button_group.add(printButton)
    button_group.add(forwardButton)
    button_group.add(leftButton)
    button_group.add(rightButton)
    button_group.add(ifButton)
    button_group.add(whileButton)
    button_group.add(backButton)

    while running:
        
        screen.fill((245,245,245)) # clear screen
        pos = pygame.mouse.get_pos()
        event = pygame.event.wait()

        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
            pygame.quit()
            break  # get out now

        if event.type == pygame.MOUSEBUTTONDOWN:
            MousePressed = True
            MouseDown = True

        if event.type == pygame.MOUSEBUTTONUP:
            MouseReleased = True
            MouseDown = False
             
        if MousePressed == True:

            for item in block_group:
                if mouseIsOn(item, pos):            # inside the bounding box
                    Target=item                     # "pick up" item
                    if targettext != None:
                        targettext.borderColor = (0,0,0)
                    targettext = setTargettext(targettext, item, (pos[0]-item.pos[0]))


            #for item in other_group:
            #    if mouseIsOn(item, pos):            # inside the bounding box


            for item in button_group:
                if mouseIsOn(item, pos):
                    targetbutton = item
                    break

            # if run button was pressed:
            if mouseIsOn(runbutton, pos):
                runbox.updateRunResult()

            
            if Target is None and targetbutton != None:  # didn't click on a block or other object
                new_blocks=targetbutton.newBlocks()
                for item in new_blocks:
                    block_group.add(item)
                    item.connect(new_blocks)
                Target = new_blocks[0]
                targetbutton = None
                targettext = setTargettext(targettext, Target, 0)



            if Target is not None:
                Target.deltax=pos[0]-Target.pos[0]
                Target.deltay=pos[1]-Target.pos[1]

                
        if MouseDown and Target is not None: # if we are dragging something


            Target.pos = pos[0]-Target.deltax, pos[1]-Target.deltay
            Target.rect.x, Target.rect.y = Target.pos
            Target.moveChildren()
            bringTargetToFront(Target,block_group) # the blocks on the move are always on top


        if MouseReleased and Target is not None:
            disconnectBlocks(Target)
            Target.connect(block_group)
            connectToStart(Target, triangle)
            codebox.update(triangle)
            last_target = Target
            Target=None # Drop item, if we have any


        if event.type == KEYDOWN:
            if event.key == K_DELETE:
                if last_target != None:
                    disconnectBlocks(last_target)
                    last_target.remove(block_group)
                    codebox.update(triangle)
            if event.key == K_RETURN:
                runbox.updateRunResult()


        # RENDERING

        for item in block_group:
            item.Render(screen) # Draw all items
            for i in range(len(item.elements.textboxes)):
                box = item.elements.getTextbox(i)
                if targettext == box:
                    box.Update(event)
                    break


        for item in other_group:
            item.Render(screen)

        for item in button_group:
            item.Render(screen)

        runbutton.Render(screen)
            
        pygame.display.flip()

        # RESETTING some values

        MousePressed = False # Reset these to False
        MouseReleased = False # Ditto
    return # End of function
    
if __name__ == '__main__': # Are we RUNNING from this module?
    main() # Execute our main function

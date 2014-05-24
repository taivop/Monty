import pygame
from pygame.locals import *
import os, sys
sys.path.append(os.path.abspath(".."))

from gui.StartTriangle import StartTriangle
from gui.blocks import Block
from gui.CodeBox import *
from gui.buttons import *


def disconnectParent(block):
    if block.hasParent():
        block.parent.child = None
        block.parent = None
    print("disconnected blocks")

def disconnectChild(block):
    if block.hasChild():
        block.child.parent = None
        block.child = None
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
        if result != None:
            result.borderColor = (255,255,255)
    else:
        result = None
    return result

def newBlocks(targetbutton, block_group, targettext):
    new_blocks=targetbutton.newBlocks()
    for item in new_blocks:
        block_group.add(item)
        item.connect(new_blocks)
    return new_blocks[0], None, setTargettext(targettext, new_blocks[0], 0)


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
    target_block_button=None
    backup_sprites=[]

    block_group = pygame.sprite.LayeredUpdates()     # group for keeping Block objects (IN ORDER)
    other_group = pygame.sprite.Group()     # group for keeping any other renderable objects
    block_button_group = pygame.sprite.Group()
    other_button_group = pygame.sprite.Group()

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
    button_x = 600

    runbutton = RunButton()
    hidebutton = HideButton(button_x, 390)
    exitbutton = ExitButton("Välju", button_x, 450)
    savecodebutton = SaveCodeButton("Salvesta", button_x, 360)
    undobutton = UndoButton("Tagasi", button_x, 420)

    other_button_group.add(hidebutton)
    other_button_group.add(exitbutton)
    other_button_group.add(runbutton)
    other_button_group.add(savecodebutton)
    other_button_group.add(undobutton)


    assignButton = AssignButton(button_x, 40)
    printButton = PrintButton(button_x, 70)
    ifButton = IfButton(button_x, 100)
    whileButton = WhileButton(button_x, 130)

    forwardButton = ForwardButton(button_x, 200)
    backButton = BackButton(button_x, 230)
    leftButton = LeftButton(button_x, 260)
    rightButton = RightButton(button_x, 290)

    block_button_group.add(assignButton)
    block_button_group.add(printButton)
    block_button_group.add(forwardButton)
    block_button_group.add(leftButton)
    block_button_group.add(rightButton)
    block_button_group.add(ifButton)
    block_button_group.add(whileButton)
    block_button_group.add(backButton)

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
                    targettext = setTargettext(targettext, item, (pos[0]-item.pos[0]))


            #for item in other_group:
            #    if mouseIsOn(item, pos):            # inside the bounding box


            for item in block_button_group:
                if mouseIsOn(item, pos):
                    target_block_button = item
                    break

            if mouseIsOn(hidebutton, pos):
                if not hidebutton.hidden:
                    hidebutton.hide(block_group)
                    disconnectChild(triangle)
                else:
                    hidebutton.show(block_group, connectToStart, triangle)
                codebox.update(triangle)
            elif mouseIsOn(exitbutton, pos):
                pygame.quit()
                break
            elif mouseIsOn(savecodebutton, pos):
                f=open("fail.py", 'w')
                f.write(runbox.getProgramText())
                f.close()
            elif mouseIsOn(undobutton, pos):
                item = undobutton.undo(block_group)
                if item != None:
                    connectToStart(item, triangle)
                    if last_target == None:
                        last_target = item
                    codebox.update(triangle)

            # if run button was pressed:
            elif mouseIsOn(runbutton, pos):
                runbox.updateRunResult()

            
            if Target is None and target_block_button != None:  # didn't click on a block or other object
                Target, target_block_button, targettext = newBlocks(target_block_button, block_group, targettext)


            if Target is not None:
                Target.deltax=pos[0]-Target.pos[0]
                Target.deltay=pos[1]-Target.pos[1]

        if event.type == KEYDOWN:
            if event.key == K_DELETE:
                if last_target != None:
                    disconnectParent(last_target)
                    disconnectChild(last_target)
                    last_target.kill()
                    undobutton.addBlock(last_target)
                    last_target = None
                    codebox.update(triangle)
            if event.key == K_RETURN:
                runbox.updateRunResult()
            if event.key == K_TAB:
                if targettext != None and last_target != None:
                    targettext.borderColor = (0,0,0)
                    prev = targettext
                    targettext, last_target = last_target.changeTextbox(targettext)
                    if targettext == None:
                        targettext = prev
                    targettext.borderColor = (255,255,255)
            for item in block_button_group:
                if item.hotkey == event.key:
                    target_block_button = item
                    Target, target_block_button, targettext = newBlocks(target_block_button, block_group, targettext)
                    MouseReleased = True
                    break

        if MouseDown and Target is not None: # if we are dragging something


            Target.pos = pos[0]-Target.deltax, pos[1]-Target.deltay
            Target.rect.x, Target.rect.y = Target.pos
            Target.moveChildren()
            bringTargetToFront(Target,block_group) # the blocks on the move are always on top


        if MouseReleased and Target is not None:
            disconnectParent(Target)
            Target.connect(block_group)
            connectToStart(Target, triangle)
            codebox.update(triangle)
            last_target = Target
            Target=None # Drop item, if we have any


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

        for item in block_button_group:
            item.Render(screen)

        for item in other_button_group:
            item.Render(screen)
            
        pygame.display.flip()

        # RESETTING some values

        MousePressed = False # Reset these to False
        MouseReleased = False # Ditto
    return # End of function
    
if __name__ == '__main__': # Are we RUNNING from this module?
    main() # Execute our main function

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

def disconnectChild(block):
    if block.hasChild():
        block.child.parent = None
        block.child = None

def mouseIsOn(item, mouse_pos):
    """ Check if mouse (at mouse_pos) is on the item.
    """
    if (item.pos[0]) <= mouse_pos[0] <= (item.pos[0]+item.width) and\
                            (item.pos[1]+item.height) >= mouse_pos[1] >= (item.pos[1]):
        return True
    return False


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

def removeAll(group):
    for item in group:
        item.kill()
        if isinstance(item, Block):
            disconnectChild(item)
            disconnectParent(item)
    group.empty()

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

    block_group = pygame.sprite.LayeredUpdates()     # group for keeping Block objects (IN ORDER)
    other_group = pygame.sprite.Group()     # group for keeping any other renderable objects
    block_button_group = pygame.sprite.Group()
    other_button_group = pygame.sprite.Group()
    triangle_group = pygame.sprite.Group()

    triangle=StartTriangle((0,255,0),[10,0], 20,9) # create a new one
    triangle2 = StartTriangle((255,0,0),[300,0], 20,9)
    triangle_group.add(triangle) # add to list of things to draw
    triangle_group.add(triangle2)

    # Create run box and code box
    runbox = RunBox()
    other_group.add(runbox)

    codebox = CodeBox()
    #codebox.setLineList(["foo = bar()", "print(moot)", "a line of code"])
    other_group.add(codebox)

    runbox.codebox = codebox

    # Create run button
    button_x = 595
    first_y = 10
    delta_y = 30
    between_group = 30

    runbutton = RunButton()
    clearbutton = ClearButton       ("Puhasta", button_x, first_y+13*delta_y+2*between_group)
    exitbutton = ExitButton         ("Välju",   button_x, first_y+14*delta_y+2*between_group)
    savecodebutton = SaveCodeButton ("Salvesta",button_x, first_y+10*delta_y+2*between_group)
    undobutton = UndoButton         ("Tagasi",  button_x, first_y+12*delta_y+2*between_group)
    scenebutton = SceneButtons      (           button_x, first_y+11*delta_y+2*between_group)

    other_button_group.add(clearbutton)
    other_button_group.add(exitbutton)
    other_button_group.add(runbutton)
    other_button_group.add(savecodebutton)
    other_button_group.add(undobutton)
    other_button_group.add(scenebutton)


    assignButton = AssignButton(button_x, first_y)
    printButton = PrintButton(button_x, first_y+1*delta_y)
    ifButton = IfButton(button_x, first_y+2*delta_y)
    whileButton = WhileButton(button_x, first_y+3*delta_y)
    functionbutton = FunctionButton(button_x, first_y+4*delta_y)
    emptybutton = EmptyButton(button_x, first_y+5*delta_y)

    forwardButton = ForwardButton(button_x, first_y+7*delta_y+1*between_group)
    backButton = BackButton(button_x, first_y+6*delta_y+1*between_group)
    leftButton = LeftButton(button_x, first_y+8*delta_y+1*between_group)
    rightButton = RightButton(button_x, first_y+9*delta_y+1*between_group)

    block_button_group.add(assignButton)
    block_button_group.add(printButton)
    block_button_group.add(forwardButton)
    block_button_group.add(leftButton)
    block_button_group.add(rightButton)
    block_button_group.add(ifButton)
    block_button_group.add(whileButton)
    block_button_group.add(backButton)
    block_button_group.add(functionbutton)
    block_button_group.add(emptybutton)

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

            # Other button "listeners"

            if mouseIsOn(clearbutton, pos):
                removeAll(block_group)
                removeAll(other_button_group)
                removeAll(block_button_group)
                removeAll(other_group)
                return True
            elif mouseIsOn(scenebutton, pos):
                scenebutton.onClick(block_group)
                for triangle in triangle_group:
                    disconnectChild(triangle)
                    for item in block_group:
                        if triangle.connect(item):
                            break
                codebox.update(triangle_group)
            elif mouseIsOn(exitbutton, pos):
                pygame.quit()
                break
            elif mouseIsOn(savecodebutton, pos):
                text = runbox.getProgramText()
                if text != '':
                    f=open("stseen"+str(scenebutton.current_scene)+".py", 'w')
                    f.write(text)
                    f.close()
            elif mouseIsOn(undobutton, pos):
                item = undobutton.undo(block_group, scenebutton.current_scene)
                if item != None:
                    for triangle in triangle_group:
                        triangle.connect(item)
                        if last_target == None:
                            last_target = item
                    codebox.update(triangle_group)
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
                    undobutton.addBlock(last_target, scenebutton.current_scene)
                    last_target = None
                    codebox.update(triangle_group)
            if event.key == K_RETURN:
                runbox.updateRunResult()
            if event.key == K_TAB:
                if targettext != None:
                    targettext.borderColor = (0,0,0)
                prev_text = targettext
                prev_block = last_target
                if last_target != None:
                    targettext, last_target = last_target.changeTextbox(targettext)
                else:
                    last_target = block_group.sprites()[0]
                if targettext == None:
                    targettext = prev_text
                else:
                    targettext.borderColor = (255,255,255)
                if last_target == None:
                    last_target=prev_block
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
            for triangle in triangle_group:
                triangle.connect(Target)
            codebox.update(triangle_group)
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

        for item in triangle_group:
            item.Render(screen)
            
        pygame.display.flip()

        # RESETTING some values

        MousePressed = False # Reset these to False
        MouseReleased = False # Ditto
    return False # End of function
    
if __name__ == '__main__': # Are we RUNNING from this module?
    running = True
    while running:
        running = main() # Execute our main function

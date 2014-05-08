import pygame

# Example script from: https://programmeerimine.cs.ut.ee/pygame.html

pygame.init()

ekraani_pind = pygame.display.set_mode( (800, 600) )
pygame.display.set_caption("Minu esimene aken")
ekraani_pind.fill( (0,255,0) )

ristkylik1 = pygame.Rect(100,0,100,100)
pygame.draw.rect(ekraani_pind, (255,0,0), ristkylik1)
pygame.display.flip()

while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
pygame.quit()
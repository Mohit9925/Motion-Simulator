import pygame 

def cursor_loader(screen,image):
    
    pygame.mouse.set_visible(False)
    
    screen.blit(pygame.image.load('./image/cursor/cirlce.png'),pygame.mouse.get_pos())

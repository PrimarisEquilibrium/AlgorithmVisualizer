import pygame

# pygame setup
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

running = True
while running:
    # Allows the window to be closed on QUIT ("X" at top right of the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Displays contents onto screen
    pygame.display.update()
    
    # Sets the FPS of the window to 60
    clock.tick(60)

pygame.quit()
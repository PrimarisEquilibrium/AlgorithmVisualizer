import pygame
import pygame_textinput

from cell import CellArray
from algorithms import BinarySearch
from colors import colors

# pygame setup
pygame.init()
pygame.display.set_caption("Kevin's Algorithm Visualizer")

# Screen settings
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800

# pygame Handlers
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

my_cell_array = CellArray(screen, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
my_binary_search = BinarySearch(my_cell_array, 3)

my_text_input = pygame_textinput.TextInputVisualizer(
    font_color=colors.PRIMARY_COLOR, cursor_color=colors.PRIMARY_COLOR
)

def init() -> None:
    my_time = pygame.time.get_ticks()
    interval = 500
    running = True

    while running:
        screen.fill(colors.BACKGROUND_COLOR)

        my_binary_search.render()
        current_time = pygame.time.get_ticks()
        if current_time - my_time >= interval:
            screen.fill(colors.BACKGROUND_COLOR)
            my_time = current_time
            my_binary_search.render()
            my_binary_search.search_step()

        events = pygame.event.get()
        my_text_input.update(events)
        screen.blit(my_text_input.surface, (50, 50))

        # Allows the window to be closed on QUIT ("X"  at top right of the window)
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # Displays contents onto screen
        pygame.display.update()

        # Sets the FPS of the window to 60
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
   init()
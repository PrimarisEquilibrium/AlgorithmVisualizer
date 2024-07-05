import pygame
import pygame_textinput

from cell import CellArray, font
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
    font_color=colors.PRIMARY_COLOR, cursor_color=colors.PRIMARY_COLOR, font_object=font
)

def init() -> None:
    binary_search_array = None

    my_time = pygame.time.get_ticks()
    interval = 500
    running = True

    while running:
        screen.fill(colors.BACKGROUND_COLOR)

        events = pygame.event.get()
        my_text_input.update(events)
        screen.blit(my_text_input.surface, (50, 50))

        if binary_search_array:
            binary_search_array.render()
            current_time = pygame.time.get_ticks()
            if current_time - my_time >= interval:
                my_time = current_time
                binary_search_array.render()
                binary_search_array.search_step()

        for event in events:
            # Allows the window to be closed on QUIT ("X" at top right of the window)
            if event.type == pygame.QUIT:
                running = False

            # Handle input text submission
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Get user input
                # Valid format is: "1, 2, ..., n" (seperated by commas)
                user_input = my_text_input.value
                try:
                    # String cleaning
                    user_array = ''.join(user_input.split())
                    user_array = user_array.split(",")
                    
                    # Converts each string number into an integer
                    user_array = list(map(lambda x : int(x), user_array))

                    cell_array = CellArray(screen, user_array)
                    binary_search_array = BinarySearch(cell_array, 5)
                except ValueError:
                    print("Invalid input")
                
                # Clear textbox
                my_text_input.value = ""
                my_text_input.update(events)

        # Displays contents onto screen
        pygame.display.update()

        # Sets the FPS of the window to 60
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
   init()
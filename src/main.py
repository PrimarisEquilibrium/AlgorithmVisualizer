import pygame

from cell import CellArray
from algorithms import BinarySearch
from config import colors
from widgets import InputBox, Button


# pygame setup
pygame.init()
pygame.display.set_caption("Kevin's Algorithm Visualizer")

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# pygame Handlers
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

    
def cell_array_init(user_input):
    try:
        # String cleaning
        user_array = ''.join(user_input.split())
        user_array = user_array.split(",")
        
        # Converts each string number into an integer
        user_array = list(map(lambda x : int(x), user_array))

        cell_array = CellArray(screen, user_array)
        return cell_array
    except ValueError:
        print("Invalid input")


input_box = InputBox(screen, "Array to search (seperated by commas)", 35, 60, 500, 50, 30)
val_box = InputBox(screen, "Value to find", 35, 160, 500, 50)

def get_input_data():
    cell_array = cell_array_init(input_box.get_value())
    val = int(val_box.get_value())
    return cell_array, val

submit_btn = Button(screen, "Submit", 35, 240, 125, 60, get_input_data)

def init() -> None:
    binary_search_array: BinarySearch = None

    my_time = pygame.time.get_ticks()
    interval = 500
    running = True

    display_input = True
    while running:
        screen.fill(colors.BACKGROUND_COLOR)

        events = pygame.event.get()
        if (display_input):
            input_box.draw(events)
            val_box.draw(events)
            submit_btn.draw()

        if binary_search_array:
            binary_search_array.draw(screen)
            current_time = pygame.time.get_ticks()
            if current_time - my_time >= interval:
                my_time = current_time
                binary_search_array.draw(screen)
                binary_search_array.search_step()

        for event in events:
            # Allows the window to be closed on QUIT ("X" at top right of the window)
            if event.type == pygame.QUIT:
                running = False
            
            # Handles left mouse press
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if submit_btn.is_mouse_over(mouse_x, mouse_y):
                    cell_array, val = submit_btn.on_click()
                    binary_search_array = BinarySearch(cell_array, val, 50, 140)
                    display_input = False

                input_box.handle_focus(events, mouse_x, mouse_y)
                val_box.handle_focus(events, mouse_x, mouse_y)

        # Displays contents onto screen
        pygame.display.update()

        # Sets the FPS of the window to 60
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
   init()
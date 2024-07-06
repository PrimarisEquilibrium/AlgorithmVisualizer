import pygame

from cell import CellArray
from algorithms import BinarySearch
from colors import colors
from widgets import InputBox, Button

# pygame setup
pygame.init()
pygame.display.set_caption("Kevin's Algorithm Visualizer")

# Screen settings
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800

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


input_box = InputBox("Array to search (seperated by commas)", 200, 200, 500, 50)
val_box = InputBox("Value to find", 200, 300, 500, 50)

def get_input_data():
    cell_array = cell_array_init(input_box.get_value())
    val = int(val_box.get_value())
    return BinarySearch(cell_array, val, 0, 0)

submit_btn = Button("Submit", 200, 400, 150, 75, get_input_data)

def init() -> None:
    binary_search_array = None

    my_time = pygame.time.get_ticks()
    interval = 500
    running = True

    while running:
        screen.fill(colors.BACKGROUND_COLOR)

        events = pygame.event.get()
        input_box.draw(screen, events)
        val_box.draw(screen, events)
        submit_btn.draw(screen)

        if binary_search_array:
            binary_search_array.draw()
            current_time = pygame.time.get_ticks()
            if current_time - my_time >= interval:
                my_time = current_time
                binary_search_array.draw()
                binary_search_array.search_step()

        for event in events:
            # Allows the window to be closed on QUIT ("X" at top right of the window)
            if event.type == pygame.QUIT:
                running = False
            
            # Handles input box focus
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if submit_btn.is_mouse_over(mouse_x, mouse_y):
                    binary_search_array = submit_btn.on_click()

                if (input_box.cursor_in_textbox(mouse_x, mouse_y)):
                    input_box.toggle_focus(events)
                else:
                    input_box.is_focused = False

                if (val_box.cursor_in_textbox(mouse_x, mouse_y)):
                    val_box.toggle_focus(events)
                else:
                    val_box.is_focused = False

            # Handle input text submission
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                print(input_box.get_value())

        # Displays contents onto screen
        pygame.display.update()

        # Sets the FPS of the window to 60
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
   init()
import pygame
import pygame_textinput
from typing import Callable, Any

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

class InputBox:
    def __init__(self, label: str, x: int, y: int, width: int, height: int, max_length: int = 20) -> None:
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_length = max_length

        # Base pygame text input module
        self.manager = pygame_textinput.TextInputManager(validator = lambda input : len(input) <= max_length)
        self.textinput = pygame_textinput.TextInputVisualizer(
            manager=self.manager,
            font_color=colors.PRIMARY_COLOR, 
            cursor_color=colors.PRIMARY_COLOR, 
            font_object=font,
            cursor_width=0
        )
        self._text_box = pygame.Rect(x, y, width, height)
        self.is_focused = False
    
    def draw(self, events: list[pygame.event.Event]) -> None:
        # Draw input box label
        text = font.render(f"{self.label}", True, colors.SELECTED_COLOR)
        screen.blit(text, (self.x, self.y - 35))

        # Draw box around text input
        pygame.draw.rect(screen, colors.BACKGROUND_COLOR, self._text_box)
        pygame.draw.rect(screen, colors.PRIMARY_COLOR, self._text_box, 5)

        # Draw the text input
        if (self.is_focused):
            # Only update the text input if it is in focus
            self.textinput.update(events)
        _, text_height = self.textinput.surface.get_size()
        padding = (self.height - text_height) // 2
        screen.blit(self.textinput.surface, (self.x + padding, self.y + padding))
    
    def cursor_in_textbox(self, mouse_x: int, mouse_y: int) -> None:
        """ Returns true if the cursor is located inside the text_box rect """
        if (mouse_x >= self.x and mouse_y >= self.y and
            mouse_x <= self.x + self.width and mouse_y <= self.y + self.height):
            return True
        return False
        
    def toggle_focus(self, events: list[pygame.event.Event]) -> None:
        # Toggle is_focused variable and cursor
        if (not self.is_focused):
            self.textinput.cursor_width = 4
            self.is_focused = True
        else:
            self.textinput.cursor_width = 0
            self.is_focused = False
        self.textinput.update(events)
    
    def handle_submission(self, function: Callable[[str], Any], events: list[pygame.event.Event]) -> None:
        if (self.is_focused):
            # Get user input
            # Valid format is: "1, 2, ..., n" (seperated by commas)
            user_input = self.textinput.value

            # Clear textbox
            input_box.textinput.value = ""
            input_box.textinput.update(events)

            return function(user_input)
            

input_box = InputBox("Array to search (seperated by commas)", 200, 200, 500, 50)
val_box = InputBox("Value to find", 200, 300, 500, 50)

def cell_array_init(user_input):
    try:
        # String cleaning
        user_array = ''.join(user_input.split())
        user_array = user_array.split(",")
        
        # Converts each string number into an integer
        user_array = list(map(lambda x : int(x), user_array))

        print("yes")

        cell_array = CellArray(screen, user_array)
        return cell_array
    except ValueError:
        print("Invalid input")

def init() -> None:
    binary_search_array = None

    my_time = pygame.time.get_ticks()
    interval = 500
    running = True

    while running:
        screen.fill(colors.BACKGROUND_COLOR)

        events = pygame.event.get()
        input_box.draw(events)

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
                if (input_box.cursor_in_textbox(mouse_x, mouse_y)):
                    input_box.toggle_focus(events)
                else:
                    input_box.is_focused = False

            # Handle input text submission
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                cell_array = input_box.handle_submission(cell_array_init, events)
                print(cell_array)

        # Displays contents onto screen
        pygame.display.update()

        # Sets the FPS of the window to 60
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
   init()
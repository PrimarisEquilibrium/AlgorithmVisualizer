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

class InputBox:
    def __init__(self, label: str, x: int, y: int, width: int, height: int, max_length: int = 20) -> None:
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_length = max_length

        self.manager = pygame_textinput.TextInputManager(validator = lambda input : len(input) <= max_length)
        self.textinput = pygame_textinput.TextInputVisualizer(
            manager=self.manager,
            font_color=colors.PRIMARY_COLOR, 
            cursor_color=colors.PRIMARY_COLOR, 
            font_object=font
        )
        self._text_box = pygame.Rect(x, y, width, height)
    
    def draw(self, events: list[pygame.event.Event]):
        text = font.render(f"{self.label}", True, colors.SELECTED_COLOR)
        screen.blit(text, (self.x, self.y - 35))
        pygame.draw.rect(screen, colors.BACKGROUND_COLOR, self._text_box)
        pygame.draw.rect(screen, colors.PRIMARY_COLOR, self._text_box, 5)
        self.textinput.update(events)
        _, text_height = self.textinput.surface.get_size()
        padding = (self.height - text_height) // 2
        screen.blit(self.textinput.surface, (self.x + padding, self.y + padding))

input_box = InputBox("Array to search (seperated by commas)", 200, 200, 500, 50)
val_box = InputBox("Value to find", 200, 300, 500, 50)

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

            # Handle input text submission
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Get user input
                # Valid format is: "1, 2, ..., n" (seperated by commas)
                user_input = input_box.textinput.value
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
                input_box.textinput.value = ""
                input_box.textinput.update(events)

        # Displays contents onto screen
        pygame.display.update()

        # Sets the FPS of the window to 60
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
   init()
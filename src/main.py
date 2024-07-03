import pygame
from typing import Optional

from cell import Cell, CellArray
from colors import colors


# pygame setup
pygame.init()
pygame.font.init()
pygame.display.set_caption("Kevin's Algorithm Visualizer")

# Screen settings
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800

# Array cell properties
rect_size = 50
border = 5

# pygame Handlers
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font("fonts/Roboto-Regular.ttf", rect_size // 2)
clock = pygame.time.Clock()


class BinarySearch:
    def __init__(self, cell_array_obj: CellArray, val: int, x: int = 0, y: int = 0):
        self.cell_array_obj = cell_array_obj
        self.val = val
        self.x = x
        self.y = y
        self.cell_array = cell_array_obj.array
        self.start, self.end = self.initialize_cell_array()

    def draw(self) -> None:
        draw_cell_array(self.cell_array, self.x, self.y)

    def initialize_cell_array(self) -> tuple[int, int]:
        self.draw()
        # Pointers to array search area
        start = 0
        end = len(self.cell_array) - 1 # len(<list>) is a constant time operation
        return start, end

    def get_guess(self) -> tuple[int, int]:
        mid = (self.start + self.end) // 2
        guess = self.cell_array[mid]
        self.cell_array_obj.set_selected(mid)
        return mid, guess

    def compare_guess(self, mid: int, guess: Cell) -> Optional[int]:
        guess_val = guess.value

        # If guess is correct return index in the array
        if guess_val == self.val:
            self.cell_array_obj.set_inactive(self.start, mid - 1)
            self.cell_array_obj.set_inactive(mid + 1, self.end)
            return mid
        # If guess is smaller than value the value is in the larger half of the array
        elif guess_val < self.val:
            self.cell_array_obj.set_inactive(self.start, mid)
            self.start = mid + 1
        # If guess is larger than value the value is in the smaller half of the array
        else:
            self.cell_array_obj.set_inactive(mid, self.end)
            self.end = mid - 1
        
        return None
    
    def search(self) -> None:
        self.draw()
        self.initialize_cell_array()
        mid, guess = self.get_guess()
        self.compare_guess(mid, guess)


def draw_cell(cell: Cell, x: int, y: int) -> None:
    """
    Draws a single cell with its label and visual state.

    :param cell: Cell object.
    :param x: X-Position of cell.
    :param y: Y-Position of cell.
    """

    value = cell.value
    color = cell.get_color()
    
    # Create Rect object
    rect = pygame.Rect(x, y, rect_size, rect_size)
    
    # Draw cell and border
    pygame.draw.rect(screen, colors.BACKGROUND_COLOR, rect)
    pygame.draw.rect(screen, color, rect, border)

    # Render text in cell
    text = font.render(f"{value}", True, color)
    padding = rect_size / 2
    text_x = x + padding
    text_y = y + padding
    text_rect = text.get_rect(center=(text_x, text_y))
    screen.blit(text, text_rect)


def draw_cell_array(cell_array: CellArray, x_offset: int, y_offset: int) -> None:
    """
    Draws a horizontal sequence of cells, where each cell corresponds to an element in the given cell array.

    :param cell_array: Cell array to draw.
    :param x_offset: X-Offset from top left corner of screen.
    :param y_offset: Y-Offset from top left corner of screen.
    """

    for i, cell in enumerate(cell_array):
        # Position of cell
        x = x_offset + (i * rect_size)
        y = y_offset + 0

        draw_cell(cell, x, y)


my_cell_array = CellArray(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20)
my_binary_search = BinarySearch(my_cell_array, 19)

def init() -> None:
    running = True
    while running:
        # Allows the window to be closed on QUIT ("X" at top right of the window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(colors.BACKGROUND_COLOR)

        my_binary_search.search()

        # Displays contents onto screen
        pygame.display.update()

        # Sets the FPS of the window to 60
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
   init()
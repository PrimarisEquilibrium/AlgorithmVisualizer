import pygame
from typing import Optional
from enum import Enum


# pygame setup
pygame.init()
pygame.font.init()
pygame.display.set_caption("Kevin's Algorithm Visualizer")
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font("fonts/Roboto-Regular.ttf", 25)
clock = pygame.time.Clock()

PRIMARY_COLOR = "#151515"
SECONDARY_COLOR = "#a6a6a6"
INACTIVE_COLOR = "#454545"
SELECTED_COLOR = "#ffffff"


# Enumeration containing all the states a cell could be in
class CellState(Enum):
    ACTIVE = 1
    INACTIVE = 2
    SELECTED = 3

# A Cell class containing a value and visual state
class Cell:
    def __init__(self, value, state=CellState.ACTIVE):
        self.value = value
        self.state = state

    def __str__(self):
        return f"Cell({self.value}, {self.state.name})"

    def set_active(self):
        self.state = CellState.ACTIVE
    
    def set_inactive(self):
        self.state = CellState.INACTIVE
    
    def set_selected(self):
        self.state = CellState.SELECTED
    
    def get_color(self):
        match self.state:
            case CellState.ACTIVE:
                return SECONDARY_COLOR
            case CellState.INACTIVE:
                return INACTIVE_COLOR
            case _:
                return SELECTED_COLOR

# CellArray class with methods to operate on all cells
class CellArray():
    def __init__(self, *args):
        self.array = self.make_cell_array(*args)

    def __str__(self):
        return "[" + ", ".join(str(cell) for cell in self.array) + "]"
    
    def __len__(self):
        return len(self.array)
    
    def make_cell_array(self, *args):
        # Create a Cell object for each element in the array
        return [Cell(arg) for arg in args]

    def set_active(self, start, end=None):
        if end is None:
            # Single index case
            index = start
            self.array[index].set_active()
        else:
            # Range case
            for i in range(start, end + 1):
                self.array[i].set_active()

    def set_inactive(self, start, end=None):
        if end is None:
            # Single index case
            index = start
            self.array[index].set_inactive()
        else:
            # Range case
            for i in range(start, end + 1):
                self.array[i].set_inactive()

    def set_selected(self, index):
        self.array[index].set_selected()

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

# Array cell properties
rect_size = 75
border = 5
def draw_cell(cell, x, y):
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
    pygame.draw.rect(screen, PRIMARY_COLOR, rect)
    pygame.draw.rect(screen, color, rect, border)

    # Render text in cell
    text = font.render(f"{value}", True, color)
    padding = rect_size / 2
    text_x = x + padding
    text_y = y + padding
    text_rect = text.get_rect(center=(text_x, text_y))
    screen.blit(text, text_rect)

def draw_cell_array(cell_array, x_offset, y_offset):
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

my_cell_array = CellArray(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
my_binary_search = BinarySearch(my_cell_array, 8)

def init():
    running = True
    while running:
        # Allows the window to be closed on QUIT ("X" at top right of the window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill("#151515")

        my_binary_search.draw()
        my_binary_search.initialize_cell_array()
        mid, guess = my_binary_search.get_guess()
        my_binary_search.compare_guess(mid, guess)

        # Displays contents onto screen
        pygame.display.update()

        # Sets the FPS of the window to 60
        clock.tick(1)

    pygame.quit()

if __name__ == "__main__":
    init()
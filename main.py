import pygame
from enum import Enum


# pygame setup
pygame.init()
pygame.font.init()
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
class Cell():
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


def binary_search(arr, val):
    """
    Returns the index of a given value in a sorted array.
    
    :param arr: Cell array to search.
    :param val: The value to search for.
    :return: The index of the value or False if it was not found.
    """

    # Pointers to array search area
    start = 0
    end = len(arr) - 1 # len(<list>) is a constant time operation
    while end >= start:
        mid = (start + end) // 2
        guess = arr[mid]
        print(f"Start: {start}, End: {end}, Mid: {mid}, Guess: {guess}")
        # If guess is correct return index in the array
        if guess == val:
            print(f"Result found: {guess} at index [{mid}]")
            return mid
        # If guess is smaller than value the value is in the larger half of the array
        elif guess < val:
            start = mid + 1
        # If guess is larger than value the value is in the smaller half of the array
        else:
            end = mid - 1
    print("Result not found")
    return False

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


def init():
    running = True
    while running:
        # Allows the window to be closed on QUIT ("X" at top right of the window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill("#151515")

        # Displays contents onto screen
        pygame.display.update()
        
        # Sets the FPS of the window to 60
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    init()
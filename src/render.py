import pygame

from cell import Cell, CellArray
from colors import colors

# Array cell properties
rect_size = 50
border = 5

pygame.font.init()
font = pygame.font.Font("fonts/Roboto-Regular.ttf", rect_size // 2)


def draw_cell(screen: pygame.Surface, cell: Cell, x: int, y: int) -> None:
    """
    Draws a single cell with its label and visual state.

    :param screen: The pygame screen
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


def draw_cell_array(screen: pygame.Surface, cell_array: CellArray, x_offset: int, y_offset: int) -> None:
    """
    Draws a horizontal sequence of cells, where each cell corresponds to an element in the given cell array.

    :param screen: The pygame screen
    :param cell_array: Cell array to draw.
    :param x_offset: X-Offset from top left corner of screen.
    :param y_offset: Y-Offset from top left corner of screen.
    """

    for i, cell in enumerate(cell_array):
        # Position of cell
        x = x_offset + (i * rect_size)
        y = y_offset + 0

        draw_cell(screen, cell, x, y)
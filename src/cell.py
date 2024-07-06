import pygame
from enum import Enum

from config import rect_size, border_size, Colors, colors, font


# Enumeration containing all the states a cell could be in
class CellState(Enum):
    ACTIVE = 1
    INACTIVE = 2
    SELECTED = 3


# A Cell class containing a value and visual state
class Cell:
    def __init__(self, value: int, state: CellState = CellState.ACTIVE, custom_color: Colors = None) -> None:
        self.value = value
        self.state = state
        self.custom_color = custom_color

    def __str__(self) -> str:
        return f"Cell({self.value}, {self.state.name})"
    
    def draw(self, screen: pygame.Surface, x: int, y: int) -> None:
        """
        Draws a single cell with its label and visual state.

        :param screen: The pygame screen
        :param cell: Cell object.
        :param x: X-Position of cell.
        :param y: Y-Position of cell.
        """

        color = self.get_color()
        
        # Create Rect object
        rect = pygame.Rect(x, y, rect_size, rect_size)
        
        # Draw cell and border
        pygame.draw.rect(screen, colors.BACKGROUND_COLOR, rect)
        pygame.draw.rect(screen, color, rect, border_size)

        # Render text in cell
        text = font.render(f"{self.value}", True, color)
        padding = rect_size / 2
        text_x = x + padding
        text_y = y + padding
        text_rect = text.get_rect(center=(text_x, text_y))
        screen.blit(text, text_rect)

    def set_active(self) -> None:
        self.state = CellState.ACTIVE
    
    def set_inactive(self) -> None:
        self.state = CellState.INACTIVE
    
    def set_selected(self) -> None:
        self.state = CellState.SELECTED

    def set_custom_color(self, custom_color: Colors) -> None:
        self.custom_color = custom_color

    def get_color(self) -> Colors:
        if self.custom_color:
            return self.custom_color
        else:
            match self.state:
                case CellState.ACTIVE:
                    return colors.PRIMARY_COLOR
                case CellState.INACTIVE:
                    return colors.INACTIVE_COLOR
                case _:
                    return colors.SELECTED_COLOR


# CellArray class with methods to operate on all cells
class CellArray():
    def __init__(self, screen: pygame.Surface, array: list[int]) -> None:
        self.screen = screen
        self.cell_array = [Cell(value) for value in array]

    def __str__(self) -> str:
        return "[" + ", ".join(str(cell) for cell in self.cell_array) + "]"
    
    def __len__(self) -> int:
        return len(self.cell_array)
    
    def draw(self, x_offset: int, y_offset: int) -> None:
        """
        Draws a horizontal sequence of cells, where each cell corresponds to an element in the given cell array.

        :param screen: The pygame screen
        :param cell_array: Cell array to draw.
        :param x_offset: X-Offset from top left corner of screen.
        :param y_offset: Y-Offset from top left corner of screen.
        """

        for i, cell in enumerate(self.cell_array):
            # Position of cell
            x = x_offset + (i * rect_size)
            y = y_offset + 0

            # Draw index above cell
            text = font.render(f"{i}", True, colors.SELECTED_COLOR)
            text_rect = text.get_rect(center=(x + rect_size / 2, y - rect_size / 2))
            self.screen.blit(text, text_rect)

            cell.draw(self.screen, x, y)

    def set_active(self, start: int, end: int = None) -> None:
        if end is None:
            # Single index case
            index = start
            self.cell_array[index].set_active()
        else:
            # Range case
            for i in range(start, end + 1):
                self.cell_array[i].set_active()

    def set_inactive(self, start: int, end: int = None) -> None:
        if end is None:
            # Single index case
            index = start
            self.cell_array[index].set_inactive()
        else:
            # Range case
            for i in range(start, end + 1):
                self.cell_array[i].set_inactive()

    def set_selected(self, index: int) -> None:
        self.cell_array[index].set_selected()
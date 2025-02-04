import pygame
from enum import Enum

from config import rect_size, border_size, Color, colors, font
from widgets import draw_centered_text


# Enumeration containing all the states a cell could be in
class CellState(Enum):
    ACTIVE = 1
    INACTIVE = 2
    SELECTED = 3


# A Cell class containing a value and visual state
class Cell:
    def __init__(self, value: int, state: CellState = CellState.ACTIVE, custom_color: Color = None) -> None:
        self.value = value
        self.state = state
        self.custom_color = custom_color

    def __str__(self) -> str:
        return f"Cell({self.value}, {self.state.name})"
    
    def draw(self, screen: pygame.Surface, x: int, y: int) -> None:
        """Draws a single cell with its label and visual state.

        Args:
            screen (pygame.Surface): The pygame screen.
            x (int): x-position of cell.
            y (int): y-position of cell.
        """

        color = self.get_color()
        
        # Create Rect object
        rect = pygame.Rect(x, y, rect_size, rect_size)
        
        # Draw cell and border
        pygame.draw.rect(screen, colors.BACKGROUND_COLOR, rect)
        pygame.draw.rect(screen, color, rect, border_size)

        # Render text in cell
        padding = rect_size / 2
        draw_centered_text(screen, font, color, self.value, x + padding, y + padding)

    def set_active(self) -> None:
        self.state = CellState.ACTIVE
    
    def set_inactive(self) -> None:
        self.state = CellState.INACTIVE
    
    def set_selected(self) -> None:
        self.state = CellState.SELECTED

    def set_custom_color(self, custom_color: Color) -> None:
        self.custom_color = custom_color

    def get_color(self) -> Color:
        """Returns the color hex of the cell.

        Returns:
            Colors: The hex color of the cell.
        """
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
        """Draws a horizontal sequence of cells, where each cell corresponds to an element in the given cell array.

        Args:
            x_offset (int): x-offset from top left corner of screen.
            y_offset (int): y-offset from top left corner of screen.
        """

        for i, cell in enumerate(self.cell_array):
            # Position of cell
            x = x_offset + (i * rect_size)
            y = y_offset + 0

            # Draw index above cell
            draw_centered_text(self.screen, font, colors.SELECTED_COLOR, f"{i}", x + rect_size / 2, y - rect_size / 2)

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

    def set_solution(self, start: int, end: int = None) -> None:
        if end is None:
            # Single index case
            index = start
            self.cell_array[index].set_custom_color(colors.SOLUTION)
        else:
            # Range case
            for i in range(start, end + 1):
                self.cell_array[i].set_custom_color(colors.SOLUTION)

    def swap(self, i1: int, i2: int) -> None:
        self.cell_array[i1], self.cell_array[i2] = self.cell_array[i2], self.cell_array[i1]
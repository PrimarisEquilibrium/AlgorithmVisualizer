import pygame
from enum import Enum
from typing import Optional

from cell import CellArray
from render import draw_cell_array


class BSState(Enum):
    GET_GUESS = 1
    COMPARE_GUESS = 2


class BinarySearch:
    def __init__(self, screen: pygame.Surface, cell_array_obj: CellArray, val: int, x: int = 0, y: int = 0):
        self.screen = screen
        # cell_array_obj is the object instance of CellArray
        # cell_array     is the physical array of all Cells
        self.cell_array_obj = cell_array_obj
        self.cell_array = cell_array_obj.array
        self.val = val
        self.x = x
        self.y = y

        # Starting and ending index of the CellArray
        self.start, self.end = 0, len(self.cell_array) - 1

        # Pointers to array search area
        self.left, self.right = self.start, self.end

        # Private state / variable iterators
        self._state = BSState.GET_GUESS
        self._mid = None
        self._guess = None

    def draw(self) -> None:
        # Renders the cell array to the screen then calls pygame to update it
        draw_cell_array(self.screen, self.cell_array, self.x, self.y)
        pygame.display.update()

    def get_guess(self) -> tuple[int, int]:
        # Sets the current midpoint (as the guess) and value at the midpoint
        self._mid = (self.left + self.right) // 2
        self._guess = self.cell_array[self._mid]
        
        # The current guess is highlighted on the screen
        self.cell_array_obj.set_selected(self._mid)

    def compare_guess(self) -> Optional[int]:
        guess_val = self._guess.value

        # If guess is correct return index in the array
        if guess_val == self.val:
            self.cell_array_obj.set_inactive(self.start, self._mid - 1)
            self.cell_array_obj.set_inactive(self._mid + 1, self.end)
            return self._mid
        # If guess is smaller than value the value is in the larger half of the array
        elif guess_val < self.val:
            self.cell_array_obj.set_inactive(self.start, self._mid)
            self.left = self._mid + 1 
        # If guess is larger than value the value is in the smaller half of the array
        else:
            self.cell_array_obj.set_inactive(self._mid, self.end)
            self.right = self._mid - 1
        
        return None
    
    def search_step(self) -> None:
        # For GET_GUESS state
        #  Get the guess (midpoint of the CellArray) and mark it as "SELECTED"
        #  Proceed the next call of this function to be the COMPARE_GUESS state
        if (self._state == BSState.GET_GUESS):
            self.get_guess()
            self._state = BSState.COMPARE_GUESS
        # For COMPARE_GUESS state
        #  Make the previous "SELECTED" cell to be inactive (not the searched value)
        #  Compare the current guess with the value to find and deactivate the according cells (as to compare_guess())
        #  Proceed the next call of this function to be the GET_GUESS state
        elif (self._state == BSState.COMPARE_GUESS):
            self.cell_array_obj.set_inactive(self._mid)
            self.compare_guess()
            self._state = BSState.GET_GUESS
        self.draw()
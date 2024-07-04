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
        self.cell_array_obj = cell_array_obj
        self.val = val
        self.x = x
        self.y = y
        self.cell_array = cell_array_obj.array
        self.start, self.end = 0, len(self.cell_array) - 1
        self.state = BSState.GET_GUESS
        # Pointers to array search area
        self.left, self.right = self.start, self.end

        self.mid = None
        self.guess = None

    def draw(self) -> None:
        draw_cell_array(self.screen, self.cell_array, self.x, self.y)
        pygame.display.update()

    def get_guess(self) -> tuple[int, int]:
        mid = (self.left + self.right) // 2
        guess = self.cell_array[mid]
        self.cell_array_obj.set_selected(mid)
        return mid, guess

    def compare_guess(self) -> Optional[int]:
        guess_val = self.guess.value

        # If guess is correct return index in the array
        if guess_val == self.val:
            self.cell_array_obj.set_inactive(self.start, self.mid - 1)
            self.cell_array_obj.set_inactive(self.mid + 1, self.end)
            return self.mid
        # If guess is smaller than value the value is in the larger half of the array
        elif guess_val < self.val:
            self.cell_array_obj.set_inactive(self.start, self.mid)
            self.left = self.mid + 1 
        # If guess is larger than value the value is in the smaller half of the array
        else:
            self.cell_array_obj.set_inactive(self.mid, self.end)
            self.right = self.mid - 1
        
        return None
    
    def search_step(self) -> None:
        if (self.state == BSState.GET_GUESS):
            mid, guess = self.get_guess()
            self.mid = mid
            self.guess = guess
            self.state = BSState.COMPARE_GUESS
        elif (self.state == BSState.COMPARE_GUESS):
            self.cell_array_obj.clear_selected()
            self.compare_guess()
            self.state = BSState.GET_GUESS
        self.draw()
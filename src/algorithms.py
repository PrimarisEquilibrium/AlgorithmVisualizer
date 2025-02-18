import pygame
from enum import Enum
from typing import Optional, Any

from cell import CellArray
from config import colors, header
from widgets import draw_text, InputBox, Button
from utils import get_input_data


class BSState(Enum):
    GET_GUESS = 1
    COMPARE_GUESS = 2


class BinarySearch:
    def __init__(self, cell_array_obj: CellArray, val: int, x: int = 0, y: int = 0):
        # cell_array_obj is the object instance of CellArray
        # cell_array     is the physical array of all Cells
        self.cell_array_obj = cell_array_obj
        self.cell_array = cell_array_obj.cell_array
        self.val = val
        self.x = x
        self.y = y

        # Starting and ending index of the CellArray
        self.start, self.end = 0, len(self.cell_array) - 1

        # Pointers to array search area
        self.left, self.right = self.start, self.end

        # Private state / variable iterators
        self._state = BSState.GET_GUESS
        self._solution_found = False
        self._mid = None
        self._guess = None

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
            self.cell_array[self._mid].set_custom_color(colors.SOLUTION)
            self.cell_array_obj.set_inactive(self.start, self._mid - 1)
            self.cell_array_obj.set_inactive(self._mid + 1, self.end)
            self._solution_found = True
        # If guess is smaller than value the value is in the larger half of the array
        elif guess_val < self.val:
            self.cell_array_obj.set_inactive(self.start, self._mid)
            self.left = self._mid + 1 
        # If guess is larger than value the value is in the smaller half of the array
        else:
            self.cell_array_obj.set_inactive(self._mid, self.end)
            self.right = self._mid - 1
        
        return None
    
    def next_step(self) -> None:
        if self._solution_found:
            pass
        else:
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
                self.compare_guess()
                self._state = BSState.GET_GUESS

    def draw(self, screen: pygame.Surface) -> None:
        draw_text(screen, header, colors.SELECTED_COLOR, "Binary Search Algorithm", self.x, self.y - 100)
        
        self.cell_array_obj.draw(self.x, self.y)


class BinarySearchUI:
    def __init__(self, screen: pygame.Surface):
        self.input_boxes = [
            InputBox(screen, "Array to search (seperated by commas)", 50, 140, 500, 50, 30),
            InputBox(screen, "Value to find", 50, 240, 500, 50)
        ]
        self.buttons = [
            Button(screen, "Submit", 50, 320, 125, 60, get_input_data(self.input_boxes))
        ]


class InsertionSort:
    def __init__(self, cell_array_obj: CellArray, x: int, y: int) -> None:
        self.cell_array_obj = cell_array_obj
        self.cell_array = cell_array_obj.cell_array
        self.x = x
        self.y = y

        self.i = 1
        self.cell_array_obj.set_solution(0)
        self.j = self.i
        self.swap_complete = False
        self.solved = False

    def mark_correct_spots(self) -> None:
        self.cell_array_obj.set_solution(0, self.i)
    
    def swap(self) -> None:
        if self.j > 0 and self.cell_array[self.j].value < self.cell_array[self.j - 1].value:
            self.cell_array_obj.swap(self.j, self.j - 1)
            self.j -= 1
        else:
            self.swap_complete = True
            self.mark_correct_spots()

    def next_step(self) -> None:
        if not self.solved:
            if self.i < len(self.cell_array) - 1 or self.j > 0:
                if self.swap_complete:
                    if self.i + 1 < len(self.cell_array):
                        self.i += 1
                    self.j = self.i
                    self.swap_complete = False
                self.swap()
            else:
                self.mark_correct_spots()
                self.solved = True

    def draw(self, screen: pygame.Surface) -> None:
        draw_text(screen, header, colors.SELECTED_COLOR, "Insertion Sort Algorithm", self.x, self.y - 100)
        self.cell_array_obj.draw(self.x, self.y)


class InsertionSortUI:
    def __init__(self, screen: pygame.Surface) -> None:
        self.input_boxes = [
            InputBox(screen, "Array to sort (seperated by commas)", 50, 140, 500, 50, 30),
        ]
        self.buttons = [
            Button(screen, "Submit", 50, 220, 125, 60, get_input_data(self.input_boxes))
        ]


class Node:
    def __init__(self, value) -> None:
        self.value = value
        self.left = None
        self.right = None
    
    def __str__(self) -> str:
        return f"{self.value}"


class MinHeap:
    def __init__(self) -> None:
        pass


class Dijkstra:
    def __init__(self) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        pass

    def next_step(self) -> None:
        pass
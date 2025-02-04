import pygame

from cell import CellArray
from typing import Union, Any
from widgets import InputBox


def cell_array_init(screen: pygame.Surface, user_input: str) -> Union[CellArray, None]:
    try:
        # String cleaning
        user_array = ''.join(user_input.split())
        user_array = user_array.split(",")
        
        # Converts each string number into an integer
        user_array = list(map(lambda x : int(x), user_array))

        cell_array = CellArray(screen, user_array)
        return cell_array
    except ValueError:
        print("Invalid input")
        return None

def get_input_data(input_boxes: list[InputBox]) -> list[Any]:
    def callback():
        results = []
        # Returns all the typed values in all input boxes
        for input_box in input_boxes:
            results.append(input_box.get_value())
            input_box.textinput.value = ""
        return results
    return callback
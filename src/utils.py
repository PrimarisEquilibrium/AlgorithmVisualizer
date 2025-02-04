import pygame
from cell import CellArray
from typing import Union

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
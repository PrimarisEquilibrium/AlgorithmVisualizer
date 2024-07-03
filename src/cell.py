from enum import Enum
from colors import colors


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
                return colors.PRIMARY_COLOR
            case CellState.INACTIVE:
                return colors.INACTIVE_COLOR
            case _:
                return colors.SELECTED_COLOR


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
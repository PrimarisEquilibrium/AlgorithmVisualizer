from enum import Enum
from colors import Colors, colors


# Enumeration containing all the states a cell could be in
class CellState(Enum):
    ACTIVE = 1
    INACTIVE = 2
    SELECTED = 3


# A Cell class containing a value and visual state
class Cell:
    def __init__(self, value: int, state: CellState = CellState.ACTIVE) -> None:
        self.value = value
        self.state = state

    def __str__(self) -> str:
        return f"Cell({self.value}, {self.state.name})"

    def set_active(self) -> None:
        self.state = CellState.ACTIVE
    
    def set_inactive(self) -> None:
        self.state = CellState.INACTIVE
    
    def set_selected(self) -> None:
        self.state = CellState.SELECTED

    def get_color(self) -> Colors:
        match self.state:
            case CellState.ACTIVE:
                return colors.PRIMARY_COLOR
            case CellState.INACTIVE:
                return colors.INACTIVE_COLOR
            case _:
                return colors.SELECTED_COLOR


# CellArray class with methods to operate on all cells
class CellArray():
    def __init__(self, *args: int) -> None:
        self.array = self.make_cell_array(*args)

    def __str__(self) -> str:
        return "[" + ", ".join(str(cell) for cell in self.array) + "]"
    
    def __len__(self) -> int:
        return len(self.array)
    
    def make_cell_array(self, *args: int) -> list[Cell]:
        # Create a Cell object for each element in the array
        return [Cell(arg) for arg in args]
    
    def clear_selected(self) -> None:
        for cell in self.array:
            if cell.state == CellState.SELECTED:
                cell.set_inactive()

    def set_active(self, start: int, end: int = None) -> None:
        if end is None:
            # Single index case
            index = start
            self.array[index].set_active()
        else:
            # Range case
            for i in range(start, end + 1):
                self.array[i].set_active()

    def set_inactive(self, start: int, end: int = None) -> None:
        if end is None:
            # Single index case
            index = start
            self.array[index].set_inactive()
        else:
            # Range case
            for i in range(start, end + 1):
                self.array[i].set_inactive()

    def set_selected(self, index: int) -> None:
        self.array[index].set_selected()
import pygame
from typing import Optional, Any

from cell import CellArray
from algorithms import BinarySearch, InsertionSort
from config import colors
from widgets import InputBox, Button


# pygame setup
pygame.init()
pygame.display.set_caption("Kevin's Algorithm Visualizer")

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# pygame Handlers
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class AlgorithmVisualizer:
    def __init__(self) -> None:
        self.current_algorithm_obj = None
        self.time = pygame.time.get_ticks()
        self.interval = 500 # Interval (in ms) between each algorithm step
        self.running = True # Toggles if the game loop is running
        self.state = "home"
        self.algorithm_chosen = None

        # Each algorithm may or may not have a different UI, therefore store them arbitrarily in a list
        self.input_boxes = []
        self.buttons = []

        self.home_buttons = [
            {"label": "bsa", "obj": Button(screen, "Binary Search Algorithm", 50, 50, 260, 60, (lambda: None))},
            {"label": "isa", "obj": Button(screen, "Insertion Sort Algorithm", 50, 130, 260, 60, (lambda: None))}
        ]

    def cell_array_init(self, user_input: str) -> Optional[CellArray]:
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

    def get_input_data(self) -> list[Any]:
        results = []
        # Returns all the typed values in all input boxes
        for input_box in self.input_boxes:
            results.append(input_box.get_value())
        return results

    def initialize_ui_elements(self):
        # Depending on what algorithm is chosen initialize different UI elements
        if self.algorithm_chosen == "bsa":
            self.input_boxes = [
                InputBox(screen, "Array to search (seperated by commas)", 35, 60, 500, 50, 30),
                InputBox(screen, "Value to find", 35, 160, 500, 50)
            ]
            self.buttons = [
                Button(screen, "Submit", 35, 240, 125, 60, self.get_input_data)
            ]
        elif self.algorithm_chosen == "isa":
            self.input_boxes = [
                InputBox(screen, "Array to sort (seperated by commas)", 35, 60, 500, 50, 30),
            ]
            self.buttons = [
                Button(screen, "Submit", 35, 130, 125, 60, self.get_input_data)
            ]
    
    def run(self) -> None:
        while self.running:
            screen.fill(colors.BACKGROUND_COLOR)
            events = pygame.event.get()
            for event in events:
                # Allows the window to be closed on QUIT ("X" at top right of the window)
                if event.type == pygame.QUIT:
                    self.running = False

            if self.state == "home":
                self.home_page(events)
            elif self.state == "input":
                self.input_page(events)
            elif self.state == "algorithm":
                self.algorithm_page()

            # Displays contents onto screen
            pygame.display.update()

            # Sets the FPS of the window to 60
            clock.tick(60)

        pygame.quit()
    
    def home_page(self, events):
        # Home page contains buttons to select an algorithm
        for button in self.home_buttons:
            button["obj"].draw()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in self.home_buttons:
                    if (button["obj"].is_mouse_over(mouse_x, mouse_y)):
                        # Set the algorithm and change the program state to the algorithm argument input section
                        self.algorithm_chosen = button["label"]
                        self.state = "input"
    
    _ui_variables_bounded = False
    def input_page(self, events):
        # Only initialize the ui element variables one time
        if not self._ui_variables_bounded:
            self.initialize_ui_elements()
            self._ui_variables_bounded = True
            return

        # Render the UI elements
        for button in self.buttons:
            button.draw()

        for input_box in self.input_boxes:
            input_box.draw(events)

        # UI elements typically have the same functionality, however logic changes on buttons on_click functions
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.is_mouse_over(mouse_x, mouse_y):
                        match self.algorithm_chosen:
                            case "bsa":
                                user_input, val = button.on_click()
                                print(user_input)
                                cell_array = self.cell_array_init(user_input)
                                self.current_algorithm_obj = BinarySearch(cell_array, int(val), 50, 140)
                            case "isa":
                                user_input = button.on_click()[0]
                                cell_array = self.cell_array_init(user_input)
                                self.current_algorithm_obj = InsertionSort(cell_array, 50, 140)
                        self.state = "algorithm"

                for input_box in self.input_boxes:
                    input_box.handle_focus(events, mouse_x, mouse_y)

    def algorithm_page(self):
        # Draw out the algorithm
        # Algorithms must have a draw and next_step function
        if self.current_algorithm_obj:
            self.current_algorithm_obj.draw(screen)
            current_time = pygame.time.get_ticks()
            if current_time - self.time >= self.interval:
                self.time = current_time
                self.current_algorithm_obj.draw(screen)
                self.current_algorithm_obj.next_step()


if __name__ == "__main__":
    visualizer = AlgorithmVisualizer()
    visualizer.run()
import pygame
from typing import Any

from algorithms import BinarySearch, BinarySearchUI, InsertionSort, InsertionSortUI
from config import colors, header
from widgets import Button, draw_text, draw_centered_text
from utils import cell_array_init


# pygame setup
pygame.init()
pygame.display.set_caption("Kevin's Algorithm Visualizer")

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

CTR_X = SCREEN_WIDTH / 2
CTR_Y = SCREEN_HEIGHT / 2

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

        # Variables to ensure buttons are evenly spaced
        starting_x = 100
        btn_height = 60
        padding = 20
        spacing = btn_height + padding
        self.home_buttons = [
            {"label": "bsa", "obj": Button(screen, "Binary Search Algorithm", 50, starting_x, 260, 60, (lambda: None))},
            {"label": "isa", "obj": Button(screen, "Insertion Sort Algorithm", 50, starting_x + spacing, 260, 60, (lambda: None))}
        ]

        self.back_button = Button(screen, "Return to home", 50, SCREEN_HEIGHT - 100, 200, 60, lambda: None)

    def initialize_ui_elements(self):
        # Depending on what algorithm is chosen initialize different UI elements
        if self.algorithm_chosen == "bsa":
            binary_search_ui = BinarySearchUI(screen)
            self.input_boxes = binary_search_ui.input_boxes
            self.buttons = binary_search_ui.buttons
        elif self.algorithm_chosen == "isa":
            insertion_sort_ui = InsertionSortUI(screen)
            self.input_boxes = insertion_sort_ui.input_boxes
            self.buttons = insertion_sort_ui.buttons
    
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
                self.algorithm_page(events)

            # Displays contents onto screen
            pygame.display.update()

            # Sets the FPS of the window to 60
            clock.tick(60)

        pygame.quit()
    
    def home_page(self, events):
        draw_centered_text(screen, header, colors.SELECTED_COLOR, "Algorithm Visualizer", CTR_X, 50)

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
        draw_text(screen, header, colors.SELECTED_COLOR, "Enter algorithm arguments", 50, 30)

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
                                cell_array = cell_array_init(screen, user_input)
                                self.current_algorithm_obj = BinarySearch(cell_array, int(val), 50, 140)
                            case "isa":
                                user_input = button.on_click()[0]
                                cell_array = cell_array_init(screen, user_input)
                                self.current_algorithm_obj = InsertionSort(cell_array, 50, 140)
                        self.state = "algorithm"

                for input_box in self.input_boxes:
                    input_box.handle_focus(events, mouse_x, mouse_y)

    def algorithm_page(self, events: pygame.event.Event):
        self.back_button.draw()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.back_button.is_mouse_over(mouse_x, mouse_y):
                    self.state = "home"
                    self.algorithm_chosen = None
                    self.current_algorithm_obj = None
                    self.input_boxes = []
                    self.buttons = []
                    self._ui_variables_bounded = False

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
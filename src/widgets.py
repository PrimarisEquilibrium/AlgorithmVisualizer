import pygame
import pygame_textinput

from typing import Callable, Any
from cell import font
from colors import colors

class InputBox:
    def __init__(self, screen: pygame.Surface, label: str, x: int, y: int, width: int, height: int, max_length: int = 20) -> None:
        self.screen = screen
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_length = max_length

        # Base pygame text input module
        self.manager = pygame_textinput.TextInputManager(validator = lambda input : len(input) <= max_length)
        self.textinput = pygame_textinput.TextInputVisualizer(
            manager=self.manager,
            font_color=colors.PRIMARY_COLOR, 
            cursor_color=colors.BACKGROUND_COLOR, 
            font_object=font,
            cursor_width=0
        )
        self._text_box = pygame.Rect(x, y, width, height)
        self.is_focused = False
    
    def draw(self, events: list[pygame.event.Event]) -> None:
        # Draw input box label
        text = font.render(f"{self.label}", True, colors.SELECTED_COLOR)
        self.screen.blit(text, (self.x, self.y - 35))

        # Draw box around text input
        pygame.draw.rect(self.screen, colors.BACKGROUND_COLOR, self._text_box)
        pygame.draw.rect(self.screen, colors.PRIMARY_COLOR, self._text_box, 5)

        # Draw the text input
        if (self.is_focused):
            # Only update the text input if it is in focus
            self.textinput.update(events)
        _, text_height = self.textinput.surface.get_size()
        padding = (self.height - text_height) // 2
        self.screen.blit(self.textinput.surface, (self.x + padding, self.y + padding))
    
    def cursor_in_textbox(self, mouse_x: int, mouse_y: int) -> None:
        """ Returns true if the cursor is located inside the text_box rect """
        if (mouse_x >= self.x and mouse_y >= self.y and
            mouse_x <= self.x + self.width and mouse_y <= self.y + self.height):
            return True
        return False
        
    def toggle_focus(self, events: list[pygame.event.Event]) -> None:
        # Toggle is_focused variable and cursor
        if (not self.is_focused):
            self.textinput.cursor_width = 4
            self.textinput.cursor_color = colors.PRIMARY_COLOR
            self.is_focused = True
        else:
            self.textinput.cursor_width = 0
            self.textinput.cursor_color = colors.BACKGROUND_COLOR
            self.is_focused = False
        self.draw(events)

    def handle_focus(self, events: pygame.event.Event, mouse_x: int, mouse_y: int):
        if (self.cursor_in_textbox(mouse_x, mouse_y)):
            self.toggle_focus(events)
        else:
            self.is_focused = False
    
    def get_value(self) -> str:
        return self.textinput.value
        
    
class Button:
    def __init__(self, screen: pygame.Surface, label: str, x: int, y: int, width: int, height: int, on_click: Callable) -> None:
        self.screen = screen
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.on_click = on_click
    
    def draw(self) -> None:
        button_rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.is_mouse_over(mouse_x, mouse_y):
            if pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(self.screen, colors.ACTIVE_COLOR, button_rect)
            else:
                pygame.draw.rect(self.screen, colors.HOVER_COLOR, button_rect)
        else:
            pygame.draw.rect(self.screen, colors.BACKGROUND_COLOR, button_rect)
        pygame.draw.rect(self.screen, colors.PRIMARY_COLOR, button_rect, 5)

        text = font.render(f"{self.label}", True, colors.SELECTED_COLOR)
        width_padding = self.width / 2
        height_padding = self.height / 2
        text_x = self.x + width_padding
        text_y = self.y + height_padding
        text_rect = text.get_rect(center=(text_x, text_y))
        self.screen.blit(text, text_rect)
    
    def is_mouse_over(self, mouse_x: int, mouse_y: int) -> bool:
        if (mouse_x >= self.x and mouse_y >= self.y and
            mouse_x <= self.x + self.width and mouse_y <= self.y + self.height):
            return True
        return False
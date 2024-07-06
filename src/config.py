import pygame
from collections import namedtuple

# Array cell properties
rect_size = 50
border_size = 5

# Fonts
pygame.font.init()
header = pygame.font.Font("fonts/Roboto-Bold.ttf", 36)
font = pygame.font.Font("fonts/Roboto-Regular.ttf", 22)

# Colors
Colors = namedtuple("Colors", ["BACKGROUND_COLOR", "PRIMARY_COLOR", "INACTIVE_COLOR", "SELECTED_COLOR", "SOLUTION", "HOVER_COLOR", "ACTIVE_COLOR"])
colors = Colors(
    BACKGROUND_COLOR = "#151515",
    PRIMARY_COLOR = "#a6a6a6",
    INACTIVE_COLOR = "#454545",
    SELECTED_COLOR = "#ffffff",
    SOLUTION = "#00FF00",
    HOVER_COLOR = "#454545",
    ACTIVE_COLOR = "#595959"
)
from collections import namedtuple

# Colors
Colors = namedtuple("Colors", ["BACKGROUND_COLOR", "PRIMARY_COLOR", "INACTIVE_COLOR", "SELECTED_COLOR", "SOLUTION"])
colors = Colors(
    BACKGROUND_COLOR = "#151515",
    PRIMARY_COLOR = "#a6a6a6",
    INACTIVE_COLOR = "#454545",
    SELECTED_COLOR = "#ffffff",
    SOLUTION = "#00FF00"
)
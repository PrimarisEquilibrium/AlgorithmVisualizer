import pygame

# pygame setup
pygame.init()
pygame.font.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font("fonts/Roboto-Regular.ttf", 25)
clock = pygame.time.Clock()

PRIMARY_COLOR = "#151515"
SECONDARY_COLOR = "#d3d3d3"


def binary_search(arr, val):
    """
    Returns the index of a given value in a sorted array.
    
    :param arr: Array to search.
    :param val: The value to search for.
    :return: The index of the value or False if it was not found.
    """

    # Pointers to array search area
    start = 0
    end = len(arr) - 1 # len(<list>) is a constant time operation
    while end >= start:
        mid = (start + end) // 2
        guess = arr[mid]
        print(f"Start: {start}, End: {end}, Mid: {mid}, Guess: {guess}")
        # If guess is correct return index in the array
        if guess == val:
            print(f"Result found: {guess} at index [{mid}]")
            return mid
        # If guess is smaller than value the value is in the larger half of the array
        elif guess < val:
            start = mid + 1
        # If guess is larger than value the value is in the smaller half of the array
        else:
            end = mid - 1
    print("Result not found")
    return False

print(binary_search([10, 20, 30, 40, 50], 50))


# Array cell properties
rect_size = 75
border = 5
def draw_array(arr, x_offset, y_offset):
    """
    Draws a horizontal sequence of cells, where each cell corresponds to an element in the given array.

    :param arr: Array to draw.
    :param x_offset: X-Offset from top left corner of screen.
    :param y_offset: Y-Offset from top left corner of screen.
    """

    for i, display_text in enumerate(arr):
        # Position of cell
        x = x_offset + (i * rect_size)
        y = y_offset + 0

        # Create Rect object
        rect = pygame.Rect(x, y, rect_size, rect_size)
        
        # Draw cell and border
        pygame.draw.rect(screen, PRIMARY_COLOR, rect)
        pygame.draw.rect(screen, SECONDARY_COLOR, rect, border)

        # Render text in cell
        text = font.render(f"{display_text}", True, SECONDARY_COLOR)
        padding = rect_size / 2
        text_x = x + padding
        text_y = y + padding
        text_rect = text.get_rect(center=(text_x, text_y))
        screen.blit(text, text_rect)

running = True
while running:
    # Allows the window to be closed on QUIT ("X" at top right of the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("#151515")

    draw_array([0, 1, 2, 3, 4], 50, 50)

    # Displays contents onto screen
    pygame.display.update()
    
    # Sets the FPS of the window to 60
    clock.tick(60)

pygame.quit()
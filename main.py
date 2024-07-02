import pygame

# pygame setup
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


def binary_search(arr, val):
    """
    Returns the index of a given value in a sorted array
    
    :param arr: Array to search
    :param val: The value to search for
    :return: The index of the value or False if it was not found
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


running = False
while running:
    # Allows the window to be closed on QUIT ("X" at top right of the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Displays contents onto screen
    pygame.display.update()
    
    # Sets the FPS of the window to 60
    clock.tick(60)

pygame.quit()
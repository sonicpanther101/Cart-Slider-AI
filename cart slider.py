import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Square")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define the square and line properties
SQUARE_SIZE = 50
SQUARE_X = WIDTH // 2 - SQUARE_SIZE // 2
SQUARE_Y = HEIGHT // 2 - SQUARE_SIZE // 2
LINE_LENGTH = 100
LINE_ANGLE = 0
LINE_VELOCITY = 0
LINE_DAMPING = 0.98  # Damping factor for realistic swinging motion

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and SQUARE_X > 0:
        SQUARE_X -= 5
        LINE_VELOCITY += 0.2  # Apply a force to the line when the square moves
    if keys[pygame.K_RIGHT] and SQUARE_X < WIDTH - SQUARE_SIZE:
        SQUARE_X += 5
        LINE_VELOCITY -= 0.2  # Apply a force to the line when the square moves

    # Update the line angle and velocity
    LINE_ANGLE += LINE_VELOCITY
    LINE_VELOCITY *= LINE_DAMPING  # Apply damping to the line velocity

    # Clear the window
    WINDOW.fill(WHITE)

    # Draw the square
    pygame.draw.rect(WINDOW, BLACK, (SQUARE_X, SQUARE_Y, SQUARE_SIZE, SQUARE_SIZE))

    # Draw the line
    line_end_x = SQUARE_X + SQUARE_SIZE // 2 + LINE_LENGTH * math.cos(LINE_ANGLE)
    line_end_y = SQUARE_Y + SQUARE_SIZE // 2 + LINE_LENGTH * math.sin(LINE_ANGLE)
    pygame.draw.line(WINDOW, BLACK, (SQUARE_X + SQUARE_SIZE // 2, SQUARE_Y + SQUARE_SIZE // 2), (line_end_x, line_end_y), 2)

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
# Import the pygame module
import pygame
import sys
from pygame.locals import *

# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame
pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set up the FPS (frames per second) clock
clock = pygame.time.Clock()

running = True

# Manually define the frame boundaries (adjust these based on the frame image)
FRAME_LEFT = 30   # Left boundary of the playable area
FRAME_RIGHT = 770  # Right boundary of the playable area
FRAME_TOP = 30    # Top boundary of the playable area
FRAME_BOTTOM = 570  # Bottom boundary of the playable area

# Character class
class Character:
    def __init__(self, image_path, x, y):
        # Load character image
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()  # Create a rect for the player
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Walls:
    def __init__(self, image_path, x, y):
        # Load wall image (frame)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()  # Create a rect for the wall
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# Create a player object with the image and starting position
player = Character("Bilder/vanilla_ice_cream_back_looking.png", 400, 300)

# Create the frame (wall) object
wall = Walls("Bilder/frame.png", 0, 0)

# Main game loop
while running:
    # Clear the screen with a background color (optional)
    screen.fill((255, 255, 255))  # Filling with white background

    # Event handling
    for event in pygame.event.get():
        # Check for QUIT event to exit the game
        if event.type == QUIT:
            running = False
        # Check for keypresses
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    # Handle continuous keypresses for movement
    keys = pygame.key.get_pressed()

    # Set movement to zero initially
    move_x, move_y = 0, 0

    # Restrict movement to one axis at a time
    if keys[K_LEFT]:
        move_x = -8
    elif keys[K_RIGHT]:
        move_x = 8
    elif keys[K_UP]:
        move_y = -8
    elif keys[K_DOWN]:
        move_y = 8

    # Create a copy of the player's rect to check for new position
    new_rect = player.rect.move(move_x, move_y)

    # Manually check against the frame boundaries
    if new_rect.left < FRAME_LEFT:   # Left boundary
        new_rect.left = FRAME_LEFT
    if new_rect.right > FRAME_RIGHT:  # Right boundary
        new_rect.right = FRAME_RIGHT
    if new_rect.top < FRAME_TOP:     # Top boundary
        new_rect.top = FRAME_TOP
    if new_rect.bottom > FRAME_BOTTOM:  # Bottom boundary
        new_rect.bottom = FRAME_BOTTOM

    # Update player's rect
    player.rect = new_rect

    # Draw the frame and player character 
    wall.draw(screen)
    player.draw(screen)

    # Update the display
    pygame.display.update()

    # Cap the frame rate at 30 frames per second
    clock.tick(30)

# Quit pygame
pygame.quit()
sys.exit()

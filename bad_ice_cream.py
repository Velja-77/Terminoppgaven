# Import the pygame module
import pygame
import sys
from pygame.locals import *
import random 

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

# Initialize score variable
score = 0

# Manually define the frame collisions (adjust these based on the frame image)
FRAME_LEFT = 30   # Left collision of the playable area
FRAME_RIGHT = 770  # Right collision of the playable area
FRAME_TOP = 30    # Top collision of the playable area
FRAME_BOTTOM = 570  # Bottom collision of the playable area

# Set up the font and size for displaying the score
font = pygame.font.Font(None, 30)  # Use default font, size 36

# Character class
class Character:
    def __init__(self, image_path, x, y):
        # Load character image
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()  # Create a rect for the player
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        
class Monster:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()  
        self.rect.topleft = (x, y)
        self.direction = random.choice(['left', 'right', 'up', 'down'])

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
    
    def move(self):
        if self.direction == 'left':
            self.rect.x -= 5
            if self.rect.left <= FRAME_LEFT:  
                self.direction = 'down'
        elif self.direction == 'right':
            self.rect.x += 5
            if self.rect.right >= FRAME_RIGHT:  
                self.direction = 'up'
        elif self.direction == 'up':
            self.rect.y -= 5
            if self.rect.top <= FRAME_TOP:  
                self.direction = 'left'
        elif self.direction == 'down':
            self.rect.y += 5
            if self.rect.bottom >= FRAME_BOTTOM:  
                self.direction = 'right'  

class Walls:
    def __init__(self, image_path, x, y):
        # Load wall image (frame)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()  # Create a rect for the wall
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Fruit:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()  # Create a rect for the fruit
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

def fruits_location(positions):
    fruits = []
    for pos in positions:
        fruits.append(Fruit("Bilder/banana.png", pos[0], pos[1]))
    return fruits

# Create a player object with the image and starting position
player = Character("Bilder/vanilla_ice_cream_back_looking.png", 400, 400)

fruit_positions = [
    (30, 30), (30, 60), (60, 30),
    (30, 540), (30, 510), (60, 540),
    (740, 30), (710, 30), (740, 60),
    (740, 540), (710, 540), (740, 510),
]

monster = Monster("Bilder/monster.png", 30, 30)

# Create multiple fruits at these positions
fruits = fruits_location(fruit_positions)

# Create the frame (wall) object
wall = Walls("Bilder/frame.png", 0, 0)

# Main game loop
while running:
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

    # Check against the frame collisions
    if new_rect.left < FRAME_LEFT:   # Left collision
        new_rect.left = FRAME_LEFT
    if new_rect.right > FRAME_RIGHT:  # Right collision
        new_rect.right = FRAME_RIGHT
    if new_rect.top < FRAME_TOP:     # Top collision
        new_rect.top = FRAME_TOP
    if new_rect.bottom > FRAME_BOTTOM:  # Bottom collision
        new_rect.bottom = FRAME_BOTTOM

    # Update player's rect
    player.rect = new_rect

    # Check for collision between player and any fruit
    for fruit in fruits[:]:  
        if player.rect.colliderect(fruit.rect):
            fruits.remove(fruit)  # Remove the fruit when collected
            score += 50            # Increase the score
    
    monster.move()

    if player.rect.colliderect(monster.rect):
        running = False

    # Render the score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # LAG GULL FARGE!!!!!

    # Draw the frame, player character, and all fruits
    wall.draw(screen)
    player.draw(screen)
    monster.draw(screen)
    for fruit in fruits:
        fruit.draw(screen)

    # Draw the score at the top left of the screen
    screen.blit(score_text, (10, 10))

    # Check if all fruits are eaten
    if len(fruits) == 0:
        running = False  # Exit the game when all fruits are collected

    # Update the display
    pygame.display.update()

    # Cap the frame rate at 30 frames per second
    clock.tick(30)

# Quit pygame 
pygame.quit()
sys.exit()

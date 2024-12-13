# Import the pygame module
import pygame
import sys
from pygame.locals import *
import random 
import mysql.connector

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

def printMenu():
    print("----------Log in or view Leaderboard----------")
    print("| 1. Sign up                                  ")
    print("| 2. Log in and play                          ")
    print("| 3. View leaderboard                         ")
    print("| 4. Search player                            ")
    print("| 5. Exit                                     ")
    menuChoice = input("Enter a number 1-5 to select from the menu: ")
    ifMenuChoice(menuChoice)

def ifMenuChoice(numberChoice):
    if(numberChoice == "1"):
        registerPlayer()
    elif(numberChoice == "2"):
        logIn()
    elif(numberChoice == "3"):
        leaderboard()
    elif(numberChoice == "4"):
        searchPlayer()
    elif(numberChoice == "5"):
        confirm = input("Are you sure you want to exit? Y/N")
        if(confirm == "Y" or confirm == "y"):
            exit()
        else:
            printMenu()
    else:
        again = input("Invalid choice. Enter a number 1-5. ")
        ifMenuChoice(again)

def registerPlayer():
    choice =("Press M to return to the menu or R to register.")
    if choice == 'm' or choice == 'M':
        printMenu()
    elif choice == 'r' or choice == 'R':
        name = input("Write your name:")
        password = input("Press M to return to the menu. Write your password:")
    else:
        print("Invalid choice.")
        printMenu()
        
    storeInDB(name, password)

    input("Press enter to return to the Menu.")
    printMenu()
    runGame()

def logIn():
    mydb = mysql.connector.connect(
        host="10.2.3.62",
        user="velja",
        password="velja123",
        database="score",
        port=3306,
        charset='utf8mb4',
        collation='utf8mb4_general_ci'
    )
    mycursor = mydb.cursor()

    name = input("Write your name:")
    password = input("Write your password:")

    sql = "SELECT * FROM player WHERE name = %s AND password = %s"
    val = (name, password)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()

    if result:
        print(f"Welcome back, {name}!")
        runGame(name)
    else:
        print("Invalid credentials.")
        choice = input("Press R to retry login or M to return to the menu.").lower()
        if choice == 'r' or choice == 'R':
            logIn() # Retry log in
        elif choice == 'm' or choice == 'M':
            printMenu() # Return to the menu
        else:
            print("Invalid choice.")
            printMenu()
        
def searchPlayer():
    name = input("Search by name: ")
    findPlayer(name)

def findPlayer(name):
    mydb = mysql.connector.connect(
        host="10.2.3.62",
        user="velja",
        password="velja123",
        database="score",
        port=3306,
        charset='utf8mb4',
        collation='utf8mb4_general_ci'
    )
    mycursor = mydb.cursor()

    sql = "SELECT name, score FROM player WHERE name = %s"
    val = (name, )

    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()  # Fetch one result

    if myresult:
        player_name, player_score = myresult
        print(f"Player found, Name: {player_name}, Score: {player_score}")
    else:
        print(f"No player found with the name: {name}")
        
    input("Press enter to return to the menu.")
    printMenu()
    
    # Close the cursor and the connection
    mycursor.close()
    mydb.close()

def storeInDB(name, password, score=0):
    mydb = mysql.connector.connect(
        host="10.2.3.62",
        user="velja",
        password="velja123",
        database="score",
        port=3306,
        charset='utf8mb4',
        collation='utf8mb4_general_ci'
    )
    mycursor = mydb.cursor()

    sql = "INSERT INTO player (name, password, score) VALUES (%s, %s, %s)"
    val = (name, password, score)
    mycursor.execute(sql, val)
    mydb.commit()
    print("Signed up successfully.")
    mycursor.close()
    mydb.close()

def updateScore(name, score):
    mydb = mysql.connector.connect(
        host="10.2.3.62",
        user="velja",
        password="velja123",
        database="score",
        port=3306,
        charset='utf8mb4',
        collation='utf8mb4_general_ci'
    )
    mycursor = mydb.cursor()

    # SQL query to update the player's score
    sql = "UPDATE player SET score = %s WHERE name = %s"
    val = (score, name)
    mycursor.execute(sql, val)
    mydb.commit()

    print(f"Updated score for {name} to {score}.")
    mycursor.close()
    mydb.close()

def leaderboard():
    # Connect to the database
    mydb = mysql.connector.connect(
        host="10.2.3.62",
        user="velja",
        password="velja123",
        database="score",
        port=3306,
        charset='utf8mb4',
        collation='utf8mb4_general_ci'
    )
    mycursor = mydb.cursor()

    # SQL query to get the top 5 players by score
    sql = "SELECT name, score FROM player ORDER BY score DESC LIMIT 5"
    mycursor.execute(sql)
    results = mycursor.fetchall()

    # Print the leaderboard
    print("----------Leaderboard----------")
    for idx, (name, score) in enumerate(results, start=1):
        print(f"{idx}. {name}: {score} points")
    
    # Close the database connection
    mycursor.close()
    mydb.close()

    # Return to the menu after showing the leaderboard
    input("Press Enter to return to the menu.")
    printMenu()

def gameWon():
    gameOverFont = pygame.font.Font(None, 74)
    smallFont = pygame.font.Font(None, 40)

    gameOverText = gameOverFont.render("You won!", True, (33, 106, 99))  
    scoreText = smallFont.render(f"Your score: {score}", True, (33, 106, 99))   
    restartText = smallFont.render("Press R to restart or Q to quit", True, (33, 106, 99))

    while True: 
        screen.fill((255, 255, 255))

        screen.blit(gameOverText, (SCREEN_WIDTH // 2 - gameOverText.get_width() // 2, SCREEN_HEIGHT // 2 - 75))
        screen.blit(scoreText, (SCREEN_WIDTH // 2 - scoreText.get_width() // 2, SCREEN_HEIGHT // 2 - 0))
        screen.blit(restartText, (SCREEN_WIDTH // 2 - restartText.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
       
        pygame.display.update()

        # Event handling for restart or quit
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_r:
                    restartGame()  # Restart the game
                    return          # Exit the game_over loop to avoid keeping the screen
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Game Over Function
def gameOver(player_name):
    global score
    updateScore(player_name, score)

    gameOverFont = pygame.font.Font(None, 74)
    smallFont = pygame.font.Font(None, 40)

    gameOverText = gameOverFont.render("Game Over.", True, (33, 106, 99))  
    scoreText = smallFont.render(f"Your score: {score}", True, (33, 106, 99))   
    restartText = smallFont.render("Press R to restart or Q to quit", True, (33, 106, 99))

    while True: 
        screen.fill((255, 255, 255))

        screen.blit(gameOverText, (SCREEN_WIDTH // 2 - gameOverText.get_width() // 2, SCREEN_HEIGHT // 2 - 75))
        screen.blit(scoreText, (SCREEN_WIDTH // 2 - scoreText.get_width() // 2, SCREEN_HEIGHT // 2 - 0))
        screen.blit(restartText, (SCREEN_WIDTH // 2 - restartText.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
       
        pygame.display.update()

        # Event handling for restart or quit
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_r:
                    restartGame(player_name)  # Restart the game
                    return          # Exit the game_over loop to avoid keeping the screen
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def restartGame(player_name):
    global score, player, fruits, monster, monster2, ices

    # Reset score and player position
    score = 0
    player = Character(player_images, 400, 400)

    # Reset fruits and monsters
    fruit_positions = [
        (30, 30), (30, 60), (60, 30),
        (30, 540), (30, 510), (60, 540),
        (740, 30), (710, 30), (740, 60),
        (740, 540), (710, 540), (740, 510),
    ]
    fruits = fruits_location(fruit_positions)

    ice_positions = [
        (60, 60),
        (60, 510), 
        (710, 60), 
        (710, 510), 
    ]
    ices = ice_location(ice_positions)

    monster = Monster("Bilder/monster.png", 30, 30)
    monster2 = Monster2("Bilder/monster.png", 60, 60)

    # Restart the game loop
    runGame(player_name)

# Character class
class Character:
    def __init__(self, image_paths, x, y):
        # Load character images for all directions
        self.images = {
            'left': pygame.image.load(image_paths['left']),
            'right': pygame.image.load(image_paths['right']),
            'up': pygame.image.load(image_paths['up']),
            'down': pygame.image.load(image_paths['down'])
        }
        self.current_image = self.images['down']  # Set the initial image (facing down)
        self.rect = self.current_image.get_rect()  # Create a rect for the player
        self.rect.topleft = (x, y)

    def draw(self, screen):
        # Blit the current image, not the dictionary
        screen.blit(self.current_image, self.rect.topleft)

    def change_direction(self, direction):
        if direction in self.images:
            self.current_image = self.images[direction]  # Change the image to the new direction

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
            self.rect.x -= 8
            if self.rect.left <= FRAME_LEFT:  
                self.direction = 'down'
        elif self.direction == 'right':
            self.rect.x += 8
            if self.rect.right >= FRAME_RIGHT:  
                self.direction = 'up'
        elif self.direction == 'up':
            self.rect.y -= 8
            if self.rect.top <= FRAME_TOP:  
                self.direction = 'left'
        elif self.direction == 'down':
            self.rect.y += 8
            if self.rect.bottom >= FRAME_BOTTOM:  
                self.direction = 'right'  

class Monster2:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()  
        self.rect.topleft = (x, y)
        self.direction = random.choice(['left', 'right', 'up', 'down'])

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def move(self):
        if self.direction == 'left':
            self.rect.x -= 8
            if self.rect.left <= FRAME_LEFT:  
                self.direction = 'down'
        elif self.direction == 'right':
            self.rect.x += 8
            if self.rect.right >= FRAME_RIGHT:  
                self.direction = 'up'
        elif self.direction == 'up':
            self.rect.y -= 8
            if self.rect.top <= FRAME_TOP:  
                self.direction = 'left'
        elif self.direction == 'down':
            self.rect.y += 8
            if self.rect.bottom >= FRAME_BOTTOM:  
                self.direction = 'right'  

class Walls:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()  
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Fruit:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()  
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

def fruits_location(positions):
    fruits = []
    for pos in positions:
        fruits.append(Fruit("Bilder/banana.png", pos[0], pos[1]))
    return fruits

class Ice:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()  
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

def ice_location(positions):
    ices = []
    for pos in positions:
        ices.append(Ice("Bilder/ice_cube.png", pos[0], pos[1]))
    return ices

player_images = {
    'left': "Bilder/vanilla_ice_cream_left_looking.png",
    'right': "Bilder/vanilla_ice_cream_right_looking.png",
    'up': "Bilder/vanilla_ice_cream_back_looking.png",
    'down': "Bilder/vanilla_ice_cream_forward_looking.png"
}

# Create a player object with the image and starting position
player = Character(player_images, 400, 400)

fruit_positions = [
    (30, 30), (30, 60), (60, 30),
    (30, 540), (30, 510), (60, 540),
    (740, 30), (710, 30), (740, 60),
    (740, 540), (710, 540), (740, 510),
]

ice_positions = [
    (60, 60),
    (60, 510), 
    (710, 60), 
    (710, 510), 
]

monster = Monster("Bilder/monster.png", 30, 30)
monster2 = Monster2("Bilder/monster.png", 60, 60)

# Create multiple fruits at these positions
fruits = fruits_location(fruit_positions)

ices = ice_location(ice_positions)

# Create the frame (wall) object
wall = Walls("Bilder/frame.png", 0, 0)

def runGame(player_name):
    # Main game loop
    global score
    running = True
    while running:
        screen.fill((255, 255, 255))  # White background

        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == pygame.K_r:
                    restartGame()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        # Handle continuous keypresses for movement
        keys = pygame.key.get_pressed()
        move_x, move_y = 0, 0 # Set movement to zero initially
        direction = None # Variable to store the direction

        # Restrict movement to one axis at a time
        if keys[K_LEFT]:
            move_x = -10
            direction = 'left'
        elif keys[K_RIGHT]:
            move_x = 10
            direction = 'right'
        elif keys[K_UP]:
            move_y = -10
            direction = 'up'
        elif keys[K_DOWN]:
            move_y = 10
            direction = 'down'

        # Change the player direction image
        if direction:
            player.change_direction(direction)

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
        monster2.move()

        if player.rect.colliderect(monster.rect) or player.rect.colliderect(monster2.rect):
            gameOver(player_name)

        # Render the score
        score_text = font.render(f"Score: {score}", True, (255, 215, 0)) 

        # Draw the frame, player character, and all fruits
        wall.draw(screen)
        player.draw(screen)
        monster.draw(screen)
        monster2.draw(screen)
        for ice in ices:
            ice.draw(screen)
        for fruit in fruits:
            fruit.draw(screen)

        # Draw the score at the top left of the screen
        screen.blit(score_text, (10, 10))

        # Check if all fruits are eaten
        if len(fruits) == 0:
            gameWon()

        # Update the display
        pygame.display.update()

        # Cap the frame rate at 30 frames per second
        clock.tick(30)

    # Quit pygame 
    pygame.quit()

# Run the menu first
printMenu()

# Once the user is logged in, start the game
runGame()

import pygame # type: ignore
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MathQuest")

# Game clock
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (169, 169, 169)

# Fonts
HEADER_FONT = pygame.font.Font(None, 70)
QUESTION_FONT = pygame.font.Font(None, 50)
OPTION_FONT = pygame.font.Font(None, 40)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5

    def update(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed

# Puzzle class
class Puzzle:
    def __init__(self, question, options, answer):
        self.question = question
        self.options = options
        self.answer = answer

    def check_answer(self, player_answer):
        return player_answer == self.answer

# Generate a random math puzzle suitable for 9th-grade level
def generate_puzzle():
    puzzle_type = random.choice(["arithmetic", "algebraic_identity", "geometry"])
    
    if puzzle_type == "algebraic_identity":
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        identity = random.choice(["(a+b)^2", "(a-b)^2", "a^2-b^2"])
        
        if identity == "(a+b)^2":
            question = f"Expand: ({x} + {y})^2"
            answer = x**2 + 2*x*y + y**2
        elif identity == "(a-b)^2":
            question = f"Expand: ({x} - {y})^2"
            answer = x**2 - 2*x*y + y**2
        elif identity == "a^2-b^2":
            question = f"Simplify: {x**2} - {y**2}"
            answer = (x + y) * (x - y)
    elif puzzle_type == "geometry":
        side = random.randint(5, 15)
        question = f"Calculate the area of a square with side {side} units"
        answer = side ** 2
    else:
        num1 = random.randint(1, 100)
        num2 = random.randint(1, 100)
        question = f"What is {num1} + {num2}?"
        answer = num1 + num2
    
    options = [answer]
    while len(options) < 4:
        wrong_answer = random.randint(answer - 10, answer + 10)
        if wrong_answer not in options and wrong_answer > 0:
            options.append(wrong_answer)
    
    random.shuffle(options)
    
    return Puzzle(question, options, answer)

# Display puzzle and get player's answer
def display_puzzle(puzzle):
    screen.fill(GRAY)
    
    header_text = HEADER_FONT.render("MathQuest by Aviral Tyagi", True, BLACK)
    screen.blit(header_text, (50, 50))
    
    for i in range(5, SCREEN_WIDTH, 100):
        screen.blit(HEADER_FONT.render("+", True, LIGHT_GRAY), (i, 0))
        screen.blit(HEADER_FONT.render("x", True, LIGHT_GRAY), (i - 50, 100))
    
    question_text = QUESTION_FONT.render(puzzle.question, True, BLACK)
    screen.blit(question_text, (50, 200))
    
    option_rects = []
    for i, option in enumerate(puzzle.options):
        option_text = OPTION_FONT.render(str(option), True, BLACK)
        option_rect = option_text.get_rect(topleft=(50, 300 + i * 50))
        option_rects.append((option_rect, option))
        screen.blit(option_text, option_rect.topleft)
    
    pygame.display.flip()
    
    selected_option = None
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for option_rect, option in option_rects:
                    if option_rect.collidepoint(mouse_pos):
                        selected_option = option
                        input_active = False

        screen.fill(GRAY)
        screen.blit(header_text, (50, 50))
        for i in range(5, SCREEN_WIDTH, 100):
            screen.blit(HEADER_FONT.render("+", True, LIGHT_GRAY), (i, 0))
            screen.blit(HEADER_FONT.render("x", True, LIGHT_GRAY), (i - 50, 100))
        screen.blit(question_text, (50, 200))
        for option_rect, option in option_rects:
            screen.blit(OPTION_FONT.render(str(option), True, BLACK), option_rect.topleft)
        
        pygame.display.flip()

    return selected_option

# Main game loop
def game_loop():
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    puzzle = generate_puzzle()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys_pressed = pygame.key.get_pressed()
        all_sprites.update(keys_pressed)

        screen.fill(GRAY)
        all_sprites.draw(screen)

        player_answer = display_puzzle(puzzle)
        if puzzle.check_answer(player_answer):
            print("Correct!")
            puzzle = generate_puzzle()
        else:
            print("Try again!")

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

# Run the game
game_loop()

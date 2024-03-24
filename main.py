import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
GRAVITY = 0.25
FLAP_STRENGTH = -5
PIPE_WIDTH_PERCENTAGE = 0.01
PIPE_HEIGHT = 200
GAP_SIZE = 150
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Load images
bird_image = pygame.image.load('bird.png').convert_alpha()
pipe_image = pygame.image.load('pipe.png').convert_alpha()
background_image = pygame.image.load('background.png').convert_alpha()  # Load background image
bird_image = pygame.transform.scale(bird_image, (150, 150))
pipe_image = pygame.transform.scale(pipe_image, (200, 700))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_image
        self.rect = self.image.get_rect(center=(100, SCREEN_HEIGHT // 2 - 50))
        self.vel_y = 0

    def update(self):
        # Apply gravity
        self.vel_y += GRAVITY

        # Update bird's position
        self.rect.y += self.vel_y

        # Keep bird within screen bounds
        if self.rect.top <= 0:  # Top boundary
            self.rect.top = 0
            if self.vel_y < 0:  # If bird is moving upward
                self.vel_y = 0  # Stop upward movement
        elif self.rect.bottom >= SCREEN_HEIGHT:  # Bottom boundary
            self.rect.bottom = SCREEN_HEIGHT
            self.vel_y = 0  # Stop downward movement

    def flap(self):
        if self.rect.top > 0:  # Only flap if the bird is within the screen bounds
            self.vel_y = FLAP_STRENGTH


# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pipe_image
        self.rect = self.image.get_rect()
        self.rect.height = random.randint(50, 700)
        self.rect.width = int(SCREEN_WIDTH * PIPE_WIDTH_PERCENTAGE)
        self.rect.x = x + SCREEN_WIDTH
        # Set y position to ensure the bottom of the pipe is at the bottom of the screen
        self.rect.y = SCREEN_HEIGHT - self.rect.height

        # Store the initial width for later use
        self.initial_width = self.rect.width

    def update(self):
        self.rect.x -= 5
        self.rect.width = self.initial_width
        if self.rect.right < 0:
            self.kill()


# Create sprites groups
all_sprites = pygame.sprite.Group()
pipes_group = pygame.sprite.Group()

# Create bird
bird = Bird()
all_sprites.add(bird)

# Game loop
score = 0
pipe_spawn_delay = 200
current_frame = 0
clock = pygame.time.Clock()
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.flap()

    # Update
    all_sprites.update()


    # Spawn pipes
    current_frame += 1
    if current_frame % pipe_spawn_delay == 0 and len(pipes_group) < 3:
        score += 1
        pipe = Pipe(SCREEN_WIDTH)
        pipes_group.add(pipe)
        all_sprites.add(pipe)

    # Check collisions
    if pygame.sprite.spritecollide(bird, pipes_group, False):
        running = False

    # Draw
    screen.blit(background_image, (0, 0))  # Draw background image
    all_sprites.draw(screen)
    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()

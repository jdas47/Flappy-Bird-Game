import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.5
BIRD_JUMP = -10
PIPE_WIDTH = 60
PIPE_GAP = 150
PIPE_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (135, 206, 250)

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock
clock = pygame.time.Clock()

# Load Bird Image
BIRD_WIDTH, BIRD_HEIGHT = 40, 40
bird_image = pygame.image.load("bird.png")  # Replace with your bird image file
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))

# Game Variables
bird_x, bird_y = 50, HEIGHT // 2
bird_velocity = 0

pipes = []
score = 0

# Function to create pipes
def create_pipe():
    pipe_height = random.randint(100, HEIGHT - PIPE_GAP - 100)
    top_pipe = pygame.Rect(WIDTH, 0, PIPE_WIDTH, pipe_height)
    bottom_pipe = pygame.Rect(WIDTH, pipe_height + PIPE_GAP, PIPE_WIDTH, HEIGHT - pipe_height - PIPE_GAP)
    return top_pipe, bottom_pipe

# Function to reset the game
def reset_game():
    global bird_x, bird_y, bird_velocity, pipes, score
    bird_x, bird_y = 50, HEIGHT // 2
    bird_velocity = 0
    pipes.clear()
    pipes.append(create_pipe())
    score = 0

# Create the first pipe
pipes.append(create_pipe())

# Game Loop
running = True
game_over = False
while running:
    screen.fill(BLUE)  # Sky background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                bird_velocity = BIRD_JUMP
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                reset_game()
                game_over = False

    if not game_over:
        # Bird movement
        bird_velocity += GRAVITY
        bird_y += bird_velocity

        # Update pipes
        for pipe in pipes:
            pipe[0].x -= PIPE_SPEED
            pipe[1].x -= PIPE_SPEED

        # Check for off-screen pipes and create new ones
        if pipes[0][0].x + PIPE_WIDTH < 0:
            pipes.pop(0)
            pipes.append(create_pipe())
            score += 1

        # Collision detection
        bird_rect = pygame.Rect(bird_x, bird_y, BIRD_WIDTH, BIRD_HEIGHT)
        for pipe in pipes:
            if bird_rect.colliderect(pipe[0]) or bird_rect.colliderect(pipe[1]):
                game_over = True
                break

        # Check if bird hits the ground or goes above the screen
        if bird_y + BIRD_HEIGHT > HEIGHT or bird_y < 0:
            game_over = True

    # Draw bird
    screen.blit(bird_image, (bird_x, bird_y))

    # Draw pipes
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe[0])  # Top pipe
        pygame.draw.rect(screen, GREEN, pipe[1])  # Bottom pipe

    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Game over screen
    if game_over:
        font = pygame.font.Font(None, 48)
        game_over_text = font.render("Game Over", True, BLACK)
        restart_text = font.render("Press 'R' to Restart", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

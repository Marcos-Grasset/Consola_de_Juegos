import pygame
import random

# Inicialización de Pygame
pygame.init()

# Definición de colores
BLACK = (0, 0, 0)
NEON_BLUE = (0, 255, 255)
NEON_GREEN = (57, 255, 20)
NEON_RED = (255, 0, 102)
NEON_YELLOW = (255, 255, 0)
NEON_ORANGE = (255, 165, 0)
NEON_PURPLE = (128, 0, 128)

# Lista de colores de fondo para cada nivel
BACKGROUND_COLORS = [
    (30, 0, 30),
    (0, 30, 60),
    (30, 30, 0),
    (0, 0, 30),
    (30, 15, 30),
    (15, 30, 30),
]

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Brick Breaker")

PADDLE_WIDTH = 120
PADDLE_HEIGHT = 20
paddle_speed = 10

BALL_SIZE = 20
ball_speed_x = 5 * random.choice((-1, 1))
ball_speed_y = -5

score = 0
level = 1
lives = 3
game_over = False

# Inicializar la música de fondo
background_music_sound = pygame.mixer.Sound('Brick Breaker/music.wav')
background_music_sound.set_volume(0.5)  # Ajusta el volumen (0.0 a 1.0)
background_music_sound.play(-1)  # Reproduce en bucle

# Cargar sonidos
bounce_sound = pygame.mixer.Sound('Brick Breaker/bounce.wav')
break_sound = pygame.mixer.Sound('Brick Breaker/break.wav')
lose_life_sound = pygame.mixer.Sound('Brick Breaker/lose_life.wav')
level_up_sound = pygame.mixer.Sound('Brick Breaker/level_up.wav')
game_over_sound = pygame.mixer.Sound('Brick Breaker/game_over.wav')
game_over_sound.set_volume(1.0)  # Ajusta el volumen (0.0 a 1.0)

ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)

class Bubble:
    def __init__(self):
        self.size = random.randint(15, 40)
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed_y = random.uniform(1.0, 2.0)
        self.color = random.choice([NEON_BLUE, NEON_GREEN, NEON_PURPLE])

    def move(self):
        self.y -= self.speed_y
        if self.y < -self.size:
            self.y = HEIGHT + self.size
            self.x = random.randint(0, WIDTH)

    def draw(self):
        bubble_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(bubble_surface, (0, 0, 0), (self.size, self.size), self.size)
        pygame.draw.circle(bubble_surface, self.color, (self.size, self.size), self.size - 1)

        for i in range(self.size - 1, 0, -1):
            color = tuple(max(0, int(c * (1 - (i / self.size)))) for c in self.color)
            pygame.draw.circle(bubble_surface, color, (self.size, self.size), i)

        screen.blit(bubble_surface, (self.x - self.size, self.y - self.size))

def create_blocks(rows, cols):
    block_width = WIDTH // cols
    block_height = 30
    blocks = []
    for row in range(rows):
        for col in range(cols):
            block_x = col * block_width
            block_y = row * block_height + 100
            blocks.append(pygame.Rect(block_x, block_y, block_width, block_height))
    return blocks

blocks = create_blocks(5, 10)
bubbles = [Bubble() for _ in range(20)]

def draw_background():
    current_background_color = BACKGROUND_COLORS[level - 1]
    gradient_surface = pygame.Surface((WIDTH, HEIGHT))

    for y in range(HEIGHT):
        color = (
            int(current_background_color[0] * (y / HEIGHT)),
            int(current_background_color[1] * (y / HEIGHT)),
            int(current_background_color[2] * (y / HEIGHT)),
        )
        pygame.draw.line(gradient_surface, color, (0, y), (WIDTH, y))

    screen.blit(gradient_surface, (0, 0))

def draw_message():
    font = pygame.font.Font(pygame.font.get_default_font(), 60)
    font.set_italic(True)
    
    # Crear el texto en color rojo
    text = font.render("Game Over!", True, NEON_RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
    
    # Crear bordes en amarillo alrededor del texto principal
    for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2), (0, -2), (0, 2), (-2, 0), (2, 0)]:
        outline = font.render("Game Over!", True, NEON_YELLOW)
        screen.blit(outline, text_rect.move(dx, dy))
    
    # Dibujar el texto principal encima
    screen.blit(text, text_rect)

    # Texto de instrucciones
    font_small = pygame.font.Font(pygame.font.get_default_font(), 30)
    instructions = ["'R' Restart", "'M' Menu", "'E' Exit"]
    for i, line in enumerate(instructions):
        text_line = font_small.render(line, True, NEON_YELLOW)
        screen.blit(text_line, text_line.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 40)))

def draw():
    draw_background()
    for bubble in bubbles:
        bubble.move()
        bubble.draw()

    draw_paddle(paddle)
    draw_ball_with_effect(ball)

    for block in blocks:
        draw_block_with_effect(block)

    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 50))

    font = pygame.font.Font(pygame.font.get_default_font(), 28)
    font.set_italic(True)

    score_text = font.render(f"Score: {score}", True, NEON_YELLOW)
    level_text = font.render(f"Level: {level}", True, NEON_YELLOW)
    lives_text = font.render(f"Lives: {lives}", True, NEON_YELLOW)

    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10 + score_text.get_width() + 20, 10))
    screen.blit(level_text, (WIDTH - 150, 10))

    pygame.display.flip()

def draw_ball_with_effect(ball_rect):
    pygame.draw.ellipse(screen, NEON_GREEN, ball_rect)
    pygame.draw.ellipse(screen, NEON_YELLOW, ball_rect.inflate(10, 10), 2)

def draw_block_with_effect(block_rect):
    color = random.choice([NEON_RED, NEON_ORANGE, NEON_BLUE, NEON_GREEN, NEON_PURPLE])
    shadow_color = (0, 0, 0)
    pygame.draw.rect(screen, shadow_color, block_rect.inflate(5, 5))
    pygame.draw.rect(screen, color, block_rect)
    pygame.draw.rect(screen, NEON_YELLOW, block_rect.inflate(10, 10), 2)
    pygame.draw.rect(screen, NEON_RED, block_rect.inflate(-5, -5), 1)

def draw_paddle(paddle_rect):
    pygame.draw.rect(screen, NEON_BLUE, paddle_rect)
    pygame.draw.rect(screen, NEON_YELLOW, paddle_rect.inflate(10, 10), 2)

def reset_game():
    global score, level, lives, ball, paddle, blocks, game_over, bubbles
    score = 0
    level = 1
    lives = 3
    game_over = False
    ball.x = WIDTH // 2 - BALL_SIZE // 2
    ball.y = HEIGHT // 2
    paddle.x = WIDTH // 2 - PADDLE_WIDTH // 2
    blocks = create_blocks(5, 10)
    bubbles = [Bubble() for _ in range(20)]  # Reiniciar burbujas

def game_over_screen():
    global game_over
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_m:
                    main_menu_screen()  # Ir al menú principal
                elif event.key == pygame.K_e:
                    pygame.quit()
                    exit()

        draw_background()
        for bubble in bubbles:
            bubble.move()
            bubble.draw()

        draw_message()
        pygame.display.flip()


# Bucle principal del juego
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += paddle_speed

    if not game_over:
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed_x *= -1
            bounce_sound.play()

        if ball.top <= 0:
            ball_speed_y *= -1
            bounce_sound.play()

        if ball.colliderect(paddle):
            ball_speed_y *= -1
            ball.y = paddle.top - BALL_SIZE
            bounce_sound.play()

        if ball.bottom >= HEIGHT:
            lives -= 1
            lose_life_sound.play()
            if lives <= 0:
                game_over = True
                game_over_sound.play()
            else:
                ball.x = WIDTH // 2 - BALL_SIZE // 2
                ball.y = HEIGHT // 2

        for block in blocks:
            if ball.colliderect(block):
                ball_speed_y *= -1
                score += 10
                break_sound.play()
                blocks.remove(block)
                if not blocks:  # Si no quedan bloques
                    level += 1
                    blocks = create_blocks(5 + level, 10 + level)  # Aumentar dificultad
                    level_up_sound.play()
                    ball_speed_x *= random.choice((-1, 1))
                    ball_speed_y *= random.choice((-1, 1))
                    break

    if game_over:
        game_over_screen()
    else:
        draw()
    clock.tick(100)

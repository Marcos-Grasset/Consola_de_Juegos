import pygame
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colores
WHITE = (255, 255, 255)
NEON_COLOR = (0, 255, 255)
BLACK = (0, 0, 0)

# Parámetros iniciales
initial_ball_speed = 7
initial_paddle_speed = 10
paddle_width, paddle_height = 15, 100
obstacle_width, obstacle_height = 20, 20

# Cargar la imagen de fondo
background = pygame.image.load("cancha.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Cargar el sonido de rebote
bounce_sound = pygame.mixer.Sound("rebote.ogg")

# Cargar la música de fondo y configurarla para que suene en loop
pygame.mixer.music.load("pongmusica.ogg")  # Cargar la música
pygame.mixer.music.set_volume(0.3)  # Opcional: ajustar el volumen (0.0 a 1.0)

# Crear objetos
balls = []
obstacles = []
player_paddle = pygame.Rect(20, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
ai_paddle = pygame.Rect(WIDTH - 40, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)

# Variables del juego
ball_speeds = []
paddle_speed = initial_paddle_speed
clock = pygame.time.Clock()
running = True
player_score = 0
ai_score = 0
level = 1
goals_to_win = 5

class Obstacle:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(100, WIDTH - 100), random.randint(50, HEIGHT - 50),
                                obstacle_width, obstacle_height)
        self.speed = random.choice([-3, 3])

    def move(self):
        self.rect.y += self.speed
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed = -self.speed

    def draw(self):
        pygame.draw.rect(screen, NEON_COLOR, self.rect)

def show_start_screen():
    screen.fill(BLACK)

    # Cargar la imagen para la pantalla de inicio
    start_image = pygame.image.load("start.png")  # Asegúrate de tener la imagen en el directorio correcto
    start_image = pygame.transform.scale(start_image, (300, 300))  # Ajusta el tamaño según necesites

    # Calcular las coordenadas para centrar la imagen
    image_x = WIDTH // 2 - start_image.get_width() // 2
    image_y = HEIGHT // 2 - start_image.get_height() // 2 - 30  # Ajuste hacia arriba

    # Dibujar la imagen en pantalla
    screen.blit(start_image, (image_x, image_y))

    # Crear y mostrar el texto
    font = pygame.font.Font(None, 50)
    start_text = font.render("Presiona espacio para empezar", True, WHITE)

    # Posicionar el texto con un margen mayor debajo de la imagen
    text_x = WIDTH // 2 - start_text.get_width() // 2
    text_y = image_y + start_image.get_height() + 50  # 50 píxeles debajo de la imagen

    # Dibujar el texto en pantalla
    screen.blit(start_text, (text_x, text_y))

    # Actualizar la pantalla
    pygame.display.flip()

def generate_balls_for_level():
    global balls, ball_speeds
    balls = []
    ball_speeds = []
    balls.append(pygame.Rect(WIDTH // 2, HEIGHT // 2, 20, 20))
    ball_speeds.append(random_ball_speed())

def random_ball_speed():
    speed_x = initial_ball_speed if random.random() > 0.5 else -initial_ball_speed
    speed_y = initial_ball_speed if random.random() > 0.5 else -initial_ball_speed
    return [speed_x, speed_y]

def reset_ball_positions():
    for i, ball in enumerate(balls):
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speeds[i] = random_ball_speed()

generate_balls_for_level()

# Pantalla de inicio
show_start_screen()

# Esperar a que el usuario presione espacio
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.mixer.music.play(-1)  # Iniciar música en loop (infinito)
                break  # Salir del bucle de inicio para empezar el juego

    # Romper el bucle si se presionó espacio
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        break

# Reiniciar las variables del juego para comenzar
running = True
generate_balls_for_level()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controles del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_paddle.top > 0:
        player_paddle.y -= paddle_speed
    if keys[pygame.K_DOWN] and player_paddle.bottom < HEIGHT:
        player_paddle.y += paddle_speed

    # Movimiento de las pelotas
    for i in range(len(balls)):
        balls[i].x += ball_speeds[i][0]
        balls[i].y += ball_speeds[i][1]

        if balls[i].top <= 0 or balls[i].bottom >= HEIGHT:
            ball_speeds[i][1] = -ball_speeds[i][1]
            bounce_sound.play()  # Reproducir sonido al chocar con el borde

        if balls[i].colliderect(player_paddle) or balls[i].colliderect(ai_paddle):
            ball_speeds[i][0] = -ball_speeds[i][0]
            bounce_sound.play()  # Reproducir sonido al chocar con las palas

    # Movimiento del paddle de la IA (siguiendo la trayectoria de la pelota)
    for ball in balls:
        if ai_paddle.top < ball.y and ai_paddle.bottom < HEIGHT:
            ai_paddle.y += paddle_speed // 2  # Velocidad de seguimiento
        elif ai_paddle.bottom > ball.y and ai_paddle.top > 0:
            ai_paddle.y -= paddle_speed // 2  # Velocidad de seguimiento

    # Ajustar el tamaño del paddle del jugador y la IA en función del nivel
    if level == 2 or level == 5:
        ai_paddle.height = 150
    else:
        ai_paddle.height = paddle_height

    if level == 3 or level == 5:  # Reducir tamaño del jugador en nivel 3 y 5
        player_paddle.height = 60
    else:
        player_paddle.height = paddle_height

    # Movimiento de los obstáculos
    for obstacle in obstacles:
        obstacle.move()

    # Comprobación de goles
    game_over_message = ""
    for i, ball in enumerate(balls):
        if ball.left <= 0:
            ai_score += 1
            if ai_score >= goals_to_win:
                running = False
                game_over_message = "Fin de la partida"
            else:
                reset_ball_positions()

        elif ball.right >= WIDTH:
            player_score += 1
            if player_score >= goals_to_win:
                if level < 5:
                    level += 1
                    player_score, ai_score = 0, 0
                    paddle_speed += 1.2
                    generate_balls_for_level()

                    if level >= 4:
                        obstacles = [Obstacle() for _ in range(5)]

                    if level == 5:
                        player_paddle.height = 60
                        obstacles = [Obstacle() for _ in range(10)]
                else:
                    running = False
                    game_over_message = "¡Felicidades! Juego completado."
            else:
                reset_ball_positions()

    # Colisiones con obstáculos
    for ball in balls:
        for obstacle in obstacles:
            if ball.colliderect(obstacle.rect):
                ball_speeds[0][0] = -ball_speeds[0][0]
                bounce_sound.play()
                break

    # Dibujar el fondo
    screen.blit(background, (0, 0))

    # Dibujar pelotas, paletas y obstáculos
    for ball in balls:
        pygame.draw.ellipse(screen, NEON_COLOR, ball.inflate(10, 10))
        pygame.draw.ellipse(screen, WHITE, ball)

    pygame.draw.rect(screen, NEON_COLOR, player_paddle.inflate(10, 10), border_radius=10)
    pygame.draw.rect(screen, WHITE, player_paddle, border_radius=10)
    pygame.draw.rect(screen, NEON_COLOR, ai_paddle.inflate(10, 10), border_radius=10)
    pygame.draw.rect(screen, WHITE, ai_paddle, border_radius=10)

    for obstacle in obstacles:
        obstacle.draw()

    # Dibujar puntajes y nivel
    font_large = pygame.font.Font(None, 100)
    player_score_text = font_large.render(str(player_score), True, WHITE)
    ai_score_text = font_large.render(str(ai_score), True, WHITE)
    screen.blit(player_score_text, (WIDTH // 4 - player_score_text.get_width() // 2, 50))
    screen.blit(ai_score_text, (3 * WIDTH // 4 - ai_score_text.get_width() // 2, 50))

    font_small = pygame.font.Font(None, 36)
    level_text = font_small.render(f"Nivel: {level}", True, WHITE)
    screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 25))

    pygame.display.flip()
    clock.tick(60)

# Pantalla de fin de partida
screen.fill(BLACK)
font = pygame.font.Font(None, 74)
end_text = font.render(game_over_message, True, WHITE)
screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - end_text.get_height() // 2))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
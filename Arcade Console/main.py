import pygame
import math

# Inicialización de Pygame
pygame.init()

# Configurar sonido de fondo en bucle
pygame.mixer.music.load("Arcade console/menu.wav")  # Carga el archivo de sonido
pygame.mixer.music.play(-1)  # Reproduce en bucle indefinidamente

# Colores y dimensiones
NEON_CYAN = (0, 255, 255)  # Cian
NEON_VIOLET = (148, 0, 211)  # Violeta
NEON_YELLOW = (255, 255, 0)
BACKGROUND_COLOR_1 = (30, 0, 30)
BACKGROUND_COLOR_2 = (0, 30, 60)

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcade Console")

# Variables generales
clock = pygame.time.Clock()
running = True
game_started = False
player_name = ""
selected_game = 0  # 0 = Brick Breaker, 1 = Snake, 2 = Bubble Shooter, 3 = Ping Pong
main_menu = False

# Inicializar la variable angle
angle = 0

# Cargar la imagen del arcade y fondos
arcade_image = pygame.image.load("Arcade console/ARCADE.png")
arcade_image = pygame.transform.scale(arcade_image, (400, 200))

# Cargar los fondos
background_image = pygame.image.load("Arcade console/fondo.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
background_image1 = pygame.image.load("Arcade console/fondo1.jpg")  # Fondo para la pantalla de ingreso de nombre
background_image1 = pygame.transform.scale(background_image1, (WIDTH, HEIGHT))
background_image2 = pygame.image.load("Arcade console/fondo2.jpg")
background_image2 = pygame.transform.scale(background_image2, (WIDTH, HEIGHT))

# Cargar la imagen para reemplazar "Comenzar!"
start_button_image = pygame.image.load("Arcade console/start.png")
start_button_image = pygame.transform.scale(start_button_image, (200, 100))  # Botón más grande

# Variables para el efecto de bucle infinito
bg_x = 0  # Posición inicial de fondo
bg_speed = 2  # Velocidad de desplazamiento del fondo

# Definir fuentes
def get_font(size, italic=False):
    return pygame.font.SysFont(["Franklin Gothic Medium", "Arial Narrow", "Arial"], size, italic=italic)

# Función para mostrar texto centrado
def draw_text(text, size, color, y, italic=False):
    font = get_font(size, italic=italic)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, y))
    screen.blit(text_surface, text_rect)

# Pantalla de bienvenida
def welcome_screen(angle, start_button_pressed):
    # Animación de fondo
    y_offset = (math.sin(math.radians(angle)) * 10)
    screen.blit(background_image, (0, y_offset))
    screen.blit(background_image, (0, y_offset - HEIGHT))

    # Calcular la posición de la imagen
    radius = 80
    center_x = WIDTH // 2
    center_y = HEIGHT // 3
    x = center_x + radius * math.cos(math.radians(angle))
    y = center_y + radius * math.sin(math.radians(angle))

    # Dibujar imagen
    screen.blit(arcade_image, (x - arcade_image.get_width() // 2, y - arcade_image.get_height() // 2))

    # Dibujar el botón de "Comenzar" usando la imagen con efecto de presión
    start_button_rect = start_button_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))  # Mueve el botón más abajo
    if start_button_pressed:
        # Mantener el centro del botón en su lugar mientras se escala
        pressed_button = pygame.transform.scale(start_button_image, (180, 90))  # Reducir tamaño para el efecto
        pressed_button_rect = pressed_button.get_rect(center=start_button_rect.center)
        screen.blit(pressed_button, pressed_button_rect)
    else:
        screen.blit(start_button_image, start_button_rect)

    # Crear la pastilla para el texto
    rect_width = 400
    rect_height = 50
    rect_x = (WIDTH - rect_width) // 2
    rect_y = HEIGHT // 6 + 280  # Ajustar posición según sea necesario

    # Crear la pastilla con bordes neon
    inner_color = (0, 0, 0)  # Fondo de la pastilla
    outer_color = NEON_VIOLET  # Color del borde

    # Dibujar borde
    pygame.draw.rect(screen, outer_color, (rect_x, rect_y, rect_width, rect_height), border_radius=15)
    # Dibujar interior
    pygame.draw.rect(screen, inner_color, (rect_x + 5, rect_y + 5, rect_width - 10, rect_height - 10), border_radius=10)

    # Dibujar texto de instrucciones centrado dentro de la pastilla
    draw_text("Pulsa START para continuar", 30, NEON_CYAN, rect_y + rect_height // 2, italic=True)  # Texto dentro de la pastilla

    pygame.display.flip()
    return start_button_rect

# Pantalla de ingreso de nombre
def name_input_screen(pulse_scale):
    global player_name, bg_x

    # Mover el fondo hacia la izquierda
    bg_x -= bg_speed
    if bg_x <= -WIDTH:
        bg_x = 0  # Reiniciar la posición

    # Dibujar el fondo desplazado
    screen.blit(background_image1, (bg_x, 0))
    screen.blit(background_image1, (bg_x + WIDTH, 0))  # Para crear el efecto de bucle

    # Ajuste de la posición de la imagen arcade y su tamaño
    center_x = WIDTH // 2
    center_y = max(arcade_image.get_height() // 2 + 20, HEIGHT // 3)  # Asegurar que no quede recortada arriba

    scaled_image = pygame.transform.scale(
        arcade_image, 
        (int(arcade_image.get_width() * pulse_scale), 
         int(arcade_image.get_height() * pulse_scale))
    )

    # Asegurarse que la imagen no quede fuera de la pantalla
    screen.blit(scaled_image, (center_x - scaled_image.get_width() // 2, center_y - scaled_image.get_height() // 2))

    # Obtener el ancho del texto del nombre para ajustar la pastilla
    font = get_font(30, italic=True)
    text_surface = font.render("Ingresa tu Nombre: " + player_name, True, NEON_CYAN)
    text_width = text_surface.get_width()

    # Definir un ancho mínimo para la pastilla
    min_rect_width = 400
    rect_width = max(min_rect_width, text_width + 40)  # Añadir un padding extra de 40 píxeles

    # Crear la pastilla para el texto
    rect_height = 50
    rect_x = (WIDTH - rect_width) // 2
    rect_y = HEIGHT // 2 + 80  # Ajustar posición según sea necesario

    # Crear la pastilla con bordes neon
    inner_color = (0, 0, 0)  # Fondo de la pastilla
    outer_color = NEON_VIOLET  # Color del borde

    # Dibujar borde
    pygame.draw.rect(screen, outer_color, (rect_x, rect_y, rect_width, rect_height), border_radius=15)
    # Dibujar interior
    pygame.draw.rect(screen, inner_color, (rect_x + 5, rect_y + 5, rect_width - 10, rect_height - 10), border_radius=10)

    # Dibujar texto de entrada centrado dentro de la pastilla
    screen.blit(text_surface, text_surface.get_rect(center=(WIDTH // 2, rect_y + rect_height // 2)))

    pygame.display.flip()



# Pantalla de menú principal
def main_menu_screen():
    y_offset = (math.sin(pygame.time.get_ticks() / 1000) * 10)
    screen.blit(background_image2, (0, y_offset))
    screen.blit(background_image2, (0, y_offset - HEIGHT))

    image_x = (WIDTH - arcade_image.get_width()) // 2
    image_y = (HEIGHT - arcade_image.get_height()) // 2 - 200
    screen.blit(arcade_image, (image_x, image_y))

    # Ajuste aquí para mover el mensaje de bienvenida más abajo
    draw_text(f"Bienvenido {player_name}!", 40, NEON_CYAN, HEIGHT // 17 + 200, italic=True)

    menu_options = ["1. Brick Breaker", "2. Snake", "3. Bubble Shooter", "4. Ping Pong"]
    for i, option in enumerate(menu_options):
        # Dibujar una pastilla neon
        rect_width = 400
        rect_height = 50
        rect_x = (WIDTH - rect_width) // 2
        rect_y = HEIGHT // 2 + i * (rect_height + 10)  # Espaciado entre opciones

        # Crear la pastilla con bordes neon
        inner_color = (0, 0, 0)  # Fondo negro
        outer_color = NEON_YELLOW if i == selected_game else NEON_VIOLET

        # Dibujar borde
        pygame.draw.rect(screen, outer_color, (rect_x, rect_y, rect_width, rect_height), border_radius=15)
        # Dibujar interior
        pygame.draw.rect(screen, inner_color, (rect_x + 5, rect_y + 5, rect_width - 10, rect_height - 10), border_radius=10)

        # Dibujar texto centrado
        draw_text(option, 40, NEON_CYAN, rect_y + rect_height // 2, italic=True)

    pygame.display.flip()

# Pantalla principal y selección de juego
pulse_scale = 1.0
pulse_direction = 1
start_button_pressed = False

while running:
    if not game_started:
        start_button_rect = welcome_screen(angle, start_button_pressed)
        angle += 2
        if angle >= 360:
            angle = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    start_button_pressed = True  # Activar el efecto de botón presionado
            if event.type == pygame.MOUSEBUTTONUP:
                if start_button_rect.collidepoint(event.pos):
                    game_started = True
                    start_button_pressed = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start_button_pressed = False
                    game_started = True
    else:
        if not main_menu:
            name_input_screen(pulse_scale)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        main_menu = True
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode
            pulse_scale += 0.02 * pulse_direction
            if pulse_scale >= 1.2:
                pulse_direction = -1
            elif pulse_scale <= 1.0:
                pulse_direction = 1
        else:
            main_menu_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        print(f"Juego seleccionado: {selected_game}")
                    if event.key == pygame.K_UP:
                        selected_game = (selected_game - 1) % 4
                    if event.key == pygame.K_DOWN:
                        selected_game = (selected_game + 1) % 4

    clock.tick(60)

pygame.quit()

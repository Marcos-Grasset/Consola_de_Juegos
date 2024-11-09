import pygame
import math
import random


pygame.init()


WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubble Shooter")


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (57, 255, 20),  # Verde neón
    (255, 20, 147),  # Rosa neón
    (0, 255, 255),  # Cian neón
    (255, 140, 0),  # Naranja neón
    (255, 255, 0)  # Amarillo neón
]
LIGHT_BLUE = (186, 85, 211) # Azul claro


BUBBLE_RADIUS = 20
LAUNCHER_X, LAUNCHER_Y = WIDTH // 2, HEIGHT - 50
LAUNCH_SPEED = 10


MAX_ROWS = 10  

clock = pygame.time.Clock()


font = pygame.font.Font(None, 30)


shoot_sound = pygame.mixer.Sound("sonidos/shoot.wav")
collision_sound = pygame.mixer.Sound("sonidos/bubble.wav")
remove_sound = pygame.mixer.Sound("sonidos/explosion.wav")


background = pygame.image.load('img/fondo1.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


class Bubble(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface([BUBBLE_RADIUS * 2 + 20, BUBBLE_RADIUS * 2 + 20], pygame.SRCALPHA)
        for i in range(5):
            alpha = max(0, 200 - i * 60)
            pygame.draw.circle(self.image, (255, 255, 255, alpha), (BUBBLE_RADIUS + 10, BUBBLE_RADIUS + 10),
                               BUBBLE_RADIUS + 10 + i * 2)
        pygame.draw.circle(self.image, color, (BUBBLE_RADIUS + 10, BUBBLE_RADIUS + 10), BUBBLE_RADIUS)
        self.rect = self.image.get_rect(center=(x, y))
        self.color = color
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x = -self.speed_x


class Button:
    def __init__(self, text, pos, size, color):
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.pos = pos
        self.size = size
        self.color = color
        self.rect = pygame.Rect(pos, size)
        self.hover_color = (255, 215, 0) 

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered():
            return True
        return False


def crear_cuadricula():
    grid = []
    for row in range(MAX_ROWS):
        current_row = []
        for col in range(row + 1):
            x = (WIDTH // 2) + (col - row / 2) * BUBBLE_RADIUS * 2
            y = row * BUBBLE_RADIUS * 2 + BUBBLE_RADIUS
            color = random.choice(COLORS)
            bubble = Bubble(x, y, color)
            current_row.append(bubble)
        grid.append(current_row)
    return grid


def dibujar_cuadricula(grid):
    for row in grid:
        for bubble in row:
            if bubble:
                screen.blit(bubble.image, bubble.rect)


def get_neighbors(row, col, grid):
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < len(grid) and 0 <= c < len(grid[r]) and grid[r][c] is not None:
            neighbors.append((r, c))
    return neighbors


def encontrar_burbujas_conectadas(row, col, color, grid, visited=None):
    if visited is None:
        visited = set()
    visited.add((row, col))
    for r, c in get_neighbors(row, col, grid):
        if (r, c) not in visited and grid[r][c].color == color:
            encontrar_burbujas_conectadas(r, c, color, grid, visited)
    return visited


def remover_conectadas(row, col, grid, bubbles):
    color = grid[row][col].color
    connected = encontrar_burbujas_conectadas(row, col, color, grid)
    if len(connected) >= 3:
        for r, c in connected:
            grid[r][c] = None
            bubbles.remove(grid[r][c])
        return True
    return False


def verificar_colision(bubble, grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            target = grid[row][col]
            if target:
                distance = math.hypot(bubble.rect.centerx - target.rect.centerx,
                                      bubble.rect.centery - target.rect.centery)
                if distance < BUBBLE_RADIUS * 2:
                    return row, col
    return None


def disparar_burbuja(angle, color):
    bubble = Bubble(LAUNCHER_X, LAUNCHER_Y, color)
    bubble.speed_x = LAUNCH_SPEED * math.cos(angle)
    bubble.speed_y = -LAUNCH_SPEED * math.sin(angle)
    return bubble


def dibujar_lanzador(angle, bubble_color):
    guide_length = 250  
    num_dots = 20 
    for i in range(1, num_dots + 1):
        guide_x = LAUNCHER_X + (guide_length * i / num_dots) * math.cos(angle)
        guide_y = LAUNCHER_Y - (guide_length * i / num_dots) * math.sin(angle)
        pygame.draw.circle(screen, WHITE, (int(guide_x), int(guide_y)), 3) 
    loaded_bubble = Bubble(LAUNCHER_X, LAUNCHER_Y + 30, bubble_color)
    screen.blit(loaded_bubble.image, loaded_bubble.rect)



def mostrar_mensaje_bienvenida():
    welcome_text = font.render("¡Bienvenido a Bubble Shooter!", True, WHITE)
    text_rect = welcome_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(welcome_text, text_rect)

    start_button = Button("Iniciar Juego", (WIDTH // 2 - 100, HEIGHT // 2 + 20), (200, 50), (0, 128, 0))


    waiting = True
    while waiting:
        screen.fill(BLACK)
        screen.blit(welcome_text, text_rect)
        start_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and start_button.is_hovered():
                waiting = False

        
        if start_button.is_hovered():
            start_button.color = start_button.hover_color
        else:
            start_button.color = (0, 128, 0)

        pygame.display.flip()


def create_grid(level):
    grid = []
    if level == 1:  
        for row in range(MAX_ROWS):
            current_row = []
            for col in range(row + 1):
                x = (WIDTH // 2) + (col - row / 2) * BUBBLE_RADIUS * 2
                y = row * BUBBLE_RADIUS * 2 + BUBBLE_RADIUS
                color = random.choice(COLORS)
                bubble = Bubble(x, y, color)
                current_row.append(bubble)
            grid.append(current_row)

    elif level == 2:  
        center_x, center_y = WIDTH // 2, HEIGHT // 4
        radius_increment = BUBBLE_RADIUS * 1.4 

      
        for ring in range(1, 9): 
            current_ring = []
            radius = ring * radius_increment
            bubble_count = int(2 * math.pi * radius / (BUBBLE_RADIUS * 2.5))  
            angle_increment = 360 / bubble_count

            for i in range(bubble_count):
                angle = math.radians(i * angle_increment)
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)

                color = random.choice(COLORS)
                bubble = Bubble(x, y, color)
                current_ring.append(bubble)

            grid.append(current_ring)


    elif level == 3: 
        rect_width = 400  
        rect_height = 200  
        rows = 10  
        cols = 15  
        bubble_diameter = BUBBLE_RADIUS * 2  

       
        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        offset_x = (rect_width - (cols * bubble_diameter)) // 2 + 20
        offset_y = (rect_height - (rows * bubble_diameter)) // 2 - 150 

        
        for row in range(rows):
            for col in range(cols):
              
                x = center_x - rect_width // 2 + col * bubble_diameter  + offset_x
                y = center_y - rect_height // 2 + row * bubble_diameter + offset_y
                color = random.choice(COLORS)
                bubble = Bubble(x, y, color)
                grid.append([bubble]) 
    return grid



def show_level_menu():
    screen.fill(BLACK)
    screen.blit(background, (0, 0))
    level_text = font.render("Seleccione un nivel", True, WHITE)
    text_rect = level_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(level_text, text_rect)

    level1_button = Button("Nivel 1", (WIDTH // 2 - 100, HEIGHT // 2), (200, 50), (0, 128, 0))
    level2_button = Button("Nivel 2", (WIDTH // 2 - 100, HEIGHT // 2 + 60), (200, 50), (0, 128, 128))
    level3_button = Button("Nivel 3", (WIDTH // 2 - 100, HEIGHT // 2 + 120), (200, 50), (128, 0, 128))

 
    waiting = True
    selected_level = None
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if level1_button.handle_event(event):
                selected_level = 1
                waiting = False
            elif level2_button.handle_event(event):
                selected_level = 2
                waiting = False
            elif level3_button.handle_event(event):
                selected_level = 3
                waiting = False

      
        level1_button.color = level1_button.hover_color if level1_button.is_hovered() else (0, 128, 0)
        level2_button.color = level2_button.hover_color if level2_button.is_hovered() else (0, 128, 128)
        level3_button.color = level3_button.hover_color if level3_button.is_hovered() else (128, 0, 128)

   
        screen.fill(BLACK)
        screen.blit(level_text, text_rect)
        level1_button.draw()
        level2_button.draw()
        level3_button.draw()
        pygame.display.flip()

    return selected_level




def show_final_message(score):

    screen.fill(BLACK)
    final_text = font.render("Nivel terminado", True, WHITE)
    score_text = font.render(f"Puntuación Final: {score}", True, WHITE)
    final_rect = final_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))


    screen.blit(final_text, final_rect)
    screen.blit(score_text, score_rect)
    pygame.display.flip()


    pygame.time.wait(3000) 

def main():
    running = True
    score = 0  
    start_time = pygame.time.get_ticks() 
    game_duration = 60 * 1000 

    while running:
        mostrar_mensaje_bienvenida() 
        
        level = show_level_menu()  # Mostrar menú de selección de nivel
        

        grid = create_grid(level)
        current_bubble_color = random.choice(COLORS)
        bubbles = pygame.sprite.Group()
        current_bubble = None
        shooting = False
        angle = math.pi / 2  

        exit_button = Button("Salir", (WIDTH - 105, HEIGHT - 55), (100, 50), (255, 0, 0))

     
        game_running = True
        while game_running:
            screen.fill(LIGHT_BLUE) 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                    running = False 
                    break

                
                if exit_button.handle_event(event):
                   game_running = False 
                   break  

                if event.type == pygame.MOUSEBUTTONDOWN and not shooting:
                    mouse_x, mouse_y = event.pos
                    angle = math.atan2(LAUNCHER_Y - mouse_y, mouse_x - LAUNCHER_X)
                    current_bubble = disparar_burbuja(angle, current_bubble_color)
                    shooting = True
                    shoot_sound.play()

           
            elapsed_time = pygame.time.get_ticks() - start_time
            time_left = max(0, (game_duration - elapsed_time) // 1000)

           
            if time_left == 0:
                game_running = False

          
            if shooting:
                current_bubble.update()
                collision = verificar_colision(current_bubble, grid)

                if collision:
                    row, col = collision
                    if remover_conectadas(row, col, grid, bubbles):
                        score += 10  
                        current_bubble = None
                        remove_sound.play()
                    else:
                        grid[row][col] = current_bubble 
                        current_bubble = None
                        collision_sound.play()
                    shooting = False
                    current_bubble_color = random.choice(COLORS)

         
            dibujar_cuadricula(grid)
            if current_bubble:
                screen.blit(current_bubble.image, current_bubble.rect)
            dibujar_lanzador(angle, current_bubble_color)
            exit_button.draw()

           
            score_text = font.render(f"Puntuación: {score}", True, WHITE)
            time_text = font.render(f"Tiempo: {time_left}", True, WHITE)
            screen.blit(score_text, (10, 10)) 
            screen.blit(time_text, (WIDTH - 120, 10))  

            pygame.display.flip()
            clock.tick(60)

        show_final_message(score) #

    pygame.quit()


if __name__ == "__main__":
    main()
import pygame
import random

pygame.init()

# musica y sonidos
pygame.mixer.music.load("musicaFondo.mp3")
pygame.mixer.music.play(-1)  # Reproducir en bucle

sonido_comer = pygame.mixer.Sound("pop.mp3")
sonido_choque = pygame.mixer.Sound("thud.mp3")

# colores
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)

# tamaño de la pantalla
ANCHO = 1000
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Snake con 10 niveles")

# el obstaculo
TAMANO_CUADRADO = 20

# configuraciones iniciales
velocidad = 5
vidas = 2
puntuacion = 0
nivel = 1
obstaculos = []

# sepiente inicialmente
serpiente = [(100, 100), (80, 100), (60, 100)]
direccion_serpiente = pygame.K_RIGHT

# generar comida
comida = (random.randint(0, (ANCHO // TAMANO_CUADRADO) - 1) * TAMANO_CUADRADO,
          random.randint(0, (ALTO // TAMANO_CUADRADO) - 1) * TAMANO_CUADRADO)

reloj = pygame.time.Clock()


# pantalla de inicio
def mostrar_pantalla_inicio():
    pantalla.fill(NEGRO)
    
    imagen_titulo = pygame.image.load("snake.png")
    pantalla.blit(imagen_titulo, ((ANCHO - imagen_titulo.get_width()) // 2, ALTO // 2 - 220))

    fuente_pequena = pygame.font.Font(None, 36)
    texto_instrucciones = fuente_pequena.render("Usa las flechas para moverte. Evita obstáculos y come la comida.", True, AMARILLO)
    texto_iniciar = fuente_pequena.render("Presiona cualquier tecla para empezar", True, ROJO)
    pantalla.blit(texto_instrucciones, (ANCHO // 8, ALTO // 2))
    pantalla.blit(texto_iniciar, (ANCHO // 4, ALTO // 2 + 50))

    pygame.display.flip()
    esperar_inicio()


# iniciar el juego
def esperar_inicio():
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                esperando = False


# como es la serpiente
def dibujar_serpiente():
    for segmento in serpiente:
        pygame.draw.rect(pantalla, VERDE, (segmento[0], segmento[1], TAMANO_CUADRADO, TAMANO_CUADRADO))


# como es la comida
def dibujar_comida():
    pygame.draw.rect(pantalla, ROJO, (comida[0], comida[1], TAMANO_CUADRADO, TAMANO_CUADRADO))


# como es los obstaculos
def dibujar_obstaculos():
    for obstaculo in obstaculos:
        pygame.draw.rect(pantalla, AZUL, obstaculo)


# moviemineto de la serpiente
def mover_serpiente():
    global comida, puntuacion, velocidad, nivel, obstaculos
    cabeza_x, cabeza_y = serpiente[0]

    if direccion_serpiente == pygame.K_UP:
        nueva_cabeza = (cabeza_x, cabeza_y - TAMANO_CUADRADO)
    elif direccion_serpiente == pygame.K_DOWN:
        nueva_cabeza = (cabeza_x, cabeza_y + TAMANO_CUADRADO)
    elif direccion_serpiente == pygame.K_LEFT:
        nueva_cabeza = (cabeza_x - TAMANO_CUADRADO, cabeza_y)
    elif direccion_serpiente == pygame.K_RIGHT:
        nueva_cabeza = (cabeza_x + TAMANO_CUADRADO, cabeza_y)

    nueva_cabeza = (
        nueva_cabeza[0] % ANCHO,  # pared 
        nueva_cabeza[1] % ALTO
    )

    serpiente.insert(0, nueva_cabeza)

    if serpiente[0] == comida:
        sonido_comer.play()  
        puntuacion += 10
        comida = (random.randint(0, (ANCHO // TAMANO_CUADRADO) - 1) * TAMANO_CUADRADO,
                  random.randint(0, (ALTO // TAMANO_CUADRADO) - 1) * TAMANO_CUADRADO)

        if puntuacion % 50 == 0:
            nivel += 1
            if nivel > 10:
                mostrar_pantalla_victoria()
                return
            velocidad += 1
            if nivel >= 3:
               
                obstaculo_x = random.randint(0, (ANCHO // TAMANO_CUADRADO) - 3) * TAMANO_CUADRADO
                obstaculo_y = random.randint(0, (ALTO // TAMANO_CUADRADO) - 3) * TAMANO_CUADRADO
                obstaculos.append(pygame.Rect(obstaculo_x, obstaculo_y, TAMANO_CUADRADO * 2, TAMANO_CUADRADO * 2))
    else:
        serpiente.pop()


# comprobar colisiones
def comprobar_colisiones():
    cabeza_x, cabeza_y = serpiente[0]

    if serpiente[0] in serpiente[1:]:
        sonido_choque.play()  
        return True

    for obstaculo in obstaculos:
        if obstaculo.collidepoint(cabeza_x, cabeza_y):
            sonido_choque.play()  
            return True

    return False


# mostrar puntuación, vidas y nivel
def mostrar_informacion():
    fuente = pygame.font.Font(None, 36)
    texto_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, AMARILLO)
    texto_vidas = fuente.render(f"Vidas: {vidas}", True, AMARILLO)
    texto_nivel = fuente.render(f"Nivel: {nivel}", True, AMARILLO)
    pantalla.blit(texto_puntuacion, (10, 10))
    pantalla.blit(texto_vidas, (ANCHO - 120, 10))
    pantalla.blit(texto_nivel, (ANCHO // 2 - 40, 10))


# pantalla de victoria
def mostrar_pantalla_victoria():
    pantalla.fill(NEGRO)
    fuente = pygame.font.Font(None, 74)
    texto_victoria = fuente.render("¡GANASTE! Eres el mejor ", True, VERDE)
    pantalla.blit(texto_victoria, (ANCHO // 6, ALTO // 2 - 50))
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()

# pantalla de pérdida
def mostrar_pantalla_perdida():
    pantalla.fill(NEGRO)
    fuente = pygame.font.Font(None, 74)
    texto_perdida = fuente.render("¡PERDISTE! Intenta de nuevo", True, ROJO)
    pantalla.blit(texto_perdida, (ANCHO // 6, ALTO // 2 - 50))
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()
# bucle del juego
def game_loop():
    global direccion_serpiente, vidas, velocidad

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    direccion_serpiente = evento.key

        mover_serpiente()

        if comprobar_colisiones():
            vidas -= 1
            if vidas == 0:
                print("¡Juego terminado!")
                corriendo = False
            else:
                serpiente.clear()
                serpiente.extend([(100, 100), (80, 100), (60, 100)])

        pantalla.fill(NEGRO)
        dibujar_serpiente()
        dibujar_comida()
        dibujar_obstaculos()
        mostrar_informacion()
        pygame.display.flip()

        reloj.tick(velocidad)

    pygame.quit()


# iniciar el juego mostrando la pantalla de bienvenida
mostrar_pantalla_inicio()
game_loop()

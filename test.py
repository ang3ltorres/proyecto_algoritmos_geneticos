import pygame
import numpy as np
import random

# Inicializar Pygame
pygame.init()

# Definir dimensiones de la ventana
ANCHO = 800  # Aumentar ancho
ALTO = 800   # Aumentar alto
CELDAS = 10  # Mantener el tamaño de la matriz 10x10
TAM_CELDA = ANCHO // CELDAS  # Redefinir el tamaño de las celdas

# Colores
VERDE = (34, 177, 76)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (169, 169, 169)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)  # Color del zorro (punto naranja)

# Definir la cantidad de conejos por celda (matriz 10x10)
conejosPorHectarea = np.array([
    [10, 12, 15, 14, 11, 13, 17, 16, 19, 18],
    [22, 21, 23, 24, 20, 25, 26, 28, 27, 29],
    [18, 17, 15, 14, 12, 11, 10, 16, 13, 19],
    [20, 22, 21, 25, 24, 23, 27, 26, 29, 28],
    [15, 14, 13, 11, 12, 10, 17, 16, 19, 18],
    [22, 21, 20, 24, 25, 23, 28, 26, 29, 27],
    [10, 12, 11, 13, 14, 15, 16, 17, 18, 19],
    [21, 22, 23, 24, 25, 26, 27, 28, 29, 20],
    [19, 18, 17, 16, 15, 14, 13, 12, 11, 10],
    [29, 28, 27, 26, 25, 24, 23, 22, 21, 20]
])

# Matriz de zorros (1 indica la presencia de un zorro en la celda)
matrizZorros = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
])

# Crear la ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mundo Cuadriculado con Conejos y Zorros")

# Fuente para renderizar texto
fuente = pygame.font.Font(None, 36)

# Clase para representar un conejo
class Conejo:
    def __init__(self, celda_x, celda_y):
        self.x = random.randint(0, TAM_CELDA - 1) + celda_x * TAM_CELDA
        self.y = random.randint(0, TAM_CELDA - 1) + celda_y * TAM_CELDA
        self.celda_x = celda_x
        self.celda_y = celda_y

    def mover(self):
        # Los conejos se moverán aleatoriamente dentro de su celda
        direccion = random.choice(['izquierda', 'derecha', 'arriba', 'abajo'])
        if direccion == 'izquierda' and self.x > self.celda_x * TAM_CELDA:
            self.x -= 1
        elif direccion == 'derecha' and self.x < (self.celda_x + 1) * TAM_CELDA - 1:
            self.x += 1
        elif direccion == 'arriba' and self.y > self.celda_y * TAM_CELDA:
            self.y -= 1
        elif direccion == 'abajo' and self.y < (self.celda_y + 1) * TAM_CELDA - 1:
            self.y += 1

    def dibujar(self, superficie):
        pygame.draw.circle(superficie, BLANCO, (self.x, self.y), 3)

# Clase para representar un zorro
class Zorro:
    def __init__(self, celda_x, celda_y):
        self.x = random.randint(0, TAM_CELDA - 1) + celda_x * TAM_CELDA
        self.y = random.randint(0, TAM_CELDA - 1) + celda_y * TAM_CELDA
        self.celda_x = celda_x
        self.celda_y = celda_y

    def mover(self, conejos, contador_conejos_eliminados):
        # Mover al zorro hacia un conejo de su celda si hay alguno
        for conejo in conejos:
            if conejo.celda_x == self.celda_x and conejo.celda_y == self.celda_y:
                # Mover al zorro hacia la posición del conejo
                if self.x < conejo.x:
                    self.x += 1
                elif self.x > conejo.x:
                    self.x -= 1

                if self.y < conejo.y:
                    self.y += 1
                elif self.y > conejo.y:
                    self.y -= 1

                # Verificar si el zorro "come" al conejo (cuando tocan)
                if self.x == conejo.x and self.y == conejo.y:
                    conejos.remove(conejo)
                    contador_conejos_eliminados[0] += 1  # Incrementar el contador
                break

    def dibujar(self, superficie):
        pygame.draw.circle(superficie, NARANJA, (self.x, self.y), 5)

# Crear el mundo con conejos y zorros
def crear_mundo():
    conejos = []
    zorros = []
    
    for fila in range(CELDAS):
        for col in range(CELDAS):
            # Crear conejos
            cantidad_conejos = conejosPorHectarea[fila][col]
            for _ in range(cantidad_conejos):
                conejos.append(Conejo(col, fila))
            
            # Crear zorros si hay un 1 en la matriz de zorros
            if matrizZorros[fila][col] == 1:
                zorros.append(Zorro(col, fila))

    return conejos, zorros

# Función para dibujar el mundo, conejos y zorros
def dibujar_mundo(conejos, zorros, contador_conejos_eliminados):
    pantalla.fill(VERDE)
    
    # Dibujar la cuadrícula
    for fila in range(CELDAS):
        for col in range(CELDAS):
            pygame.draw.line(pantalla, NEGRO, (0, fila * TAM_CELDA), (ANCHO, fila * TAM_CELDA))
            pygame.draw.line(pantalla, NEGRO, (col * TAM_CELDA, 0), (col * TAM_CELDA, ALTO))
    
    # Dibujar conejos
    for conejo in conejos:
        conejo.dibujar(pantalla)
    
    # Dibujar zorros
    for zorro in zorros:
        zorro.dibujar(pantalla)

    # Dibujar el contador de conejos eliminados
    texto = fuente.render(f"Conejos eliminados: {contador_conejos_eliminados[0]}", True, NEGRO)
    pantalla.blit(texto, (10, 10))

# Ejecutar el juego
corriendo = True
contador_conejos_eliminados = [0]  # Lista para contar los conejos eliminados (mutable)

conejos, zorros = crear_mundo()

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
    
    # Mover zorros y conejos
    for zorro in zorros:
        zorro.mover(conejos, contador_conejos_eliminados)
    for conejo in conejos:
        conejo.mover()
    
    # Dibujar el mundo
    dibujar_mundo(conejos, zorros, contador_conejos_eliminados)

    # Actualizar pantalla
    pygame.display.flip()


# Salir de Pygame
pygame.quit()
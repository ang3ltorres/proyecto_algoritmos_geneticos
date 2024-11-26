# simulacion.py
import pygame
import random


class SimulacionPrueba:
    def __init__(self, ancho, alto, celdas, conejos_por_hectarea, matriz_zorros, generacion):
        # Inicialización
        self.generacion = generacion
        self.ancho = ancho
        self.alto = alto
        self.celdas = celdas
        self.conejos_por_hectarea = conejos_por_hectarea
        self.matriz_zorros = matriz_zorros
        self.tam_celda = ancho // celdas
        self.conejos = []
        self.zorros = []
        self.contador_conejos_eliminados = [0]
        self.verde = (34, 177, 76)
        self.negro = (0, 0, 0)
        self.blanco = (255, 255, 255)
        self.naranja = (255, 165, 0)

        pygame.init()
        self.pantalla = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Simulación de Conejos y Zorros")
        self.fuente = pygame.font.Font(None, 36)
        self.crear_mundo()

    def crear_mundo(self):
        for fila in range(self.celdas):
            for col in range(self.celdas):
                cantidad_conejos = self.conejos_por_hectarea[fila][col]
                for _ in range(cantidad_conejos):
                    self.conejos.append(self.Conejo(col, fila, self.tam_celda, self.blanco))
                if self.matriz_zorros[fila][col] == 1:
                    self.zorros.append(self.Zorro(col, fila, self.tam_celda, self.naranja))

    def dibujar_mundo(self):
        self.pantalla.fill(self.verde)
        for fila in range(self.celdas):
            for col in range(self.celdas):
                pygame.draw.line(self.pantalla, self.negro, (0, fila * self.tam_celda), (self.ancho, fila * self.tam_celda))
                pygame.draw.line(self.pantalla, self.negro, (col * self.tam_celda, 0), (col * self.tam_celda, self.alto))
        for conejo in self.conejos:
            conejo.dibujar(self.pantalla)
        for zorro in self.zorros:
            zorro.dibujar(self.pantalla)
        texto = self.fuente.render(f"Fitness: {self.contador_conejos_eliminados[0]}", True, self.negro)
        self.pantalla.blit(texto, (10, 10))
        texto = self.fuente.render(f"Generacion: {self.generacion}", True, self.negro)
        self.pantalla.blit(texto, (10, 40))

    def ejecutar(self):
        corriendo = True
        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
            for zorro in self.zorros:
                zorro.mover(self.conejos, self.contador_conejos_eliminados)
            for conejo in self.conejos:
                conejo.mover()
            self.dibujar_mundo()
            pygame.display.flip()
        pygame.quit()

    class Conejo:
        def __init__(self, celda_x, celda_y, tam_celda, color):
            self.x = random.randint(0, tam_celda - 1) + celda_x * tam_celda
            self.y = random.randint(0, tam_celda - 1) + celda_y * tam_celda
            self.celda_x = celda_x
            self.celda_y = celda_y
            self.tam_celda = tam_celda  # Guardar tam_celda como atributo
            self.color = color

        def mover(self):
            direccion = random.choice(['izquierda', 'derecha', 'arriba', 'abajo'])
            if direccion == 'izquierda' and self.x > self.celda_x * self.tam_celda:
                self.x -= 1
            elif direccion == 'derecha' and self.x < (self.celda_x + 1) * self.tam_celda - 1:
                self.x += 1
            elif direccion == 'arriba' and self.y > self.celda_y * self.tam_celda:
                self.y -= 1
            elif direccion == 'abajo' and self.y < (self.celda_y + 1) * self.tam_celda - 1:
                self.y += 1

        def dibujar(self, superficie):
            pygame.draw.circle(superficie, self.color, (self.x, self.y), 3)

    class Zorro:
        def __init__(self, celda_x, celda_y, tam_celda, color):
            self.x = random.randint(0, tam_celda - 1) + celda_x * tam_celda
            self.y = random.randint(0, tam_celda - 1) + celda_y * tam_celda
            self.celda_x = celda_x
            self.celda_y = celda_y
            self.color = color

        def mover(self, conejos, contador_conejos_eliminados):
                for conejo in conejos:
                    if conejo.celda_x == self.celda_x and conejo.celda_y == self.celda_y:
                        if self.x < conejo.x:
                            self.x += 1
                        elif self.x > conejo.x:
                            self.x -= 1

                        if self.y < conejo.y:
                            self.y += 1
                        elif self.y > conejo.y:
                            self.y -= 1

                        if self.x == conejo.x and self.y == conejo.y:
                            conejos.remove(conejo)
                            contador_conejos_eliminados[0] += 1
                        break
        def dibujar(self, superficie):
            pygame.draw.circle(superficie, self.color, (self.x, self.y), 5)

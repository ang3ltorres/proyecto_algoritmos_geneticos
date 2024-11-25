import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import numpy
import math
import enum
import sys
from enum import IntEnum
from random import random, choice, uniform, randrange

# Globales
tileSize: int = 16
pantallaAncho: int = 1280
pantallaAlto: int = 720

alto: int = 0
ancho: int = 0

# Recursos
textureAtlas: pygame.Surface = None
fuenteDefault: pygame.font.Font = None

# Datos
zorrosPerdidos: int = None
tiempoDeCaza: int = None

class Camera:

	def __init__(self):

		self.x: int = 0
		self.y: int = 0

	def update(self):

		if pygame.mouse.get_pressed()[0]:
			mouse_movement = pygame.mouse.get_rel()
			self.x -= mouse_movement[0]
			self.y -= mouse_movement[1]
		else:
			pygame.mouse.get_rel()

	def get_camera_rect(self):

		global pantallaAncho, pantallaAlto
		return pygame.Rect(self.x, self.y, pantallaAncho, pantallaAlto)

class Entity(pygame.sprite.Sprite):

	class ANIMATION(IntEnum):
		IDLE = 0
		RUNNING = 1
		ACTION = 2

	def __init__(self, x, y):
		super().__init__()

		# Variables para la animacion
		self.spriteAncho: int = 32
		self.spriteAlto: int = 32

		self.frameActual: int = 0
		self.frameFila: int = 0
		self.frameTotal: int = 0
		self.frameVelocidad: int = 0
		self.frameVelocidadContador: int = 0
		
		# Porcion de textura
		self.image: pygame.Surface = textureAtlas.subsurface((0, 0, 32, 32))

		# Rectangulo
		self.rect: pygame.Rect = pygame.Rect((x, y, 32, 32))

		# Caracteristicas
		self.velocidad: int = 0

		# Movimiento random
		self.direccionActual: int = 0
		self.direccionTiempo: int = None
		self.direccionContadorTiempo: int = None

		self.direccionActual: int = uniform(0, 360)
		self.dx: float = math.cos(math.radians(self.direccionActual)) * self.velocidad
		self.dy: float = math.sin(math.radians(self.direccionActual)) * self.velocidad

	def update(self):
		
		# Actualizar animacion
		self.frameVelocidadContador += 1
		if self.frameVelocidadContador >= self.frameVelocidad:
			self.frameVelocidadContador = 0
			self.frameActual += 1
			if self.frameActual >= self.frameTotal:
				self.frameActual = 0
		
		rect: pygame.Rect = pygame.Rect(self.frameActual * self.spriteAncho, self.frameFila * self.spriteAlto, self.spriteAncho, self.spriteAlto)
		self.image = textureAtlas.subsurface(rect)

	def draw(self, pantalla: pygame.display, screen_pos: pygame.math.Vector2):
		pantalla.blit(self.image, screen_pos)

	def setAnimacion(self, animacion: ANIMATION):
		self.frameActual = 0
		self.frameVelocidadContador = 0

def distancia(a: Entity, b: Entity):

	# Calcular la posicion del centro de cada rectangulo
	centro_a = a.rect.center
	centro_b = b.rect.center

	# Calcular la distancia entre los centros
	return math.sqrt((centro_a[0] - centro_b[0]) ** 2 + (centro_a[1] - centro_b[1]) ** 2)

class Conejo(Entity):

	def __init__(self, x, y):
		super().__init__(x, y)
		self.setAnimacion(self.ANIMATION.RUNNING)

		# Caracteristicas
		self.velocidad: int = 1.5

		# Movimiento random
		self.direccionTiempo: int = 120
		self.direccionContadorTiempo: int = randrange(0, self.direccionTiempo, 1)

		# Rectangulo
		self.rect = pygame.Rect((x, y, 15, 12))

	def update(self):

		global ancho, alto, tileSize

		self.direccionContadorTiempo += 1
		if (self.direccionContadorTiempo >= self.direccionTiempo):
			
			self.direccionContadorTiempo = randrange(0, self.direccionTiempo, 1)
			
			if (self.rect.x < 0 or self.rect.y < 0 or self.rect.x > (ancho * tileSize) or self.rect.y > (alto * tileSize)):
				# Calcular la direccion en grados hacia el centro
				self.direccionActual = math.degrees(math.atan2(((alto * tileSize) // 2) - self.rect.y, ((ancho * tileSize) // 2) - self.rect.x))
			else:
				# Setear direccion aleatoria
				self.direccionActual = uniform(0, 360)

			# Convertir la direccion en movimiento
			self.dx = math.cos(math.radians(self.direccionActual)) * self.velocidad
			self.dy = math.sin(math.radians(self.direccionActual)) * self.velocidad

		# Mover al conejo en la direccion
		self.rect.x += int(self.dx)
		self.rect.y += int(self.dy)

		super().update()

	def draw(self, pantalla: pygame.display, camera: Camera):

		screen_pos = pygame.math.Vector2(self.rect.topleft) - pygame.math.Vector2(camera.x, camera.y)

		# Dibujar el radio
		# pygame.draw.circle(pantalla, (0, 0, 255), screen_pos, self.rango, 1)

		# Dibujar rectangulo de colision
		# pygame.draw.rect(pantalla, (255, 0, 0), self.rect.move(-camera.x, -camera.y))

		super().draw(pantalla, screen_pos)

	def setAnimacion(self, animacion):
		super().setAnimacion(animacion)
		
		match animacion:
			case self.ANIMATION.RUNNING:
				self.frameFila = 0
				self.frameTotal = 4
				self.frameVelocidad = 3

class Zorro(Entity):

	def __init__(self, x, y):
		super().__init__(x, y)
		self.setAnimacion(self.ANIMATION.RUNNING)

		# Caracteristicas
		self.velocidad: int = 3
		self.rangoPelea: int = 64

		# Movimiento random
		self.direccionTiempo: int = 90
		self.direccionContadorTiempo: int = randrange(0, self.direccionTiempo, 1)

		# Rectangulo
		self.rect = pygame.Rect((x, y, 21, 16))

	def update(self, grupoConejos: pygame.sprite.Group, grupoZorros: pygame.sprite.Group):

		global ancho, alto, tileSize, zorrosPerdidos

		# Encontrar el zorro mas cercano dentro del rango
		zorros_detectados = [z for z in grupoZorros if z != self and distancia(self, z) <= self.rangoPelea]
		if zorros_detectados:
			zorro_cercano = min(zorros_detectados, key=lambda z: distancia(self, z))
			dx = zorro_cercano.rect.x - self.rect.x
			dy = zorro_cercano.rect.y - self.rect.y
			distancia_total = max(math.sqrt(dx ** 2 + dy ** 2), 0.1)
			
			# Moverse hacia el otro zorro
			self.rect.x += int((dx / distancia_total) * self.velocidad)
			self.rect.y += int((dy / distancia_total) * self.velocidad)

			# Atacar el otro zorro y decidir quien muere
			if (self.rect.colliderect(zorro_cercano.rect)):
				zorrosPerdidos += 1
				self.kill()
		# No hay zorro cercano
		else:
			# Encontrar el conejo mas cercano dentro del rango de caza
			conejos_detectados = [c for c in grupoConejos if distancia(self, c)]
			if conejos_detectados:
				conejo_cercano = min(conejos_detectados, key=lambda c: distancia(self, c))
				dx = conejo_cercano.rect.x - self.rect.x
				dy = conejo_cercano.rect.y - self.rect.y
				distancia_total = max(math.sqrt(dx ** 2 + dy ** 2), 0.1)

				# Moverse hacia el conejo
				self.rect.x += int((dx / distancia_total) * self.velocidad)
				self.rect.y += int((dy / distancia_total) * self.velocidad)

				# Comerse al conejo
				if (self.rect.colliderect(conejo_cercano.rect)):
						conejo_cercano.kill()

			# No hay zorros ni conejos
			# El zorro camina en direcciones aleatorias
			else:
				self.direccionContadorTiempo += 1
				if (self.direccionContadorTiempo >= self.direccionTiempo):
					
					self.direccionContadorTiempo = 0
					
					# Si se sale del mapa
					if (self.rect.x < 0 or self.rect.y < 0 or self.rect.x > (ancho * tileSize) or self.rect.y > (alto * tileSize)):
						# Calcular la direccion en grados hacia el centro
						self.direccionActual = math.degrees(math.atan2(((alto * tileSize) // 2) - self.rect.y, ((ancho * tileSize) // 2) - self.rect.x))
					else:
						# Setear direccion aleatoria
						self.direccionActual = uniform(0, 360)

					# Convertir la direccion en movimiento
					self.dx = math.cos(math.radians(self.direccionActual)) * self.velocidad
					self.dy = math.sin(math.radians(self.direccionActual)) * self.velocidad

				# Mover al zorro en la direccion
				self.rect.x += int(self.dx)
				self.rect.y += int(self.dy)

		super().update()

	def draw(self, pantalla: pygame.display, camera: Camera):
		screen_pos = pygame.math.Vector2(self.rect.topleft) - pygame.math.Vector2(camera.x, camera.y)

		# Dibujar el radio
		pygame.draw.circle(pantalla, (255, 0, 0), screen_pos, self.rangoPelea, 1)

		# Dibujar rectangulo de colision
		# pygame.draw.rect(pantalla, (255, 0, 0), self.rect.move(-camera.x, -camera.y))

		super().draw(pantalla, screen_pos)

	def setAnimacion(self, animacion):
		super().setAnimacion(animacion)
		
		match animacion:
			case self.ANIMATION.RUNNING:
				self.frameFila = 2
				self.frameTotal = 6
				self.frameVelocidad = 3

class Simulacion:

	# Cargar recursos principales
	def __init__(self):
		global tileSize, textureAtlas, fuenteDefault

		self.frecuenciaDibujado = 1

		pygame.init()
		textureAtlas = pygame.image.load("proyecto_algoritmos_geneticos/texture.png")
		fuenteDefault = pygame.font.SysFont("Consolas", 18)

	def draw(self):
		# Limpiar pantalla
		self.pantalla.fill((0, 0, 0))
		
		# Dibujar
		cam_rect = self.camera.get_camera_rect()

		# Terreno
		visible_area = cam_rect.clip((0, 0, ancho * tileSize, alto * tileSize))
		self.subSurfaceTerreno = self.surfaceTerreno.subsurface(visible_area)
		self.pantalla.blit(self.subSurfaceTerreno, (visible_area.left - cam_rect.x, visible_area.top - cam_rect.y))

		# Entidades que estan dentro de la camara
		conejo: Conejo
		for conejo in self.grupoConejos:
			if cam_rect.colliderect(conejo.rect):
				conejo.draw(self.pantalla, self.camera)

		zorro: Zorro
		for zorro in self.grupoZorros:
			if cam_rect.colliderect(zorro.rect):
				zorro.draw(self.pantalla, self.camera)
		
		pygame.display.flip()

	def run(self, posicionesZorros: numpy.ndarray, conejosPorHectarea: int) -> tuple[int, int]:
		global alto, ancho, zorrosPerdidos, tiempoDeCaza

		zorrosPerdidos = 0
		tiempoDeCaza = 0

		# Una hectarea igual a 16 cuadritos de 16 pixeles cada uno (256 PIXELES)
		alto, ancho = posicionesZorros.shape
		ancho *= 16
		alto *= 16

		# Inicializar
		self.clock = pygame.time.Clock()

		pygame.display.set_caption("Simulacion presa-depredador")
		self.pantalla = pygame.display.set_mode((pantallaAncho, pantallaAlto))

		self.grupoConejos = pygame.sprite.Group()
		self.conejosPorHectarea = conejosPorHectarea
		
		self.grupoZorros = pygame.sprite.Group()

		self.frameSkip = False
	
		for y in range(posicionesZorros.shape[0]):
			for x in range(posicionesZorros.shape[1]):

				# Crear conejos por hectarea
				for i in range(conejosPorHectarea):
					self.grupoConejos.add(Conejo((x * 256), (y * 256)))
				
				# Crear zorros en las posiciones dadas
				if (posicionesZorros[y, x] == 1):
					self.grupoZorros.add(Zorro(x * 256, y * 256))

		# Camara
		self.camera = Camera()

		# Crear la textura del pasto
		self.surfaceTerreno = pygame.Surface((ancho * tileSize, alto * tileSize), pygame.SRCALPHA)
		self.surfaceTerreno.fill((59, 150, 74))
		for x in range(ancho):
			for y in range(alto):
				# Pintar el pasto decorativo
				if random() < 0.05:
					self.surfaceTerreno.blit(textureAtlas, (x * tileSize, y * tileSize), (144 + (16 * choice(range(10))), 0, 16, 16))

		# Dibujar cuadricula
		width, height = self.surfaceTerreno.get_size()
		
		grid_size = 16*16
		for x in range(0, width, grid_size):
				pygame.draw.line(self.surfaceTerreno, (0, 128, 0), (x, 0), (x, height), 1)

		for y in range(0, height, grid_size):
				pygame.draw.line(self.surfaceTerreno, (0, 128, 0), (0, y), (width, y), 1)

		# Main loop
		self.frecuenciaDibujadoContador = 0

		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

				elif event.type == pygame.KEYDOWN:

					if event.key == pygame.K_RIGHT:
						self.frecuenciaDibujado += 1
					elif event.key == pygame.K_LEFT:
						self.frecuenciaDibujado = max(1, self.frecuenciaDibujado - 1)

			self.camera.update()
			
			# Actualizar sprites
			for conejo in self.grupoConejos:
				conejo.update()
			for zorro in self.grupoZorros:
				zorro.update(self.grupoConejos.sprites(), self.grupoZorros.sprites())

			# Si ya no hay conejos devolvemos los resultados
			if (self.grupoConejos.__len__() == 0):
				return [zorrosPerdidos, tiempoDeCaza / 60]
			
			# Tiempo
			tiempoDeCaza += 1
			
			# Dibujar
			self.frecuenciaDibujadoContador += 1
			if (self.frecuenciaDibujadoContador >= self.frecuenciaDibujado):
				
				self.frecuenciaDibujadoContador = 0
				if not self.frameSkip:
					self.draw()
			
			# self.clock.tick(0)

		# Si el usuario cierra la ventana antes de terminar
		return [0, 0]
import pygame
import numpy
import math
import enum
import sys
from enum import IntEnum
from random import random, choice, uniform, randrange

# Globales
tileSize = 16
pantallaAncho = 800
pantallaAlto = 600

alto = 0
ancho = 0

# Recursos
textureAtlas = None
fuenteDefault = None

class Camera:

	def __init__(self):

		self.x = 0
		self.y = 0

	def update(self):

		if pygame.mouse.get_pressed()[0]:
			mouse_movement = pygame.mouse.get_rel()
			self.x -= mouse_movement[0]
			self.y -= mouse_movement[1]
		else:
			pygame.mouse.get_rel()

class Entity(pygame.sprite.Sprite):

	class ANIMATION(IntEnum):
		IDLE = 0
		RUNNING = 1
		ACTION = 2

	def __init__(self, x, y):
		super().__init__()

		# Variables para la animacion
		self.spriteAncho = 32
		self.spriteAlto = 32

		self.frameActual = 0
		self.frameFila = 0
		self.frameTotal = 0
		self.frameVelocidad = 0
		self.frameVelocidadContador = 0
		
		# Porcion de textura
		self.image = textureAtlas.subsurface((0, 0, 32, 32))

		# Rectangulo
		self.rect = pygame.Rect((x, y, 32, 32))

		# Caracteristicas
		self.velocidad = 0

	def update(self):
		
		# Actualizar animacion
		self.frameVelocidadContador += 1
		if self.frameVelocidadContador >= self.frameVelocidad:
			self.frameVelocidadContador = 0
			self.frameActual += 1
			if self.frameActual >= self.frameTotal:
				self.frameActual = 0
		
		rect = pygame.Rect(self.frameActual * self.spriteAncho, self.frameFila * self.spriteAlto, self.spriteAncho, self.spriteAlto)
		self.image = textureAtlas.subsurface(rect)

	def draw(self, pantalla: pygame.display, camera: Camera):
		pass

	def setAnimacion(self, animacion: ANIMATION):
		self.frameActual = 0
		self.frameVelocidadContador = 0

# Distancia entre 2 entidates
def distancia(a: Entity, b: Entity):
	return math.sqrt((a.rect.x - b.rect.x) ** 2 + (a.rect.y - b.rect.y) ** 2)

class Conejo(Entity):

	def __init__(self, x, y):
		super().__init__(x, y)
		self.setAnimacion(self.ANIMATION.RUNNING)
		self.velocidad = 2
		self.rango = 128

	def update(self, grupoZorros: pygame.sprite.Group):

		# Encontrar el zorro más cercano dentro del rango
		zorros_detectados = [z for z in grupoZorros if distancia(self, z) <= self.rango]
		if zorros_detectados:
			zorro_cercano = min(zorros_detectados, key=lambda z: distancia(self, z))
			dx = self.rect.x - zorro_cercano.rect.x
			dy = self.rect.y - zorro_cercano.rect.y
			distancia_total = max(math.sqrt(dx ** 2 + dy ** 2), 0.1)

			# Huir
			self.rect.x += int((dx / distancia_total) * self.velocidad)
			self.rect.y += int((dy / distancia_total) * self.velocidad)

		super().update()

	def draw(self, pantalla: pygame.display, camera: Camera):

		screen_pos = pygame.math.Vector2(self.rect.topleft) - pygame.math.Vector2(camera.x, camera.y)
		pygame.draw.circle(pantalla, (255, 0, 0), screen_pos, self.rango, 1)
		pantalla.blit(self.image, screen_pos)

	def setAnimacion(self, animacion):
		super().setAnimacion(animacion)
		
		match animacion:
			case self.ANIMATION.IDLE:
				self.frameFila = 0
				self.frameTotal = 2
				self.frameVelocidad = 8
			case self.ANIMATION.RUNNING:
				self.frameFila = 1
				self.frameTotal = 4
				self.frameVelocidad = 3
			case self.ANIMATION.ACTION:
				self.frameFila = 3
				self.frameTotal = 10
				self.frameVelocidad = 24

class Zorro(Entity):

	def __init__(self, x, y):
		super().__init__(x, y)
		self.setAnimacion(self.ANIMATION.RUNNING)
		self.velocidad = 3
		self.rangoPelea = 128
		self.rangoCaza = 128 * 3

		# Movimiento random
		self.direccionActual = 0
		self.direccionTiempo = 90
		self.direccionContadorTiempo = randrange(0, self.direccionTiempo, 1)

		self.direccionActual = uniform(0, 360)
		self.dx = math.cos(math.radians(self.direccionActual)) * self.velocidad
		self.dy = math.sin(math.radians(self.direccionActual)) * self.velocidad

	def update(self, grupoConejos: pygame.sprite.Group, grupoZorros: pygame.sprite.Group):

		global ancho, alto, tileSize

		# Encontrar el zorro más cercano dentro del rango
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
				if (choice([True, False])):
					self.kill()
				else:
					zorro_cercano.kill()
		
		# Encontrar el conejo más cercano dentro del rango
		else:
			conejos_detectados = [c for c in grupoConejos if distancia(self, c) <= self.rangoCaza]
			if conejos_detectados:
				conejo_cercano = min(conejos_detectados, key=lambda c: distancia(self, c))
				dx = conejo_cercano.rect.x - self.rect.x
				dy = conejo_cercano.rect.y - self.rect.y
				distancia_total = max(math.sqrt(dx ** 2 + dy ** 2), 0.1)

				# Moverse hacia el conejo
				self.rect.x += int((dx / distancia_total) * self.velocidad)
				self.rect.y += int((dy / distancia_total) * self.velocidad)

			# No hay zorros ni conejos
			# El zorro camina en direcciones aleatorias
			else:
				self.direccionContadorTiempo += 1
				if (self.direccionContadorTiempo >= self.direccionTiempo):
					
					self.direccionContadorTiempo = 0
					
					# Si se sale del mapa
					if (self.rect.x < 0 or self.rect.y < 0 or self.rect.x > (ancho * tileSize) or self.rect.y > (alto * tileSize)):
						# Calcular la dirección en grados hacia el centro
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
		pygame.draw.circle(pantalla, (255, 0, 0), screen_pos, self.rangoPelea, 1)
		pygame.draw.circle(pantalla, (0, 255, 255), screen_pos, self.rangoCaza, 1)
		pantalla.blit(self.image, screen_pos)

	def setAnimacion(self, animacion):
		super().setAnimacion(animacion)
		
		match animacion:
			case self.ANIMATION.IDLE:
				self.frameFila = 4
				self.frameTotal = 5
				self.frameVelocidad = 8
			case self.ANIMATION.RUNNING:
				self.frameFila = 5
				self.frameTotal = 6
				self.frameVelocidad = 3
			case self.ANIMATION.ACTION:
				self.frameFila = 6
				self.frameTotal = 11
				self.frameVelocidad = 4

class Simulacion:

	# Cargar recursos principales
	def __init__(self):
		global tileSize, textureAtlas, fuenteDefault

		pygame.init()
		textureAtlas = pygame.image.load("texture.png")
		fuenteDefault = pygame.font.SysFont("Consolas", 18)

	def run(self, posicionesZorros: numpy.ndarray) -> tuple[int, int]:
		global alto, ancho

		# Una hectarea igual a 16 cuadritos de 16 pixeles cada uno
		alto, ancho = posicionesZorros.shape
		ancho *= 16
		alto *= 16

		# Inicializar
		pygame.display.set_caption("Simulacion presa-depredador")
		self.pantalla = pygame.display.set_mode((pantallaAncho, pantallaAlto))

		self.grupoConejos = pygame.sprite.Group()
		
		# Crear zorros en las posiciones dadas
		self.grupoZorros = pygame.sprite.Group()
	
		for x in range(posicionesZorros.shape[0]):
			for y in range(posicionesZorros.shape[1]):
				if (posicionesZorros[x, y] == 1):
					self.grupoZorros.add(Zorro(x * 256, y * 256))

		# Camara
		self.camera = Camera()

		# Crear la textura del pasto
		self.surfaceTerreno = pygame.Surface((ancho * tileSize, alto * tileSize), pygame.SRCALPHA)
		self.surfaceTerreno.fill((59, 150, 74))
		for x in range(ancho):
			for y in range(alto):
				# Pintar el pasto decorativo
				if random() < 0.1:
					self.surfaceTerreno.blit(textureAtlas, (x * tileSize, y * tileSize), (144 + (16 * choice(range(4))), 0, 16, 16))

		# Main loop
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			self.camera.update()
			
			# Actualizar sprites
			for conejo in self.grupoConejos:
				conejo.update(self.grupoZorros.sprites())
			for zorro in self.grupoZorros:
				zorro.update(self.grupoConejos.sprites(), self.grupoZorros.sprites())

			# Limpiar pantalla
			self.pantalla.fill((0, 0, 0))

			# Dibujar terreno
			self.pantalla.blit(self.surfaceTerreno, (-self.camera.x, -self.camera.y))

			# Dibujar entidades
			for conejo in self.grupoConejos:
				conejo.draw(self.pantalla, self.camera)
			for zorro in self.grupoZorros:
				zorro.draw(self.pantalla, self.camera)

			#
			pygame.display.flip()
			pygame.time.Clock().tick(30)

		pygame.quit()
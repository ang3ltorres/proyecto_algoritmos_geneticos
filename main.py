import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Bunny(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.spriteSheet = pygame.image.load("texture.png")
		
		self.spriteWidth = 32
		self.spriteHeight = 32

		self.currentFrame = 0
		self.update_image()

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		
		self.frameCounter = 0
		self.frameSpeed = 5

	def update(self):
		self.frameCounter += 1
		
		if self.frameCounter >= self.frameSpeed:
			self.frameCounter = 0
			self.currentFrame += 1
			if self.currentFrame >= 4:
				self.currentFrame = 0
			self.update_image()

		self.rect.x += 1

	def update_image(self):
		rect = pygame.Rect(self.currentFrame * self.spriteWidth, 0, self.spriteWidth, self.spriteHeight)
		self.image = self.spriteSheet.subsurface(rect)


def main():

	pygame.init()

	screenWidth = 800
	screenHeight = 600
	screen = pygame.display.set_mode((screenWidth, screenHeight))
	pygame.display.set_caption("GA")

	spriteGroup = pygame.sprite.Group()
	spriteGroup.add(Bunny(100, 100))
	spriteGroup.add(Bunny(100, 120))
	spriteGroup.add(Bunny(100, 170))
	spriteGroup.add(Bunny(100, 200))

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		spriteGroup.update()

		screen.fill(BLACK)

		spriteGroup.draw(screen)

		pygame.display.flip()

		pygame.time.Clock().tick(60)

	pygame.quit()
	sys.exit()

if __name__ == '__main__':
	main()

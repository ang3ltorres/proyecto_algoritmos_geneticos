from simulacion import Simulacion
import numpy as np

def main():
	simulacion = Simulacion()
	
	pos1 = np.array([
		[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],

	])

	resultados = []

	conejosPorHectarea = 10

	for i in range(1):
		zorrosPerdidos, tiempoDeCaza = simulacion.run(pos1, conejosPorHectarea)
		resultados.append((zorrosPerdidos, tiempoDeCaza))

if __name__ == '__main__':
	main()

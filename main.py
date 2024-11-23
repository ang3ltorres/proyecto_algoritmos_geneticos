from simulacion import Simulacion
import numpy as np

def main():
	simulacion = Simulacion()
	
	pos1 = np.array([
		[1, 0, 1, 0, 1, 0, 1, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[1, 0, 1, 0, 1, 0, 1, 0],
	])

	conejosPorHectarea = 4
	
	zorrosPerdidos, tiempoDeCaza = simulacion.run(pos1, conejosPorHectarea)
	zorrosPerdidos, tiempoDeCaza = simulacion.run(pos1, conejosPorHectarea)
	zorrosPerdidos, tiempoDeCaza = simulacion.run(pos1, conejosPorHectarea)
	zorrosPerdidos, tiempoDeCaza = simulacion.run(pos1, conejosPorHectarea)
	zorrosPerdidos, tiempoDeCaza = simulacion.run(pos1, conejosPorHectarea)
	print(f"Zorros Perdidos: {zorrosPerdidos}\nTiempo de Caza: {tiempoDeCaza:.2f} (Horas? Minutos?)")

if __name__ == '__main__':
	main()

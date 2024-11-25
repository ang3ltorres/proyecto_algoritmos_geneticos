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

	conejosPorHectarea = 1

	for i in range(1):
		zorrosPerdidos, tiempoDeCaza = simulacion.run(pos1, conejosPorHectarea)
		resultados.append((zorrosPerdidos, tiempoDeCaza))

	# Calcular promedios
	zorrosPerdidosPromedio = sum(r[0] for r in resultados) / len(resultados)
	tiempoDeCazaPromedio = sum(r[1] for r in resultados) / len(resultados)

	print("Zorros Perdidos Promedio:", zorrosPerdidosPromedio)
	print("Tiempo de Caza Promedio:", tiempoDeCazaPromedio)

if __name__ == '__main__':
	main()

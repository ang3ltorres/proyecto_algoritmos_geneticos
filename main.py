from simulacion import Simulacion
from AGB import FoxRabbit, AG
import numpy as np

def main():
    filas = 10
    columnas = 10
    conejos = np.array([
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
    problema = FoxRabbit(conejos)
    individuos = 32
    generaciones = 2000
    factor_mutacion = 0.01
    ag = AG(individuos, filas, columnas, generaciones, factor_mutacion, problema)
    resultados, gen_sim = ag.run()

    # Dimensiones de la simulación
    ANCHO = 800
    ALTO = 800
    CELDAS = 10

    # Ejecutar simulación
    for i, resultado in enumerate(resultados):
        simulacion = Simulacion(ANCHO, ALTO, CELDAS, conejos, resultado, gen_sim[i])
        simulacion.ejecutar()

if __name__ == '__main__':
    main()

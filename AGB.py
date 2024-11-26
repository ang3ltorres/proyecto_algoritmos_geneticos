import copy
import numpy as np

class Individuo:
    def __init__(self, filas, columnas, cromosoma):
        self._filas = filas
        self._columnas = columnas
        self._cromosoma = cromosoma
        self._fitness = 0
        

class AG:
    def __init__(self, cantidad_individuos, filas, columnas, generaciones, p, problema):
        self._cantidad_individuos = cantidad_individuos
        self._filas = filas
        self._columnas = columnas
        self._generaciones = generaciones
        self._p = p
        self._problema = problema
        self._individuos = np.array([])
        self.mejores_matrices = []  # Almacena las mejores matrices de cada n generación
        self.generaciones_simuladas = []

    def run(self):
        self.crearIndividuos()
        self._mejor_historico = self._individuos[0]
        generacion = 1
        while generacion <= self._generaciones:
            self.evaluaIndividuos()
            hijos = np.array([])
            while len(hijos) < len(self._individuos):
                padre1 = self.ruleta()
                padre2 = self.ruleta()
                while padre1 == padre2:
                    padre2 = self.ruleta()
                h1, h2 = self.cruza(self._individuos[padre1], self._individuos[padre2])
                hijos = np.append(hijos, [h1])
                hijos = np.append(hijos, [h2])
            self.mutacion(hijos)
            self._individuos = np.copy(hijos)
            self._individuos[np.random.randint(len(self._individuos))] = copy.deepcopy(self._mejor_historico)
            if generacion % 400 == 0:
                 # Guardar la matriz del mejor histórico
                self.mejores_matrices.append(copy.deepcopy(self._mejor_historico._cromosoma))
                self.generaciones_simuladas.append(generacion)
                print("Generación: ", generacion)
                print("Mejor Histórico (Fitness: {}):".format(self._mejor_historico._fitness))
                print(self._mejor_historico._cromosoma)
            generacion += 1
        return self.mejores_matrices, self.generaciones_simuladas

    def crearIndividuos(self):
        for i in range(self._cantidad_individuos):
            cromosoma = np.zeros((self._filas, self._columnas), dtype=int)
            for fila in range(self._filas):
                for columna in range(self._columnas):
                    if cromosoma[fila, columna] == 0 and np.random.rand() > 0.5:
                        cromosoma[fila, columna] = 1
                        if fila > 0:
                            cromosoma[fila - 1, columna] = 0
                        if fila < self._filas - 1:
                            cromosoma[fila + 1, columna] = 0
                        if columna > 0:
                            cromosoma[fila, columna - 1] = 0
                        if columna < self._columnas - 1:
                            cromosoma[fila, columna + 1] = 0
            individuo = Individuo(self._filas, self._columnas, cromosoma)
            self._individuos = np.append(self._individuos, [individuo])

    def evaluaIndividuos(self):
        for i in self._individuos:
            i._fitness = self._problema.f(i._cromosoma)
            if i._fitness > self._mejor_historico._fitness:
                self._mejor_historico = copy.deepcopy(i)

    def ruleta(self):
        f_sum = np.sum([i._fitness for i in self._individuos])
        if f_sum == 0:
            return np.random.randint(len(self._individuos))
        else:
            r = np.random.randint(f_sum + 1)
            k = 0
            F = self._individuos[k]._fitness
            while F < r:
                k += 1
                F += self._individuos[k]._fitness
            return k

    def cruza(self, i1, i2):
        h1 = copy.deepcopy(i1)
        h2 = copy.deepcopy(i2)
        punto_cruza = np.random.randint(1, self._filas)
        h1._cromosoma[punto_cruza:], h2._cromosoma[punto_cruza:] = (
            h2._cromosoma[punto_cruza:], h1._cromosoma[punto_cruza:]
        )
        return h1, h2

    def mutacion(self, hijos):
        for h in hijos:
            for fila in range(self._filas):
                for columna in range(self._columnas):
                    if np.random.rand() < self._p:
                        h._cromosoma[fila, columna] = int(not h._cromosoma[fila, columna])
                        if h._cromosoma[fila, columna] == 1:
                            if fila > 0:
                                h._cromosoma[fila - 1, columna] = 0
                            if fila < self._filas - 1:
                                h._cromosoma[fila + 1, columna] = 0
                            if columna > 0:
                                h._cromosoma[fila, columna - 1] = 0
                            if columna < self._columnas - 1:
                                h._cromosoma[fila, columna + 1] = 0

class FoxRabbit:
    def __init__(self, denominaciones):
        self._denominaciones = denominaciones

    def f(self, cromosoma):
        max_dinero = 0
        filas, columnas = cromosoma.shape
        penalizacion_adyacencias = 0  # Inicializamos una variable para penalizar las adyacencias

        for fila in range(filas):
            for columna in range(columnas):
                if cromosoma[fila, columna] == 1:
                    max_dinero += self._denominaciones[fila, columna]

                    # Penalización por adyacencias verticales
                    if fila > 0 and cromosoma[fila - 1, columna] == 1:  # Celda arriba
                        penalizacion_adyacencias += 1
                    if fila < filas - 1 and cromosoma[fila + 1, columna] == 1:  # Celda abajo
                        penalizacion_adyacencias += 1
                    
                    # Penalización por adyacencias diagonales
                    if fila > 0 and columna > 0 and cromosoma[fila - 1, columna - 1] == 1:  # Arriba a la izquierda
                        penalizacion_adyacencias += 1
                    if fila > 0 and columna < columnas - 1 and cromosoma[fila - 1, columna + 1] == 1:  # Arriba a la derecha
                        penalizacion_adyacencias += 1
                    if fila < filas - 1 and columna > 0 and cromosoma[fila + 1, columna - 1] == 1:  # Abajo a la izquierda
                        penalizacion_adyacencias += 1
                    if fila < filas - 1 and columna < columnas - 1 and cromosoma[fila + 1, columna + 1] == 1:  # Abajo a la derecha
                        penalizacion_adyacencias += 1

        # Restamos la penalización de las adyacencias verticales y diagonales
        max_dinero -= penalizacion_adyacencias * 10  # Ajusta el valor de penalización según sea necesario

        return max_dinero


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
    resultados,gen_sim = ag.run()

    # Ejecutar simulación
    for i, resultado in enumerate(resultados):
        simulacion = SimulacionPrueba(ANCHO, ALTO, CELDAS, conejos, resultado, gen_sim[i])
        simulacion.ejecutar()




if __name__ == '__main__':
    main()

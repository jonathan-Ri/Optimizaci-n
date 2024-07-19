import random as rnd
from functools import cmp_to_key
import argparse
from itertools import product
import matplotlib.pyplot as plt
import numpy as np


    


def funcionMax(x):
    return 77 * x[0] + 93 * x[1] + 41 * x[2] + 68 * x[3] + 28 * x[4]

def funcionMin(x):
    return 184 * x[0] + 330 * x[1] + 42 * x[2] + 108 * x[3] + 18 * x[4]

max_values = [15, 10, 25, 4, 30]

# Restricciones
def check_constraints(x):
    if x[0] > 15 or x[1] > 10 or x[2] > 25 or x[3] > 4 or x[4] > 30:
        return False
    if 184 * x[0] + 330 * x[1] > 3800:
        return False
    if 42 * x[2] + 108 * x[3] > 2800:
        return False
    if 42 * x[2] + 18 * x[4] > 3500:
        return False
    return True

def generate_combinations(max_values, step=1):
    ranges = [range(0, max_value + 1, step) for max_value in max_values]
    for combination in product(*ranges):
        yield combination

# Encuentra soluciones factibles
def find_feasible_solutions(max_values, step=1):
    feasible_solutions = []
    for combination in generate_combinations(max_values, step):
        if check_constraints(combination):
            feasible_solutions.append(combination)
    return feasible_solutions




class Problem:
    def __init__(self, importancia_max, importancia_min):
        self.dimension = 5
        self.importanciaMax = importancia_max
        self.importanciaMin = importancia_min
        self.MaxVector = [15, 10, 25, 4, 30]
        self.MinVector = [0, 0, 0, 0, 0]
        self.c = 10**64

    def fit(self, x):
        salida = ((self.funcionMax(x) * self.importanciaMax) / (self.funcionMax(self.MaxVector))) + \
                 (((self.c - self.funcionMin(x)) / (self.c - self.funcionMin(self.MinVector))) * self.importanciaMin)
        return salida

    def funcionMax(self, x):
        return 77 * x[0] + 93 * x[1] + 41 * x[2] + 68 * x[3] + 28 * x[4]

    def funcionMin(self, x):
        return 184 * x[0] + 330 * x[1] + 42 * x[2] + 108 * x[3] + 18 * x[4]

    def check(self, x):
        if 184 * x[0] + 330 * x[1] > 3800:
            return False
        if 42 * x[2] + 108 * x[3] > 2800:
            return False
        if 42 * x[2] + 18 * x[4] > 3500:
            return False
        return True

class Agent:
    def __init__(self, problem):
        self.p = problem
        self.x = []
        self.breeder = False
        maximos = [15, 10, 25, 4, 30]
        for i in range(len(maximos)):
            NMRj = rnd.uniform(0, 1)*(maximos[i])#editado para probar
            self.x.append(round(NMRj))  # Redondeamos a enteros iniciales

    def isFeasible(self):
        return self.p.check(self.x)

    def isBetterThan(self, g):
        return self.fit() > g.fit()

    def fit(self):
        return self.p.fit(self.x)

    def move(self, g):
        for j in range(self.p.dimension):
            self.x[j] = round(self.x[j] + rnd.uniform(0, 1) * (g.x[j] - self.x[j]))  

    def moveb(self, g):
        lamda = rnd.uniform(0, 1)
        for j in range(self.p.dimension):
            self.x[j] = round((1 - lamda) * self.x[j] + lamda * (g.x[j] - self.x[j]))  # Movimiento breeder redondeado

    def __str__(self):
        return f"fit: {self.fit()}\",\"{self.x}\","

    def copy(self, a):
        self.x = a.x.copy()

class Swarm:
    def __init__(self, importancia_max, importancia_min):
        self.maxIter = 500
        self.nAgents = 50
        self.swarm = []
        self.p = Problem(importancia_max, importancia_min)
        self.g = Agent(self.p)
        self.gw = Agent(self.p)

    def get_solition(self):
        return f"\"{self.g.x}"

    def solve(self):
        self.initRand()
        self.evolve()

    def initRand(self):
        for _ in range(self.nAgents):
            while True:
                a = Agent(self.p)
                if a.isFeasible():
                    break
            self.swarm.append(a)

        self.g.copy(self.swarm[0])
        self.gw.copy(self.swarm[0])
        for i in range(1, self.nAgents):
            if self.swarm[i].isBetterThan(self.g):
                self.g.copy(self.swarm[i])
        self.selector()
        for i in range(1, self.nAgents):
            if self.swarm[i].isBetterThan(self.gw) and not self.swarm[i].breeder:
                self.gw.copy(self.swarm[i])

    def comparar(self, rata1, rata2):
        if rata1.isBetterThan(rata2):
            return -1
        elif rata2.isBetterThan(rata1):
            return 1
        else:
            return 0

    def selector(self):
        self.swarm.sort(key=cmp_to_key(self.comparar))
        for i in range(5):
            self.swarm[i].breeder = True

    def evolve(self):
        breddingProbability = 0.5
        t = 1
        while t <= self.maxIter:
            for i in range(self.nAgents):
                a = Agent(self.p)
                evo = rnd.uniform(0, 1)
                while True:
                    a.copy(self.swarm[i])
                    if i > 4:
                        a.move(self.gw)
                    else:
                        if evo > breddingProbability:
                            a.moveb(self.g)
                    if a.isFeasible():
                        break
                self.swarm[i].copy(a)

            for i in range(self.nAgents):
                if self.swarm[i].isBetterThan(self.g):
                    self.g.copy(self.swarm[i])
            for i in range(self.nAgents):
                if self.swarm[i].isBetterThan(self.gw) and not self.swarm[i].breeder:
                    self.gw.copy(self.swarm[i])

            t += 1
            print(f"{self.g}")
            print(f"\"{self.g}\"funcionMax: {self.p.funcionMax(self.g.x)}\",\"funcionMin: {self.p.funcionMin(self.g.x)}\"")

numeros=["1","2","3","4","5","6","7","8","9","10"]

def filtro(texto):
    a=texto.split(",")
    b = list()
    for i in a:
        c=i.strip()
        d=""
        for j in c:
            if j in numeros:
                d=d+j
            
        b.append(int(d))
    return b


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Descripción de tu programa')
    parser.add_argument('--importancia_max', type=float, default=0.6, help='Valor de importancia máximo')
    parser.add_argument('--importancia_min', type=float, default=0.4, help='Valor de importancia mínimo')

    args = parser.parse_args()


    
    vector_solucion= Swarm(args.importancia_max, args.importancia_min)
    vector_solucion.solve()
    texto=vector_solucion.get_solition()
    x=filtro(texto)
    
    #print("---------------")
    #print(x)
    #print("---------------")
    feasible_solutions = find_feasible_solutions(max_values)

    # Evalúa las soluciones en las funciones objetivo
    objective_values = [(funcionMax(sol), funcionMin(sol)) for sol in feasible_solutions]
   
    # Grafica las soluciones factibles
    x_vals = [val[0] for val in objective_values]
    y_vals = [val[1] for val in objective_values]

    plt.scatter(x_vals, y_vals, c='blue', label='Soluciones factibles')
    plt.xlabel('Función Max (77x1 + 93x2 + 41x3 + 68x4 + 28x5)')
    plt.ylabel('Función Min (184x1 + 330x2 + 42x3 + 108x4 + 18x5)')
    plt.title('Soluciones factibles evaluadas en las funciones objetivo')
    plt.scatter(funcionMax(x), funcionMin(x), color='red', label='solución encontrada con NMR')
    plt.legend()
    plt.grid(True)
    plt.show()

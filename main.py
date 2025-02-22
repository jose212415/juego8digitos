import tkinter as tk
import heapq
import random
from copy import deepcopy

class Juego8Digitos:
    def __init__(self):
        self.estado = self.generar_estado_valido()
        self.solucion = []
        self.pausado = False
        self.paso_actual = 0

    def contar_inversiones(self, estado):
        lista = [num for fila in estado for num in fila if num != 0]
        inversiones = sum(1 for i in range(len(lista)) for j in range(i + 1, len(lista)) if lista[i] > lista[j])
        return inversiones

    def es_resoluble(self, estado):
        return self.contar_inversiones(estado) % 2 == 0

    def generar_estado_valido(self):
        while True:
            numeros = list(range(9))
            random.shuffle(numeros)
            estado = [numeros[i:i+3] for i in range(0, 9, 3)]
            if self.es_resoluble(estado):
                return estado

    def encontrar_espacio_vacio(self, estado):
        for i in range(3):
            for j in range(3):
                if estado[i][j] == 0:
                    return i, j

    def generar_estados_posibles(self, estado):
        estados_posibles = []
        empty_x, empty_y = self.encontrar_espacio_vacio(estado)
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, Abajo, Izquierda, Derecha
        
        for dx, dy in movimientos:
            new_x, new_y = empty_x + dx, empty_y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                nuevo_estado = deepcopy(estado)
                nuevo_estado[empty_x][empty_y], nuevo_estado[new_x][new_y] = nuevo_estado[new_x][new_y], nuevo_estado[empty_x][empty_y]
                estados_posibles.append(nuevo_estado)
        
        return estados_posibles

    def manhattan_distance(self, estado):
        objetivo = {num: (i, j) for i, fila in enumerate([[1, 2, 3], [4, 5, 6], [7, 8, 0]]) for j, num in enumerate(fila)}
        distancia = sum(abs(i - objetivo[estado[i][j]][0]) + abs(j - objetivo[estado[i][j]][1]) for i in range(3) for j in range(3) if estado[i][j] != 0)
        return distancia

    def a_estrella(self):
        prioridad = []
        heapq.heappush(prioridad, (self.manhattan_distance(self.estado), 0, self.estado, []))
        visitados = set()
        
        while prioridad:
            _, g, estado_actual, camino = heapq.heappop(prioridad)
            estado_tuple = tuple(tuple(fila) for fila in estado_actual)
            
            if estado_tuple in visitados:
                continue
            visitados.add(estado_tuple)
            
            if estado_actual == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
                return camino + [estado_actual]
            
            for siguiente_estado in self.generar_estados_posibles(estado_actual):
                if tuple(tuple(fila) for fila in siguiente_estado) not in visitados:
                    f = g + 1 + self.manhattan_distance(siguiente_estado)
                    heapq.heappush(prioridad, (f, g + 1, siguiente_estado, camino + [estado_actual]))
        
        return None

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de los 8 Dígitos")
        self.juego = Juego8Digitos()
        
        self.botones = [[tk.Button(root, font=("Arial", 20), width=5, height=2) for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.botones[i][j].grid(row=i, column=j)

        self.btn_iniciar = tk.Button(root, text="Iniciar", command=self.iniciar)
        self.btn_iniciar.grid(row=3, column=0, sticky="we")

        self.btn_pausar = tk.Button(root, text="Pausar", command=self.pausar)
        self.btn_pausar.grid(row=3, column=1, sticky="we")

        self.btn_reiniciar = tk.Button(root, text="Reiniciar", command=self.reiniciar)
        self.btn_reiniciar.grid(row=3, column=2, sticky="we")
        
        self.actualizar_tablero()

    def actualizar_tablero(self):
        for i in range(3):
            for j in range(3):
                num = self.juego.estado[i][j]
                self.botones[i][j].config(text=str(num) if num != 0 else " ")

    def iniciar(self):
        self.juego.pausado = False
        self.juego.solucion = self.juego.a_estrella()
        
        if self.juego.solucion:
            self.juego.paso_actual = 0
            self.mostrar_solucion_paso_a_paso()

    def pausar(self):
        self.juego.pausado = True

    def reiniciar(self):
        self.juego.pausado = True
        self.juego.estado = self.juego.generar_estado_valido()
        self.actualizar_tablero()

    def mostrar_solucion_paso_a_paso(self):
        if not self.juego.pausado and self.juego.paso_actual < len(self.juego.solucion):
            self.juego.estado = self.juego.solucion[self.juego.paso_actual]
            self.actualizar_tablero()
            self.juego.paso_actual += 1
            self.root.after(1000, self.mostrar_solucion_paso_a_paso)

root = tk.Tk()
gui = PuzzleGUI(root)
root.mainloop()

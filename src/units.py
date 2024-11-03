# Clase para representar la posición de un elemento
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Clase para representar un elemento de la imagen
class Node:
    def __init__(self, point, pixel):
        self.position = point
        self.color = pixel
        
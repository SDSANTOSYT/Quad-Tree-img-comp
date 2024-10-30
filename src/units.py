# Clase para representar el color de un elemento
class Pixel:
    def __init__(self, r, g, b):
        self.r = 0
        self.g = 0
        self.b = 0

# Clase para representar la posición de un elemento
class Point:
    def __init__(self, x, y):
        self.x = 0
        self.y = 0

# Clase para representar un elemento de la imagen
class Node:
    def __init__(self, point: Point, pixel: Pixel):
        self.position = point
        self.color = pixel
        
# Función para promediar el color de un elemento
def mean_color(p1: Pixel, p2: Pixel, p3: Pixel, p4: Pixel):
    r = (p1.r + p2.r + p3.r + p4.r) // 4
    g = (p1.g + p2.g + p3.g + p4.g) // 4
    b = (p1.b + p2.b + p3.b + p4.b) // 4
    return Pixel(r, g, b)
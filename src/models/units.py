import numpy as np

# Clase para representar la posición de un elemento========================================================================================
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Clase para representar un elemento de la imagen==========================================================================================
class Node:
    def __init__(self, point, pixel):
        self.position = point
        self.color = pixel
    
    # Función para calcular la distancia entre dos pixeles=================================================================================   
    def calculate_distance(self, pixel):
        return np.sqrt((self.color[0] - pixel[0])**2 + (self.color[1] - pixel[1])**2 + (self.color[2] - pixel[2])**2)

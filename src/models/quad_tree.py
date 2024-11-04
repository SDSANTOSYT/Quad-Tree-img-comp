from models.units import*

# Clase para representar un árbol cuaternario==============================================================================================
class QuadTree:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.node = None
        self.children = [None,None,None,None]
    
    def is_leaf(self):
        return self.children[0] is None and self.children[1] is None and self.children[2] is None and self.children[3] is None
    
    # Función para insertar un nodo en el árbol=============================================================================================
    def insert(self, node):
        
        # Si el tamaño del árbol es 1 (es decir del tamaño de un pixel), se inserta el nodo en el árbol===================================
        if self.size == 1:
            self.node = node
            return True
        
        # se divide el árbol en 4 partes===================================================================================================
        half = self.size // 2
        
        # Se verifica en que parte del árbol se insertará el nodo==========================================================================
        if node.position.x < self.x + half and node.position.y < self.y + half:
            # Mitad superior izquierda=====================================================================================================
            if self.children[0] is None:
                self.children[0] = QuadTree(self.x, self.y, half)
            return self.children[0].insert(node)
        
        elif node.position.x >= self.x + half and node.position.y < self.y + half:
            # Mitad superior derecha=======================================================================================================
            if self.children[1] is None:
                self.children[1] = QuadTree(self.x + half, self.y, half)
            return self.children[1].insert(node)
        
        elif node.position.x < self.x + half and node.position.y >= self.y + half:
            # Mitad inferior izquierda=====================================================================================================
            if self.children[2] is None:
                self.children[2] = QuadTree(self.x, self.y + half, half)
            return self.children[2].insert(node)
        
        else:
            # Mitad inferior derecha=======================================================================================================
            if self.children[3] is None:
                self.children[3] = QuadTree(self.x + half, self.y + half, half)
            return self.children[3].insert(node)
    
    # Función para calcular el promedio de cada area de pixeles en el árbol=================================================================
    def calculate_mean(self):
        # Si el tamaño del árbol es 1 (es decir del tamaño de un pixel), se retorna el color del nodo======================================
        if self.size == 1:
            return self.node.color
        
        else:
            # Se calcula el promedio de los colores de los nodos hijos=====================================================================
            p1 = self.children[0].calculate_mean()
            p2 = self.children[1].calculate_mean()
            p3 = self.children[2].calculate_mean()
            p4 = self.children[3].calculate_mean()
            if self.node is None:
                self.node = Node(Point(self.x, self.y), np.array(3))
            # Se asigna el promedio de los colores de los nodos hijos al nodo actual=======================================================
            self.node.color = np.mean([p1[0], p2[0], p3[0], p4[0]]), np.mean([p1[1], p2[1], p3[1], p4[1]]), np.mean([p1[2], p2[2], p3[2], p4[2]])
            return self.node.color
    
    # Función para comprimir la imagen=====================================================================================================
    def compress(self, level, tollerance):
        # Se crea el array que guardará la imagen comprimida===============================================================================
        array_img = np.ndarray((self.size, self.size, 3), dtype=np.uint8)
        return self.__compress(0, level, array_img,tollerance)
    
    # Función auxiliar para comprimir la imagen============================================================================================
    def __compress(self, current_level, level, array_img, tollerance):
        # Si el nodo actual es una hoja o si el nivel actual es mayor o igual al nivel de compresión, se asigna el color del nodo actual===
        if self.is_leaf() or (current_level >= level and self.is_tollerant(tollerance)) :
            array_img[self.y:self.y + self.size, self.x:self.x + self.size] = self.node.color
            
        else:
            # Se llama recursivamente a la función para los nodos hijos====================================================================
            for child in self.children:
                if child is not None:
                    child.__compress(current_level + 1, level, array_img,tollerance)
        return array_img
    
    # Función para verificar si los nodos hijos se encuentran dentro del umbral de tolerancia==============================================
    def is_tollerant(self, tollerance):
        dist1 = self.children[0].node.calculate_distance(self.node.color)
        dist2 = self.children[1].node.calculate_distance(self.node.color)
        dist3 = self.children[2].node.calculate_distance(self.node.color)
        dist4 = self.children[3].node.calculate_distance(self.node.color)
        return dist1 < tollerance and dist2 < tollerance and dist3 < tollerance and dist4 < tollerance
    
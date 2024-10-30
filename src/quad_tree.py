from units import*

# Clase para representar un quadtree=======================================================================================================
class QuadTree:
    def __init__(self, topL, botR):
        self.topLeft: Point = topL
        self.bottonRight: Point = botR
        self.node: Node = None
        self.topLeftTree: QuadTree = None
        self.topRightTree: QuadTree = None
        self.bottonLeftTree: QuadTree = None
        self.bottonRightTree: QuadTree = None
    
    # Función para saber si el punto se encuentra en los limites del quadtree==============================================================
    def in_bounds(self, point: Point):
        return point.x >= self.topLeft.x and point.x <= self.bottonRight.x and point.y >= self.topLeft.y and point.y <= self.bottonRight.y
    
    # Función para saber si el quadtree se puede dividir===================================================================================
    def can_divide(self):
        return not (abs(self.topLeft.x - self.bottonRight.x) <= 1 and abs(self.topLeft.y - self.bottonRight.y) <= 1)
    
    # Función para insertar un nodo en el quadtree=========================================================================================
    def insert(self, node: Node):
        
        # Verifica que el nodo no sea nulo
        if node is None:
            return
        
        # Verifica que el nodo se encuentre en los limites del quadtree
        if not self.in_bounds(node.position):
            return
        
        # Verifica si el quadtree ya no se puede dividir
        if not self.can_divide():
            if self.node is None:
                self.node = node
            return
        
        # Verifica si el nodo que se va a insertar está en la mitad izquierda
        if (self.topLeft.x + self.bottonRight.x) / 2 >= node.position.x:
            # Verifica si el nodo que se va a insertar está en la mitad superior
            if (self.topLeft.y + self.bottonRight.y) / 2 >= node.position.y:
                if self.topLeftTree is None:
                    self.topLeftTree = QuadTree(self.topLeft, Point((self.topLeft.x + self.bottonRight.x) / 2, (self.topLeft.y + self.bottonRight.y) / 2))
                self.topLeftTree.insert(node)
            # Verifica si el nodo que se va a insertar está en la mitad inferior
            else:
                if self.bottonLeftTree is None:
                    self.bottonLeftTree = QuadTree(Point(self.topLeft.x, (self.topLeft.y + self.bottonRight.y) / 2), Point((self.topLeft.x + self.bottonRight.x) / 2, self.bottonRight.y))
                self.bottonLeftTree.insert(node)
        # Verifica si el nodo que se va a insertar está en la mitad derecha
        else:
            # Verifica si el nodo que se va a insertar está en la mitad superior
            if (self.topLeft.y + self.bottonRight.y) / 2 >= node.position.y:
                if self.topRightTree is None:
                    self.topRightTree = QuadTree(Point((self.topLeft.x + self.bottonRight.x) / 2, self.topLeft.y), Point(self.bottonRight.x, (self.topLeft.y + self.bottonRight.y) / 2))
                self.topRightTree.insert(node)
            # Verifica si el nodo que se va a insertar está en la mitad inferior
            else:
                if self.bottonRightTree is None:
                    self.bottonRightTree = QuadTree(Point((self.topLeft.x + self.bottonRight.x) / 2, (self.topLeft.y + self.bottonRight.y) / 2), self.bottonRight)
                self.bottonRightTree.insert(node)
    
    # Metodo para calcular el promedio de los colores de los nodos=========================================================================
    def calculate_mean(self):
        
        # Verifica si el quadtree ya no se puede dividir, es decir si es del tamaño de un pixel
        if not self.can_divide():
            # Verifica si contiene un piexel o no
            if self.node is None:
                return Pixel(0, 0, 0)
            else:
                return self.node.color
        else:
            # Calcula el promedio de los colores de todos los subquadtree
            p1 = self.topLeftTree.calculate_mean()
            p2 = self.topRightTree.calculate_mean()
            p3 = self.bottonLeftTree.calculate_mean()
            p4 = self.bottonRightTree.calculate_mean()
            self.node.color = mean_color(p1, p2, p3, p4)
            return self.node.color
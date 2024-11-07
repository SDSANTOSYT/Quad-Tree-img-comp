// Quadtree implementation in JavaScript

// Clase punto que contiene las coordenadas x, y===========================================================================================
class Point {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
}

// Clase rectángulo que delimitará el espacio de cada quadtree=============================================================================
class Rectangle {
    constructor(x, y, width, height) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
    }
    // Método que verifica si un punto está dentro del rectángulo==========================================================================
    contains(point) {
        return point.x >= this.x - this.width &&
            point.x <= this.x + this.width &&
            point.y >= this.y - this.height &&
            point.y <= this.y + this.height;
    }
}

// Clase QuadTree que almacena los puntos==================================================================================================
class QuadTree {
    constructor(boundary, capacity) {
        this.boundary = boundary;
        this.capacity = capacity;
        this.points = [];
        this.divided = false;
    }

    // Metodo que subdiide el quadtree en 4 cuadrantes=====================================================================================
    subdivide() {
        let x = this.boundary.x;
        let y = this.boundary.y;
        let w = this.boundary.width / 2;
        let h = this.boundary.height / 2;
        let ne = new Rectangle(x + w, y - h, w, h);
        this.northeast = new QuadTree(ne, this.capacity);
        let nw = new Rectangle(x - w, y - h, w, h);
        this.northwest = new QuadTree(nw, this.capacity);
        let se = new Rectangle(x + w, y + h, w, h);
        this.southeast = new QuadTree(se, this.capacity);
        let sw = new Rectangle(x - w, y + h, w, h);
        this.southwest = new QuadTree(sw, this.capacity);
        this.divided = true;
    }

    // Metodo que inserta un punto en el quadtree==========================================================================================
    insert(point) {
        if (!this.boundary.contains(point)) {
            return;
        }
        if (this.points.length < this.capacity) {
            this.points.push(point);
        } else {
            if (!this.divided) {
                this.subdivide();
            }
            this.northwest.insert(point);
            this.northeast.insert(point);
            this.southwest.insert(point);
            this.southeast.insert(point);
        }
    }

    // Metodo para dibujar el quadtree=====================================================================================================
    show() {
        stroke(255);
        strokeWeight(1);
        noFill();
        rectMode(CENTER);
        rect(this.boundary.x, this.boundary.y, this.boundary.width * 2, this.boundary.height * 2);
        if (this.divided) {
            this.northwest.show();
            this.northeast.show();
            this.southwest.show();
            this.southeast.show();
        }
        for (let p of this.points) {
            stroke(0,255,0);
            strokeWeight(5);
            point(p.x, p.y);
        }
    }
}
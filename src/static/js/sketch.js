// Sketch for QuadTree visualization

let qtree;

function setup() {
    createCanvas(900, 900);
    let boundary = new Rectangle(450, 450, 450, 450);
    qtree = new QuadTree(boundary, 12);
}

function draw() {
    if (mouseIsPressed) {
        for (let i = 0; i < 1; i++) {
            let m = new Point(mouseX + random(-5, 5), mouseY + random(-5, 5));
            qtree.insert(m);
        }
    }
    background(0);
    qtree.show();
}



from flask import Flask, request, send_file, render_template, jsonify
import cv2 as cv
import numpy as np
from quad_tree import*

quad = None
img = None

app = Flask(__name__)

# Rutas====================================================================================================================================


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global quad, img
    img = cv.imdecode(np.frombuffer(request.files['image'].read(), np.uint8), cv.IMREAD_COLOR)
    quad = QuadTree(0, 0, img.shape[0])
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            quad.insert(Node(Point(j, i), img[i][j]))
    quad.calculate_mean()
    print(quad.node.color)
    return jsonify({'size': f'{img.shape[0]}'})

@app.route('/compression')
def compression():
    global quad, img
    if not quad or img is None:
        return jsonify({'message': 'Image not uploaded'})
    
    subdivision = request.args.get('subdiv',0)
    threshold = request.args.get('th',0)
    
    print(cv.imwrite('src/static/comp_img.png',quad.compress(int(subdivision),int(threshold))))
    
    return send_file('.\\static\\comp_img.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
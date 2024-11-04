from flask import Flask, request, send_file, render_template, jsonify
import cv2 as cv
import numpy as np
from quad_tree import*

quad = None
img = None

app = Flask(__name__)

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
    return jsonify({'message': 'Image uploaded successfully'})

@app.route('/compression')
def compression():
    global quad, img
    print(img.shape)
    if not quad or img is None:
        return jsonify({'message': 'Image not uploaded'})
    
    subdivision = np.log2(img.shape[0]) * np.float64(request.args.get('subdiv',0))
    print(subdivision)
    threshold = request.args.get('th',0)
    
    print(cv.imwrite('src/static/hola3.png',quad.compress(round(subdivision),round(int(threshold)))))
    
    return send_file('.\\static\\hola3.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, send_file, render_template, jsonify
import cv2 as cv
from models.quad_tree import*

# inicialización de variables globales===================================================================================================
quad = None
img = None

# Inicialización de la aplicación=======================================================================================================
app = Flask(__name__)

# Ruta principal===========================================================================================================================
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para subir la imagen================================================================================================================
@app.route('/upload', methods=['POST'])
def upload():
    global quad, img
    # se decodinifica la imagen============================================================================================================
    img = cv.imdecode(np.frombuffer(request.files['image'].read(), np.uint8), cv.IMREAD_COLOR)
    
    # se guarda la información de la imagen en el quadtree=================================================================================
    quad = QuadTree(0, 0, img.shape[0])
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            quad.insert(Node(Point(j, i), img[i][j]))
    quad.calculate_mean()
    
    # se retorna el tamaño de la imagen===================================================================================================
    return jsonify({'size': f'{img.shape[0]}'})

# Ruta para comprimir la imagen============================================================================================================
@app.route('/compression')
def compression():
    global quad, img
    # se verifica si la imagen fue subida=================================================================================================
    if not quad or img is None:
        return jsonify({'message': 'Image not uploaded'})
    
    # se obtienen los parametros de la compresión===========================================================================================
    subdivision = request.args.get('subdiv',0)
    threshold = request.args.get('th',0)
    
    # se comprime la imagen y se guarda en la carpeta static===============================================================================
    print(cv.imwrite('src/static/comp_img.png',quad.compress(int(subdivision),int(threshold))))
    
    # se retorna la imagen comprimida=====================================================================================================
    return send_file('.\\static\\comp_img.png', mimetype='image/png')


# Ruta para visualizar un quadtree=========================================================================================================
@app.route('/visualize')
def visualize():
    return render_template('quadtree.html')

if __name__ == '__main__':
    app.run(debug=True)
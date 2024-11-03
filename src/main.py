import cv2 as cv
from PIL import Image
from quad_tree import*

img = cv.imread('xd.png')

print(img.shape)  # [255 255 255]

quad = QuadTree(Point(0, 0), Point(img.shape[0]-1, img.shape[1]-1))

for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        quad.insert(Node(Point(j, i), Pixel(img[i][j][2], img[i][j][1], img[i][j][0])))

quad.calculate_mean()

print(quad.node.color)
#print(quad.compress(7))
image = Image.fromarray(quad.compress(8))
image.show()
#cv.imwrite("hola3.png",quad.compress(8))
#cv.imshow('hola3.png', cv.imread('hola3.png'))
#cv.waitKey(0)
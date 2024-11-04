import cv2 as cv
from PIL import Image
from quad_tree import*

img = cv.imread('xd.png')

print(img.shape)  # [255 255 255]

quad = QuadTree(0, 0, img.shape[0])

for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        quad.insert(Node(Point(j, i), img[i][j]))

quad.calculate_mean()

print(quad.node.color)
cv.imwrite("hola3.png",quad.compress(0,0))
#cv.imshow('hola3.png', cv.imread('hola3.png'))
#cv.waitKey(0)
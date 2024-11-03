import cv2 as cv
from quad_tree import*

img = cv.imread('hola.png')

print(img.shape)  # [255 255 255]

quad = QuadTree(Point(0, 0), Point(img.shape[0], img.shape[1]))

for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        quad.insert(Node(Point(j, i), Pixel(img[i][j][2], img[i][j][1], img[i][j][0])))

quad.calculate_mean()

print(quad.node.color)
print(quad.compress(6))
cv.imwrite("hola3.png",quad.compress(6))
#cv.imshow('hola3.png', cv.imread('hola3.png'))
#cv.waitKey(0)
import cv2

img = cv2.imread('2.png')
img = cv2.resize(img,dsize=(400,255))
cv2.imwrite('2_1.png',img)

import cv2

# path
path = '/home/kilox/a_raw.png'

# Using cv2.imread() method
img = cv2.imread(path,3)

# Displaying the image
cv2.imshow('image', img)

print(img)

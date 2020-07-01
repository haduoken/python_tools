import cv2
from cv2 import Stitcher_create
from cv2 import Stitcher

stitcher = Stitcher_create()
stitcher = Stitcher()
stitcher.create()
foo = cv2.imread("data/pantilt/4.jpg")
bar = cv2.imread("data/pantilt/5.jpg")
foo = cv2.resize(foo, (480, 270))
cv2.imshow('foo',foo)
cv2.waitKey(0)
bar = cv2.resize(bar, (480, 270))
cv2.imshow('bar',bar)
cv2.waitKey(0)
status, img = stitcher.stitch((foo, bar))
print(status)
if status == 0:
    cv2.imshow('result', img)
    cv2.waitKey(0)

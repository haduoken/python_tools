#!/usr/bin/python3
import cv2, os, shutil

cap = cv2.VideoCapture(0)
i = 0
image_folder = 'image_1'
if os.path.exists(image_folder):
    shutil.rmtree(image_folder)
os.mkdir(image_folder)

while True:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3264)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2448)
    ok, image = cap.read()
    if not ok:
        break
    cv2.imshow('image', image)
    key = cv2.waitKey(2)
    if key != -1:
        if key == ord('q'):
            break
        else:
            i += 1
            print('保存图像', i)
            cv2.imwrite('{}/{}.jpg'.format(image_folder, i), image)

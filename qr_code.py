import qrcode, cv2, os
from pyzbar.pyzbar import decode
from PIL import Image
import random

# img_left = qrcode.make('left', box_size=100, border=0)
# img_right = qrcode.make('right', box_size=100, border=0)
# img_left.save('left.png')
# img_right.save('right.png')

# target = Image.new('RGB', (5000, 5000))
#
# data = list('sdfxsdfjwkelfjskldfjl')
# left, top = 0, 0
# for left in range(0, 5000, 300):
#     for top in range(0, 5000, 300):
#         random.shuffle(data)
#         a = ''.join(data)
#         # version 代表了尺寸
#         img_small_qr_code = qrcode.make(a, version=1)
#         img = img_small_qr_code.get_image()
#         target.paste(img, (left, top))
#         # target.show('tmp')
#
# target.save('small_qr_code_fill.png')

# img_small_qr_code.save('small_qr_code.png')


folder = '/home/kilox/2020-03-20'
for file in os.listdir(folder):
    file_name = os.path.join(folder, file)
    img = cv2.imread(file_name)
    text_content = decode(img)
    if text_content is not None:
        print("{} content : {}".format(file_name, text_content))
# cv.imshow("input", src)

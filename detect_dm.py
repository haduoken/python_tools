from pydmtx import DataMatrix
from PIL import Image

# Read a Data Matrix barcode
dm_read = DataMatrix()
img = Image.open("data/dm.png")

print(dm_read.decode(img.size[0], img.size[1], str(img.tobytes())))
print(dm_read.count())
print(dm_read.message(1))

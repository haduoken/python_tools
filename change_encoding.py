import codecs
import os
import chardet


def convert(filename):
    try:
        content = codecs.open(filename, 'rb').read()
        source_encoding = chardet.detect(content)['encoding']
        content = content.decode(source_encoding).encode('utf-8')
        codecs.open(filename, 'wb').write(content)
    except UnicodeDecodeError as e:
        print("I/O error :{}".format(e))

change_extension = ['.h','.cpp','.txt']
import sys
dirname = sys.argv[1]
for root,dirs,files in os.walk(dirname):
    for file in files:
        if os.path.splitext(file)[1] in change_extension:
            full_path = os.path.join(root,file)
            print(full_path)
            convert(full_path)

from PIL import Image
import os
import pytesseract
import  shutil

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd =  r'C:\Program Files\Tesseract-OCR\tesseract'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

# Simple image to string
# ok = pytesseract.image_to_string(Image.open('MCS-Haramain-2000.png'))
# print(ok)

for f in os.listdir('new_ar'):
    font = f.split('.')[0]
    check = pytesseract.image_to_string(Image.open('new_ar/' + f))
    zero_str = list(check).count('0')
    o_str = list(check).count('O')
    if check == "":
        try:
            shutil.move('trdg/fonts/new_ar/' + font + '.ttf', 'trdg/fonts/damage_ar/' + font + '.ttf')
            print(str(zero_str) + ' ------- ' + f + ' ------- ' + str(o_str))
        except:
            shutil.move('trdg/fonts/new_ar/' + font + '.TTF', 'trdg/fonts/damage_ar/' + font + '.TTF')
            print(str(zero_str) + ' ------- ' + f + ' ------- ' + str(o_str))
        os.remove('new_ar/' + f)
    # print(str(o_str) + '         ' + f)
    # print(check)
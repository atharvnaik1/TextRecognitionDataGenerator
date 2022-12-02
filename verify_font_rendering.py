import os
import sys
import argparse
from PIL import ImageDraw, ImageFont, Image

# Initialize parser
parser = argparse.ArgumentParser()
parser.add_argument("-fs", "--FontSize", type=int, help="Text Size you want in Image")
parser.add_argument("-tf", "--TextFile", help="Text File containing data to be generated")
parser.add_argument("-fd", "--FontsDirectory", help="Fonts Directory containing fonts to be generated")
parser.add_argument("-savepath", "--ImageSave", help="Image Save Directory Path")

args = parser.parse_args()

# Default Values
fontsize = 30
# txt = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z\n1 2 3 4 5 6 7 8 9 0\n& ! - , \" ' ."
txt = '، ؛ ؟ء آ أ ؤ إ ئ ا ب ة ت ث ج \nح خ د ذ ر ز س ش ص ض ط ظ ع غ ـ ف ق ك ل \nم ن ه و ى يً   ٌ  ٍ  َ  ُ  ِ  ّ  ْ  ٓ  ٔ  ٕ ﷲ ﷺ ﷻ ﷴ٠ ٳ \nٲ ٱ ٰ ٯ ٮ ٭ ٬ ٫ ٪ ٩ ٨ ٧ ٦ ٥ ٤ ٣ ٢ ١'


if args.FontSize:
    fontsize = args.FontSize
if args.TextFile:
    f = open(args.TextFile, "r", encoding='utf8')
    txt = f.read()
print(fontsize)
print(txt)

if args.FontsDirectory:
    for f in os.listdir(args.FontsDirectory):
        # pass
        # try:
        #     os.mkdir('Verify_Fonts')
        # except:
        #     pass
        image = Image.new('RGBA', (1000, 500), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(os.path.join(args.FontsDirectory, f), fontsize)
        draw.text((10, 0), txt, (0, 0, 0), font=font, stroke_width=0)
        image.save('{}/{}.png'.format(args.ImageSave, f.split('.')[0]))
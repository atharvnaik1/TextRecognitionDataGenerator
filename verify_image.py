import os
from PIL import ImageDraw, ImageFont, Image

fontsize = 30
txt = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z\n1 2 3 4 5 6 7 8 9 0\n& ! - , \" ' ."

for f in os.listdir(os.path.join(os.path.dirname(__file__), "trdg/fonts/latin")):
    try:
        os.mkdir('Verify_Fonts')
    except:
        pass
    image = Image.new('RGBA', (800, 150), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), "trdg/fonts/latin", f), fontsize)
    draw.text((10, 0), txt, (0, 0, 0), font=font, stroke_width=0)
    image.save('Verify_Fonts/{}.png'.format(f.split('.')[0]))
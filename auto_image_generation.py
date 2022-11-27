from trdg.generators import GeneratorFromStrings
import os

"""Read the dictionnary file and returns all words in it.
"""
lang_dict = []
with open(
    os.path.join(os.path.dirname(__file__), "trdg/dicts", 'en' + ".txt"),
    "r",
    encoding="utf8",
    errors="ignore",
) as d:
    lang_dict = [l for l in d.read().splitlines() if len(l) > 0]

image_dir=os.path.join("..", os.path.split(os.path.realpath(__file__))[0], "trdg\\images")
print(image_dir)
# This will define the dict count for each font.
lang_dict = lang_dict[:10]
margins = (5, 5, 5, 5)
# Size or format is the quality of the picture
size = 64
fit = False
output_bboxes = 0
# Note
# For normal white background type 0, 1, 2 or 3.
# For transparent_background type 4 and for custom_background type 5.
# Custom background images will place in image_dir
background_type = 0


generator_from_string = GeneratorFromStrings(strings=lang_dict, margins=margins, fit=fit, background_type=background_type,
                                             output_bboxes=output_bboxes, size=size, image_dir=image_dir)

# print(generator_from_string.fonts)

count = 1
for img, font, c, lbl in generator_from_string:
    mf = font.split("\\")[-1].split('.')[0]
    # try:
    #     os.mkdir('check2')
    # except:
    #     pass
    # try:
    #     os.mkdir('check2/{}'.format(mf))
    # except:
    #     pass
    # Image Save
    # img.save("check2/{}/{}.png".format(mf, c),"PNG")
    # Label save
    # with open('check2/{}/{}.txt'.format(mf, c), 'w') as f:
    #     f.write(lbl)
    # count += 1
    # print(count, lbl)
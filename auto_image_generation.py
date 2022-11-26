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

print(len(lang_dict))

"""Load all fonts in the fonts directories
"""

generator_from_string = GeneratorFromStrings(lang_dict)

# print(generator_from_string.fonts)

count = 1
for img, font, c, lbl in generator_from_string:
    mf = font.split("\\")[-1].split('.')[0]
    try:
        os.mkdir('check/{}'.format(mf))
    except:
        pass
    # Image Save
    img.save("check/{}/{}.png".format(mf, c),"PNG")
    # Label save
    with open('check/{}/{}.txt'.format(mf, c), 'w') as f:
        f.write(lbl)
    count += 1
    print(count, lbl)
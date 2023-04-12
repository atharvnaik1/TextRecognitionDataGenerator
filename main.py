"""
Modified script of trdg.run.py

to support generating font wise data

ex. For font Times_new_roman the data will saved in that folder -- Times_new_roman/1.png 

Usage:

1) to generate all font data -- separate folder for each-- 
    python main.py  --count 5 --name_format 3 --font_wise_separate_data

2) Specific font:
  python trdg/run.py  --count 5 --name_format 3 --font_wise_separate_data  --font "./trdg/fonts/latin/AllerDisplay.ttf"

"""
import argparse
import errno
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import random as rnd
import string
import sys
from multiprocessing import Pool

from tqdm import tqdm

from trdg.data_generator import FakeTextDataGenerator
from trdg.string_generator import (create_strings_from_dict,
                                   create_strings_from_file,
                                   create_strings_from_wikipedia,
                                   create_strings_randomly)
from trdg.utils import load_dict, load_fonts


def margins(margin):
    margins = margin.split(",")
    if len(margins) == 1:
        return [int(margins[0])] * 4
    return [int(m) for m in margins]


def parse_arguments():
    """
        Parse the command line arguments of the program.
    """

    parser = argparse.ArgumentParser(
        description="Generate synthetic text data for text recognition."
    )
    parser.add_argument(
        "--output_dir", type=str, nargs="?", help="The output directory", default="./out/"
    )
    parser.add_argument(
        "-i",
        "--input_file",
        type=str,
        nargs="?",
        help="When set, this argument uses a specified text file as source for the text",
        default="",
    )
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        nargs="?",
        help="The language to use, should be fr (French), en (English), es (Spanish), de (German), ar (Arabic), cn (Chinese), ja (Japanese) or hi (Hindi)",
        default="en",
    )
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        nargs="?",
        help="The number of images to be created.",
        required=False,
        default=1
    )
    parser.add_argument(
        "-rs",
        "--random_sequences",
        action="store_true",
        help="Use random sequences as the source text for the generation. Set '-let','-num','-sym' to use letters/numbers/symbols. If none specified, using all three.",
        default=False,
    )
    parser.add_argument(
        "-let",
        "--include_letters",
        action="store_true",
        help="Define if random sequences should contain letters. Only works with -rs",
        default=False,
    )
    parser.add_argument(
        "-num",
        "--include_numbers",
        action="store_true",
        help="Define if random sequences should contain numbers. Only works with -rs",
        default=False,
    )
    parser.add_argument(
        "-sym",
        "--include_symbols",
        action="store_true",
        help="Define if random sequences should contain symbols. Only works with -rs",
        default=False,
    )
    parser.add_argument(
        "-w",
        "--length",
        type=int,
        nargs="?",
        help="Define how many words should be included in each generated sample. If the text source is Wikipedia, this is the MINIMUM length",
        default=1,
    )
    parser.add_argument(
        "-r",
        "--random",
        action="store_true",
        help="Define if the produced string will have variable word count (with --length being the maximum)",
        default=False,
    )
    parser.add_argument(
        "-f",
        "--format",
        type=int,
        nargs="?",
        help="Define the height of the produced images if horizontal, else the width",
        default=32,
    )
    parser.add_argument(
        "-t",
        "--thread_count",
        type=int,
        nargs="?",
        help="Define the number of thread to use for image generation",
        default=1,
    )
    parser.add_argument(
        "-e",
        "--extension",
        type=str,
        nargs="?",
        help="Define the extension to save the image with",
        default="png",
    )
    parser.add_argument(
        "-k",
        "--skew_angle",
        type=int,
        nargs="?",
        help="Define skewing angle of the generated text. In positive degrees",
        default=0,
    )
    parser.add_argument(
        "-rk",
        "--random_skew",
        action="store_true",
        help="When set, the skew angle will be randomized between the value set with -k and it's opposite",
        default=False,
    )
    parser.add_argument(
        "-wk",
        "--use_wikipedia",
        action="store_true",
        help="Use Wikipedia as the source text for the generation, using this parameter ignores -r, -n, -s",
        default=False,
    )
    parser.add_argument(
        "-bl",
        "--blur",
        type=int,
        nargs="?",
        help="Apply gaussian blur to the resulting sample. Should be an integer defining the blur radius",
        default=0,
    )
    parser.add_argument(
        "-rbl",
        "--random_blur",
        action="store_true",
        help="When set, the blur radius will be randomized between 0 and -bl.",
        default=False,
    )
    parser.add_argument(
        "-b",
        "--background",
        type=int,
        nargs="?",
        help="Define what kind of background to use. 0: Gaussian Noise, 1: Plain white, 2: Quasicrystal, 3: Image 4: transparent background",
        default=0,
    )
    parser.add_argument(
        "-hw",
        "--handwritten",
        action="store_true",
        help='Define if the data will be "handwritten" by an RNN',
    )
    parser.add_argument(
        "-na",
        "--name_format",
        type=int,
        help="""
            Define how the produced files will be named. 
            0: [TEXT]_[ID].[EXT], 
            1: [ID]_[TEXT].[EXT] 
            2: [ID].[EXT] + one file labels.txt containing id-to-label mappings
            3: [ID].[EXT] + [ID].txt containing label i.e text of each image
            4: [ID].[EXT] without label -- suitable for font identification and language classification data -- no labels required in that
        """,
        default=0,
    )
    parser.add_argument(
        "-om",
        "--output_mask",
        type=int,
        help="Define if the generator will return masks for the text",
        default=0,
    )
    parser.add_argument(
        "-obb",
        "--output_bboxes",
        type=int,
        help="Define if the generator will return bounding boxes for the text, 1: Bounding box file, 2: Tesseract format",
        default=0
    )
    parser.add_argument(
        "-d",
        "--distorsion",
        type=int,
        nargs="?",
        help="Define a distorsion applied to the resulting image. 0: None (Default), 1: Sine wave, 2: Cosine wave, 3: Random",
        default=0,
    )
    parser.add_argument(
        "-do",
        "--distorsion_orientation",
        type=int,
        nargs="?",
        help="Define the distorsion's orientation. Only used if -d is specified. 0: Vertical (Up and down), 1: Horizontal (Left and Right), 2: Both",
        default=0,
    )
    parser.add_argument(
        "-wd",
        "--width",
        type=int,
        nargs="?",
        help="Define the width of the resulting image. If not set it will be the width of the text + 10. If the width of the generated text is bigger that number will be used",
        default=-1,
    )
    parser.add_argument(
        "-al",
        "--alignment",
        type=int,
        nargs="?",
        help="Define the alignment of the text in the image. Only used if the width parameter is set. 0: left, 1: center, 2: right",
        default=1,
    )
    parser.add_argument(
        "-or",
        "--orientation",
        type=int,
        nargs="?",
        help="Define the orientation of the text. 0: Horizontal, 1: Vertical",
        default=0,
    )
    parser.add_argument(
        "-tc",
        "--text_color",
        type=str,
        nargs="?",
        help="Define the text's color, should be either a single hex color or a range in the ?,? format.",
        default="#282828",
    )
    parser.add_argument(
        "-sw",
        "--space_width",
        type=float,
        nargs="?",
        help="Define the width of the spaces between words. 2.0 means twice the normal space width",
        default=1.0,
    )
    parser.add_argument(
        "-cs",
        "--character_spacing",
        type=int,
        nargs="?",
        help="Define the width of the spaces between characters. 2 means two pixels",
        default=0,
    )
    parser.add_argument(
        "-m",
        "--margins",
        type=margins,
        nargs="?",
        help="Define the margins around the text when rendered. In pixels",
        default=(5, 5, 5, 5),
    )
    parser.add_argument(
        "-fi",
        "--fit",
        action="store_true",
        help="Apply a tight crop around the rendered text",
        default=False,
    )
    parser.add_argument(
        "-ft", "--font", type=str, nargs="?", help="Define font to be used"
    )
    parser.add_argument(
        "-fd",
        "--font_dir",
        type=str,
        nargs="?",
        help="Define a font directory to be used",
    )
    parser.add_argument(
        "-id",
        "--image_dir",
        type=str,
        nargs="?",
        help="Define an image directory to use when background is set to image",
        default=os.path.join(os.path.split(os.path.realpath(__file__))[0], "images"),
    )
    parser.add_argument(
        "-ca",
        "--case",
        type=str,
        nargs="?",
        help="Generate upper or lowercase only. arguments: upper or lower. Example: --case upper",
    )
    parser.add_argument(
        "-dt", "--dict", type=str, nargs="?", help="Define the dictionary to be used"
    )
    parser.add_argument(
        "-ws",
        "--word_split",
        action="store_true",
        help="Split on words instead of on characters (preserves ligatures, no character spacing)",
        default=True,
    )
    parser.add_argument(
        "-stw",
        "--stroke_width",
        type=int, 
        nargs="?",
        help="Define the width of the strokes",
        default=0,
    )
    parser.add_argument(
        "-stf",
        "--stroke_fill",
        type=str, 
        nargs="?",
        help="Define the color of the contour of the strokes, if stroke_width is bigger than 0",
        default="#282828",
    )
    parser.add_argument(
        "-im",
        "--image_mode",
        type=str,
        nargs="?",
        help="Define the image mode to be used. RGB is default, L means 8-bit grayscale images, 1 means 1-bit binary images stored with one pixel per byte, etc.",
        default="RGBA",
    )

    ## -----------------------------------------------
    ## Newly added parameters by Nivratti

    """
    1. preserver indexing :
        if preserve_indexing set to True -- it will pick elements by order. If count going above dict size then it will be repeated -- ex. if count is 500 and length of dict 498(total dict lines), then all values will be taken and process is repeated for remaining count i.e. 2 more first dict values will be picked

        Useful in : 
            1) Document card synth : In Qatar document id person name is in both english and arabic needs to be rendered and for that we use two different dictionaries to generate data. And we need to preserve indexing to get equivalent item by order
    """
    parser.add_argument(
        "-pi",
        "--preserve_indexing",
        action="store_true",
        help="if preserve_indexing set to True -- it will pick elements by order.",
        default=False,
    )
    parser.add_argument(
        "-fsd",
        "--font_wise_separate_data",
        action="store_true",
        help="""
            if font_wise_separate_data set to True it will store data for each font
            else it will generate original format mix of data. Default to false.
        """,
        default=False,
    )
    parser.add_argument(
        "--input_strings", default=[], nargs='*',
        help="Option to pass tet directly from command line. It haws highest priority over others if this passed by suer"
    )
    parser.add_argument(
        "-rmg",
        "--random_margin",
        action="store_true",
        help="""
        Apply random diffrent margin around image. As text detector result will be of 
        diffrent pixels margin around detected text, so enabling this can mimic similar same behaviour.
        """,
        default=False,
    )
    return parser.parse_args()

def generate_text_data(
        alignment=1, background=0, blur=0, case=None, character_spacing=0, count=1, 
        dict=None, distorsion=0, distorsion_orientation=0, extension='png', 
        fit=False, font=None, font_dir=None, format=32, handwritten=False, 
        image_dir='./images', image_mode='RGBA', 
        include_letters=False, include_numbers=False, include_symbols=False, 
        input_file='', language='en', length=1, margins=(5, 5, 5, 5), 
        name_format=3, orientation=0, output_bboxes=0, output_dir='./out/',
        output_mask=0, preserve_indexing=False, random=False, random_blur=False, 
        random_sequences=False, random_skew=False, skew_angle=0, space_width=1.0, 
        stroke_fill='#282828', stroke_width=0, text_color='#282828', thread_count=1, 
        use_wikipedia=False, width=-1, word_split=True,
        font_wise_separate_data=False, input_strings=[], random_margin=False,
    ):
    """
    Generate text data
    TODO: add doc details later

    Args:
        alignment (int, optional): _description_. Defaults to 1.
        background (int, optional): _description_. Defaults to 0.
        blur (int, optional): _description_. Defaults to 0.
        case (_type_, optional): _description_. Defaults to None.
        character_spacing (int, optional): _description_. Defaults to 0.
        count (int, optional): _description_. Defaults to 1.
        dict (_type_, optional): _description_. Defaults to None.
        distorsion (int, optional): _description_. Defaults to 0.
        distorsion_orientation (int, optional): _description_. Defaults to 0.
        extension (str, optional): _description_. Defaults to 'png'.
        fit (bool, optional): _description_. Defaults to False.
        font (_type_, optional): _description_. Defaults to None.
        font_dir (_type_, optional): _description_. Defaults to None.
        format (int, optional): _description_. Defaults to 32.
        handwritten (bool, optional): _description_. Defaults to False.
        image_dir (str, optional): _description_. Defaults to './images'.
        image_mode (str, optional): _description_. Defaults to 'RGBA'.
        include_letters (bool, optional): _description_. Defaults to False.
        include_numbers (bool, optional): _description_. Defaults to False.
        include_symbols (bool, optional): _description_. Defaults to False.
        input_file (str, optional): _description_. Defaults to ''.
        language (str, optional): _description_. Defaults to 'en'.
        length (int, optional): _description_. Defaults to 1.
        margins (tuple, optional): _description_. Defaults to (5, 5, 5, 5).
        name_format (int, optional): _description_. Defaults to 3.
        orientation (int, optional): _description_. Defaults to 0.
        output_bboxes (int, optional): _description_. Defaults to 0.
        output_dir (str, optional): _description_. Defaults to './out/'.
        output_mask (int, optional): _description_. Defaults to 0.
        preserve_indexing (bool, optional): _description_. Defaults to False.
        random (bool, optional): _description_. Defaults to False.
        random_blur (bool, optional): _description_. Defaults to False.
        random_sequences (bool, optional): _description_. Defaults to False.
        random_skew (bool, optional): _description_. Defaults to False.
        skew_angle (int, optional): _description_. Defaults to 0.
        space_width (float, optional): _description_. Defaults to 1.0.
        stroke_fill (str, optional): _description_. Defaults to '#282828'.
        stroke_width (int, optional): _description_. Defaults to 0.
        text_color (str, optional): _description_. Defaults to '#282828'.
        thread_count (int, optional): _description_. Defaults to 1.
        use_wikipedia (bool, optional): _description_. Defaults to False.
        width (int, optional): _description_. Defaults to -1.
        word_split (bool, optional): _description_. Defaults to True.
        font_wise_separate_data (bool, optional): _description_. Defaults to False.
        random_margin(bool, optional): If true, it will add rando margin around rendered text.
    """
    # Create the directory if it does not exist.
    try:
        os.makedirs(output_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Creating word list
    if dict:
        lang_dict = []
        if os.path.isfile(dict):
            with open(dict, "r", encoding="utf8", errors="ignore") as d:
                lang_dict = [l for l in d.read().splitlines() if len(l) > 0]
        else:
            sys.exit("Cannot open dict")
    else:
        lang_dict = load_dict(language)

    # Create font (path) list
    if font_dir:
        fonts = [
            os.path.join(font_dir, p)
            for p in os.listdir(font_dir)
            if os.path.splitext(p)[1] == ".ttf"
        ]
    elif font:
        if os.path.isfile(font):
            fonts = [font]
        else:
            sys.exit("Cannot open font")
    else:
        fonts = load_fonts(language)

    if input_strings:
        strings = input_strings
    else:
        # Creating synthetic sentences (or word)
        strings = []

        if use_wikipedia:
            strings = create_strings_from_wikipedia(length, count, language)
        elif input_file != "":
            strings = create_strings_from_file(input_file, count)
        elif random_sequences:
            strings = create_strings_randomly(
                length,
                random,
                count,
                include_letters,
                include_numbers,
                include_symbols,
                language,
            )
            # Set a name format compatible with special characters automatically if they are used
            if include_symbols or True not in (
                include_letters,
                include_numbers,
                include_symbols,
            ):
                name_format = 2
        else:
            strings = create_strings_from_dict(
                length, random, count, lang_dict, 
                preserve_indexing=preserve_indexing
            )

    if language == "ar":
        from arabic_reshaper import ArabicReshaper
        from bidi.algorithm import get_display

        arabic_reshaper = ArabicReshaper()
        # strings = [
        #     " ".join([get_display(arabic_reshaper.reshape(w)) for w in s.split(" ")[::-1]])
        #     for s in strings
        # ]
        ## changes -- 17-11-2022
        ## get strings without RTL display
        ## to properly render UAE identity card
        strings = [
            " ".join([arabic_reshaper.reshape(w) for w in s.split(" ")[::-1]])
            for s in strings
        ]
    if case == "upper":
        strings = [x.upper() for x in strings]
    if case == "lower":
        strings = [x.lower() for x in strings]

    string_count = len(strings)

    if thread_count == 1:
        # no Pool -- so debugging will be better
        fonts = [fonts[rnd.randrange(0, len(fonts))] for _ in range(0, string_count)]

        for index in tqdm(range(0, string_count)):
            FakeTextDataGenerator.generate(
                index=index,
                text=strings[index],
                font=fonts[index],
                out_dir=output_dir,
                size=format,
                extension=extension,
                skewing_angle=skew_angle,
                random_skew=random_skew,
                blur=blur,
                random_blur=random_blur,
                background_type=background,
                distorsion_type=distorsion,
                distorsion_orientation=distorsion_orientation,
                is_handwritten=handwritten,
                name_format=name_format,
                width=width,
                alignment=alignment,
                text_color=text_color,
                orientation=orientation,
                space_width=space_width,
                character_spacing=character_spacing,
                margins=margins,
                fit=fit,
                output_mask=output_mask,
                word_split=word_split,
                image_dir=image_dir,
                stroke_width=stroke_width, 
                stroke_fill=stroke_fill,
                image_mode=image_mode, 
                output_bboxes=output_bboxes,
                random_margin=random_margin,
            )
    else:
        p = Pool(thread_count)
        for _ in tqdm(
            p.imap_unordered(
                FakeTextDataGenerator.generate_from_tuple,
                zip(
                    [i for i in range(0, string_count)],
                    strings,
                    [fonts[rnd.randrange(0, len(fonts))] for _ in range(0, string_count)],
                    [output_dir] * string_count,
                    [format] * string_count,
                    [extension] * string_count,
                    [skew_angle] * string_count,
                    [random_skew] * string_count,
                    [blur] * string_count,
                    [random_blur] * string_count,
                    [background] * string_count,
                    [distorsion] * string_count,
                    [distorsion_orientation] * string_count,
                    [handwritten] * string_count,
                    [name_format] * string_count,
                    [width] * string_count,
                    [alignment] * string_count,
                    [text_color] * string_count,
                    [orientation] * string_count,
                    [space_width] * string_count,
                    [character_spacing] * string_count,
                    [margins] * string_count,
                    [fit] * string_count,
                    [output_mask] * string_count,
                    [word_split] * string_count,
                    [image_dir] * string_count,
                    [stroke_width] * string_count,
                    [stroke_fill] * string_count,
                    [image_mode] * string_count,
                    [output_bboxes] * string_count,
                    [random_margin] * string_count,
                ),
            
            ),
            total=count,
        ):
            pass
        p.terminate()

    if name_format == 2:
        # Create file with filename-to-label connections
        with open(
            os.path.join(output_dir, "labels.txt"), "w", encoding="utf8"
        ) as f:
            for i in range(string_count):
                file_name = str(i) + "." + extension

                ## Check is file exists before writing it in label file
                file_abs_path = os.path.join(output_dir, file_name)
                if not os.path.exists(file_abs_path):
                    continue

                label = strings[i]
                # print(f"label: ", label)
                if space_width == 0:
                    label = label.replace(" ", "")
                f.write("{} {}\n".format(file_name, label))

def main():
    """
        Description: Main function
    """
    from pathlib import Path

    # Argument parsing
    args = parse_arguments()

    # # dev purpose
    # import ipdb;ipdb.set_trace()

    if args.font_wise_separate_data:
        # Create font (path) list
        if args.font_dir:
            fonts = [
                os.path.join(args.font_dir, p)
                for p in os.listdir(args.font_dir)
                if os.path.splitext(p)[1] == ".ttf"
            ]
        elif args.font:
            if os.path.isfile(args.font):
                fonts = [args.font]
            else:
                sys.exit("Cannot open font")
        else:
            fonts = load_fonts(args.language)

        # TODO -- replace print messages with loguru logger
        print(f"INFO : Total font files: {len(fonts)}")

        # KEEP ORIGINAL OUTPUT DIR
        original_output_dir = args.output_dir

        for font in fonts:
            font_stem = Path(font).stem
            print(f"=" * 50)
            print(f"Generating data for font : {font_stem}")
            args_dict = vars(args)

            # update font and output dir
            args_dict["font_dir"] = None
            args_dict["font"] = font
            args_dict["output_dir"] = os.path.join(original_output_dir, font_stem)
            os.makedirs(args_dict["output_dir"], exist_ok=True)

            # pass argparse argument to function as-kwargs
            generate_text_data(**args_dict)
            print("\n")
    else:
        ## Default mode
        generate_text_data(**vars(args))


if __name__ == "__main__":
    main()

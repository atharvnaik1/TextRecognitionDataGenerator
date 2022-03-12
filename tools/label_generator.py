import os
import shutil
from pathlib import Path
from nb_utils.file_dir_handling import list_files
import pandas as pd
from tqdm.auto import tqdm

dir_dataset_parent = "/home/nivratti/Desktop/TextRecognitionDataGenerator/dataset/march-12/"

display_message = False
cnt_successful = 0

# lst_subfoldernames = []
# ## Auto generate from pattern
# total_subfolders = 18
# for i in range(1, total_subfolders + 1):
#     subfoldername = f"out-Amiri-Regular-500k-all-news-corpus-chunk-{i:02}"
#     lst_subfoldernames.append(subfoldername)

lst_subfoldernames = [
    "out-Latif-Regular-all-news-corpus-chunk-08",
    # "out-Naskh-Regular-all-news-corpus-chunk-05",
    # "out-Naskh-Regular-all-news-corpus-chunk-06",
    # "out-Naskh-Regular-all-news-corpus-chunk-07",
    # "out-Latif-Regular-all-news-corpus-chunk-08",
    # "out-Latif-Regular-all-news-corpus-chunk-09",
    # "out-Latif-Regular-all-news-corpus-chunk-10",
]

for subfoldername in lst_subfoldernames:
    print("=" * 100)

    subfolder_path = os.path.join(dir_dataset_parent, subfoldername)
    print(f"subfolder_path: ", subfolder_path)

    if not os.path.exists(subfolder_path):
        print(f"Error... Subfolder path not exists.. skipping")
        continue

    ## read label file
    original_label_filename = os.path.join(subfolder_path, "labels.txt")

    df = pd.read_csv(original_label_filename, sep=r"\s+", names=["filename", "words"], engine='python', error_bad_lines=True)

    lst_filename = []
    words = []
    # df = df.reset_index()  # make sure indexes pair with number of rows
    for index, row in df.iterrows():
        # print(row['c1'], row['c2'])
        img_filename = row['filename']
        if display_message: print(f"img_filename: ", img_filename)

        label = row['words']

        img_file_abspath = os.path.join(subfolder_path, img_filename)
        if not os.path.exists(img_file_abspath) or label is None:
            continue

        lst_filename.append(img_filename)
        words.append(label)

    ## create df
    new_df = pd.DataFrame({
        "filename": lst_filename,
        "words": words
    })

    out_filepath = os.path.join(subfolder_path, "label-modified.txt")
    new_df.to_csv(out_filepath, sep='\t', index=None, header=None)

    ## add parent folder-name in filename
    new_df['filename'] = f"{subfoldername}/" + new_df['filename'].astype("str")
    out_filepath = os.path.join(subfolder_path, "label-with-parent-name.txt")
    new_df.to_csv(out_filepath, sep='\t', index=None, header=None)

    import pdb;pdb.set_trace()
    # # copy inside parentnew_df
    # out_filepath_parent = os.path.join(os.path.dirname(subfolder_path), "label-with-parent-name.txt")
    # shutil.copy(out_filepath, out_filepath_parent)

    print(f"Subfolder processing done... label files written on disk")
    cnt_successful += 1

print(f"cnt_successful: ", cnt_successful)
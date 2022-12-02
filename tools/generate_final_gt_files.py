import os
import shutil
from pathlib import Path
from nb_utils.file_dir_handling import list_files
import pandas as pd
from tqdm.auto import tqdm

dir_dataset_parent = "/home/nivratti/Desktop/TextRecognitionDataGenerator/dataset-march-10-contextual-form"

lst_train_subfoldernames = [
    "new_ar-Amiri-Regular-500k-all-news-corpus-chunk-02",
    "new_ar-Amiri-Regular-500k-all-news-corpus-chunk-03",
]

lst_test_subfoldernames = [
    "new_ar-Amiri-Regular-4k-all-news-corpus-chunk-01",
    "new_ar-Amiri-Regular-100k-all-news-corpus-chunk-01",
]

lst_train_labelfiles = []
for subfoldername in lst_train_subfoldernames:
    print("=" * 100)

    subfolder_path = os.path.join(dir_dataset_parent, subfoldername)
    print(f"subfolder_path: ", subfolder_path)

    if not os.path.exists(subfolder_path):
        print(f"Error... Subfolder path not exists.. skipping")
        continue

    ## label file
    label_filepath = os.path.join(subfolder_path, "label-with-parent-name.txt")
    lst_train_labelfiles.append(label_filepath)


lst_test_labelfiles = []
for subfoldername in lst_test_subfoldernames:
    print("=" * 100)

    subfolder_path = os.path.join(dir_dataset_parent, subfoldername)
    print(f"subfolder_path: ", subfolder_path)

    if not os.path.exists(subfolder_path):
        print(f"Error... Subfolder path not exists.. skipping")
        continue

    ## label file
    label_filepath = os.path.join(subfolder_path, "label-with-parent-name.txt")

    lst_test_labelfiles.append(label_filepath)

print(f"\n lst_train_labelfiles: ", lst_train_labelfiles)
print(f"\n lst_test_labelfiles: ", lst_test_labelfiles, "\n")


# -------------------
li = []
for filename in lst_train_labelfiles:
    df = pd.read_csv(filename, sep='\t', names=["filename", "words"], engine='python') ## paddleocr format
    li.append(df)

train_df = pd.concat(li, axis=0, ignore_index=True)

out_filepath = os.path.join(dir_dataset_parent, "rec_gt_train_combined.txt")
train_df.to_csv(out_filepath, sep='\t', index=None, header=None)

# ----------------------------
li = []
for filename in lst_test_labelfiles:
    df = pd.read_csv(filename, sep='\t', names=["filename", "words"], engine='python') ## paddleocr format
    li.append(df)

test_df = pd.concat(li, axis=0, ignore_index=True)
out_filepath = os.path.join(dir_dataset_parent, "rec_gt_test_combined.txt")
test_df.to_csv(out_filepath, sep='\t', index=None, header=None)

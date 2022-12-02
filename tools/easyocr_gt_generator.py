import os
from pathlib import Path
import shutil
import pandas as pd
from collections import Counter

raw_data_folder_path = "/home/nivratti/Desktop/TextRecognitionDataGenerator/dataset-march-contextual-form/march-14-sample/"

train_out_path = "/home/nivratti/Desktop/TextRecognitionDataGenerator/dataset-march-contextual-form/ar_train_filtered"
os.makedirs(train_out_path, exist_ok=True)

val_out_path = "/home/nivratti/Desktop/TextRecognitionDataGenerator/dataset-march-contextual-form/val_filtered"
os.makedirs(val_out_path, exist_ok=True)

##--------------------------------------------------------------------
directories_in_base_dir = [f.name for f in Path(raw_data_folder_path).iterdir() if f.is_dir()]
print("Directories in base dir: ", *directories_in_base_dir, sep="\n")

lst_val_subfoldernames = [
    "new_ar-sample-500"
]
skip_val_subfoldernames_from_train = False # True

lst_train_subfoldernames = []
if skip_val_subfoldernames_from_train and lst_val_subfoldernames:
    lst_train_subfoldernames = list(Counter(directories_in_base_dir) - Counter(lst_val_subfoldernames))
else:
    lst_train_subfoldernames = directories_in_base_dir

print(f"lst_val_subfoldernames: ", lst_val_subfoldernames, "\n")
print(f"lst_train_subfoldernames: ", lst_train_subfoldernames, "\n")

## ----------------------------------------------------------------

def generate_easyocr_gt_file(lst_subfoldernames, out_path, file_operation):
    """
    Generate easyocr gt files from given list of foldernames
    """
    li = []
    for subfoldername in lst_subfoldernames:
        # print("=" * 100)

        subfolder_path = os.path.join(raw_data_folder_path, subfoldername)
        # print(f"subfolder_path: ", subfolder_path)

        filename = os.path.join(subfolder_path, "label-with-parent-name.txt")
        df = pd.read_csv(filename, sep='\t', names=["filename", "words"], engine='python', error_bad_lines=False) ## paddleocr format
        li.append(df)

    df = pd.concat(li, axis=0, ignore_index=True)
    # print(f"df.head: ", df.head())
    print(f"df.info: ", df.info())

    ## ---------------------------------------------------------------------
    new_filenames = []
    labels = []

    file_operation = "copy"  # move
    for index, row in df.iterrows():
        # print(f"index: ", index)
        # print(f"row: ", row)
        filepath = row["filename"]
        file_suffix = Path(filepath).suffix
        input_file_fullpath = os.path.join(raw_data_folder_path, filepath)

        new_filename = f"{index}{file_suffix}"
        out_filepath = os.path.join(out_path, new_filename)

        if os.path.exists(input_file_fullpath):
            if file_operation == "move":
                dest = shutil.move(input_file_fullpath, out_filepath)
            else:
                dest = shutil.copy2(input_file_fullpath, out_filepath)

            new_filenames.append(new_filename)
            labels.append(row["words"])

    ## Append filename string at index 0 in new files
    ## and append words string at index 0 in labels
    ## as per easyocr format
    if not new_filenames[0] == "filename":
        new_filenames.insert(0, "filename")
        labels.insert(0, "words")

    new_df = pd.DataFrame(
        {
            "filename": new_filenames,
            "words": labels
        }
    )
    # new_df.head()

    ## Save new train df
    out_filepath = os.path.join(out_path, "labels.csv")
    new_df.to_csv(out_filepath, header=None, index=None)
    print(f"Easyocr label format annonation written to disk..")

def main():
    ## 1. Training data
    print(f"Processing train:")
    generate_easyocr_gt_file(
        lst_train_subfoldernames, 
        train_out_path, 
        file_operation="copy"
    )
    ## 2. val
    print(f"Processing Val:")
    generate_easyocr_gt_file(
        lst_val_subfoldernames, 
        val_out_path, 
        file_operation="copy"
    )

if __name__ == "__main__":
    main()
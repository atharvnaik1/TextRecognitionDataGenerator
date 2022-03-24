from tqdm import tqdm
import io
import regex
import os
from datasets import load_dataset


lst_names = ["Alittihad", "Almasryalyoum", "Almustaqbal", "Alqabas", "Echoroukonline", "Ryiadh", "Sabanews", "SaudiYoum", "Techreen", "Youm7"]

out_dir_final_txt = "final_txt"
os.makedirs(out_dir_final_txt, exist_ok=True)

all_newspaper_arabic_processed_words = []

for newspaper_name in lst_names:
    print("=" * 100)
    print(f"newspaper_name: ", newspaper_name)

    out_file = os.path.join(out_dir_final_txt, f"{newspaper_name}-unique-words.txt")
    if os.path.exists(out_file):
      print(f"Already processed this newspaper ... final file exists on disk..")
      continue

    dataset = load_dataset("arabic_billion_words", newspaper_name)

    all_arabic_processed_words = []
    for single_text_str in tqdm(dataset["train"]["text"]):
        # print(single_text_str)
        lst_raw_txt = single_text_str.split(" ")

        for raw_txt in lst_raw_txt:
            only_arabic = regex.sub(r'[^\u0600-\u06FF]', u'', raw_txt)
            # print(only_arabic)

            if only_arabic and (len(only_arabic) > 2) and (len(only_arabic) <= 30):
              all_arabic_processed_words.append(only_arabic)

    print(f"All words count: ", len(all_arabic_processed_words))

    ## Remove duplicates
    # using set()
    # to remove duplicated 
    # from list 
    lst_unique_all_arabic_processed_words = list(set(all_arabic_processed_words))

    print(f"Length of unique words : ", len(lst_unique_all_arabic_processed_words))
    
    with io.open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lst_unique_all_arabic_processed_words))

    ## finally extend all newspaper list
    all_newspaper_arabic_processed_words.extend(lst_unique_all_arabic_processed_words)
    

print(f"All newspaper words: ", len(all_newspaper_arabic_processed_words))

lst_unique_all_newspaper_arabic_processed_words = list(set(all_newspaper_arabic_processed_words))
print(f"Length of all newspaper unique words : ", len(lst_unique_all_newspaper_arabic_processed_words))

out_file_all_newspapers = os.path.join(out_dir_final_txt, f"all-newspapers-unique-words.txt")
with io.open(out_file_all_newspapers, "w", encoding="utf-8") as f:
    f.write("\n".join(lst_unique_all_newspaper_arabic_processed_words))


import pdb; pdb.set_trace()
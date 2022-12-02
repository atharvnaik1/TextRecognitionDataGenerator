import os

arabic_dict_file = "/home/nivratti/Downloads/arabic_dict.txt"

with open(arabic_dict_file) as f:
    lines = [line.rstrip('\n') for line in f]

dict_chars = lines
print(f"dict_chars: ", dict_chars)

# -----------------------------------------------
# print("\nWe are listing new_ar only the directories in current directory -")
from pathlib import Path

# All subdirectories in the current directory, not recursive.
base_dir = "/home/nivratti/Desktop/PaddleOCR/train_data/"
p = Path(base_dir)
directories_in_basedir = [f for f in p.iterdir() if f.is_dir()]
print(f"directories_in_basedir:", directories_in_basedir)

extra_chars = set()
for directory in directories_in_basedir:
	arabic_label_file = os.path.join(directory, "label-with-parent-name.txt")

	with open(arabic_label_file) as f:
		lines = [line.rstrip('\n') for line in f]

	for text_line in lines:
		all_chars = [char for char in text_line]

		for char in all_chars:
			if not char in dict_chars:
				extra_chars.add(char)

print(f"extra_chars: ", extra_chars)

file_extra_chars = "extra_chars.txt"
with open(file_extra_chars, "w", encoding="utf-8") as f:
    f.write("\n".join(list(extra_chars)))

# import pdb;pdb.set_trace()

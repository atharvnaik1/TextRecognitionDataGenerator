import os

# arabic_dict_file = "/home/nivratti/Downloads/arabic_dict.txt"
arabic_dict_file = "/home/nivratti/Desktop/PaddleOCR/ppocr/utils/dict/arabic_dict_v2_with_contextual_chars.txt"

with open(arabic_dict_file) as f:
    lines = [line.rstrip('\n') for line in f]

dict_chars = lines
print(f"dict_chars: ", dict_chars)

# -----------------------------------------------
# print("\nWe are listing new_ar only the directories in current directory -")
from pathlib import Path

# # All subdirectories in the current directory, not recursive.
# base_dir = "/home/nivratti/Desktop/PaddleOCR/train_data/"
# p = Path(base_dir)
# directories_in_basedir = [f for f in p.iterdir() if f.is_dir()]
# print(f"directories_in_basedir:", directories_in_basedir)

# lst_labelfiles = []
# for directory in directories_in_basedir:
# 	arabic_label_file = os.path.join(directory, "label-with-parent-name.txt")

# 	if os.path.exists(arabic_label_file):
# 		lst_labelfiles.append(arabic_label_file)
# 	else:
# 		print(f"Error...file {arabic_label_file} not found ..")

# or mannually specify -- labelsfiles
lst_labelfiles = [
	"old-label-format-1--gt-files/rec_gt_train_combined.txt",
	"old-label-format-1--gt-files/rec_gt_test_combined.txt"
]

# ----------------------------------------------------------------------
extra_chars = set()
for arabic_label_file in lst_labelfiles:
	with open(arabic_label_file) as f:
		lines = [line.rstrip('\n') for line in f]

	for text_line in lines:
		all_chars = [char for char in text_line]

		for char in all_chars:
			if not char in dict_chars:
				extra_chars.add(char)

print(f"extra_chars: ", extra_chars)

file_extra_chars = "extra_chars_v2.txt"
with open(file_extra_chars, "w", encoding="utf-8") as f:
    f.write("\n".join(list(extra_chars)))

# import pdb;pdb.set_trace()

import os
import random

DIR = os.path.join(os.getcwd(), "downloaded")
mp3_list = [file for file in os.listdir(DIR) if file.endswith(".mp3")]
idx = 1

while mp3_list:
    selected = random.randrange(len(mp3_list))
    file_name = mp3_list.pop(selected)

    old_path = os.path.join(DIR, file_name)
    new_path = os.path.join(DIR, f"{idx}. {file_name}")
    os.rename(old_path, new_path)

    idx += 1

print("Done!")

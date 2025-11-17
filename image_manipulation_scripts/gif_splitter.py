from PIL import Image
import sys
import os

#pass in path of gif file, will place folder containing split gif in the same directory with the same name
# for example:
#   Windows:
#   py gif_splitter.py .\gif_folder\my_gif.gif

#   Unix:
#   python gif_splitter.py ./gif_folder/my_gif.gif

target_gif = sys.argv[1]
split = target_gif.split(".gif")
folder_path = split[0]

if not os.path.exists(folder_path):
    os.makedirs(folder_path)
with Image.open(target_gif) as gif:
    length = gif.n_frames
    for i in range(length):
        gif.seek(i)
        gif.save(f'./{folder_path}/frame_{i}.png')
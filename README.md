# assorted tools

tools I made and use
feel free 2 use + modify

gif_splitter.py and image_resizer.py are made to be used together. I wrote them for this [project](https://github.com/anthonyjdelpino/pets-4-max).

gif_splitter.py will print the directory it put the frame images in, this can be piped into image_resizer.py

image_resizer.py will not resize gifs frame by frame and does not create backups, so be careful with it. It will verify if you want to continue, should you use it on a directory as it will resize everything in the directory (non-recursively).

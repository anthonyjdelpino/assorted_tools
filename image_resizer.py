from PIL import Image
import sys
import os
import sys
import argparse

valid_extensions = [
    ".apng", ".avif", ".avifs", ".blp", ".bmp", ".bufr", ".bw", ".cur", ".dcx",
    ".dds", ".dib", ".emf", ".eps", ".fit", ".fits", ".flc", ".fli", ".ftc",
    ".ftu", ".gbr", ".gif", ".grib", ".h5", ".hdf", ".icb", ".icns", ".ico",
    ".iim", ".im", ".j2c", ".j2k", ".j2p", ".jpc", ".jpe", ".jpeg", ".jpg",
    ".jpf", ".jp2", ".jpx", ".jfif", ".mpeg", ".mpg", ".msp", ".pbm", ".pcd",
    ".pcx", ".pfm", ".pgm", ".png", ".pnm", ".ppm", ".ps", ".psd", ".pxr",
    ".qoi", ".ras", ".rgb", ".rgba", ".sgi", ".tga", ".tif", ".tiff", ".vda",
    ".vst", ".webp", ".wmf", ".xbm", ".xpm"
]

arg_parser = argparse.ArgumentParser(description="Resize an image or all images in a directory. Provide the X and Y dimension OR a scaling factor.")
arg_parser.add_argument('-x', type=int, help="Pixels in X dimension to scale to")
arg_parser.add_argument('-y', type=int, help="Pixels in Y dimension to scale to")
arg_parser.add_argument('-s', '--scale', type=float, help="Scale image by factor in both dimensions")
arg_parser.add_argument('-m', '--method', choices=['NEAREST','BOX','BILINEAR','HAMMING','BICUBIC','LANCZOS'], default='NEAREST', help="Resampling method")
arg_parser.add_argument('-f', '--force', default=False, help="Bypass the warning on targeting a directory", action='store_true')
arg_parser.add_argument('-t','--target', help="Relative or absolute path to target file or directory. Optional if using STDIN piping to provide a target path")
arg_parser.add_argument('-e', '--extension', help="Apply resize only to this extension type", choices=valid_extensions)
arg_parser.add_argument('-l', '--list_extensions', help="Print a list of all accepted file extensions and exit", action='store_true')

args = arg_parser.parse_args()



if args.list_extensions:
    print(f'{valid_extensions}')
    sys.exit()

if args.target is None and sys.stdin.isatty():
    print("Enter a target path with the \'--target\' parameter or pipe in via stdout.")
    sys.exit()
if args.target is not None:
    target = args.target
else:
    target = sys.stdin.read().strip()

if args.extension is not None:
    extensions = args.extension
else:
    extensions = valid_extensions

size_x = None
size_y = None
using_scale = args.scale is not None
using_x = args.x is not None
using_y = args.y is not None

if (using_scale and (using_x or using_y)) or (using_x != using_y): # invalid combination of size options
    print("Enter BOTH -x and -y OR use --scale. These options cannot be mixed.")
    sys.exit()
elif using_scale:
    scale_factor = args.scale
    if scale_factor <= 0:
        print(f'Invalid scale factor of {scale_factor}. Enter a positive, non-zero value.')
        sys.exit()
else:
    size_x = args.x
    size_y = args.y
    if size_x <= 0 or size_y <= 0:
        print("Dimensions must be positive integers.")
        sys.exit()


method = {
    'NEAREST':  Image.NEAREST,
    'BOX':      Image.BOX,
    'BILINEAR': Image.BILINEAR,
    'HAMMING':  Image.HAMMING,
    'BICUBIC':  Image.BICUBIC,
    'LANCZOS':  Image.LANCZOS
}[args.method]

is_file = os.path.isfile(target) #check if targeting a file or a folder

if is_file: # is a file so scale it if its an image
    file_name, file_extension = os.path.splitext(target)
    if file_extension.lower() not in extensions:
        print(f'\'{file_extension}\' not using the specified extension')
    else:
        with Image.open(target) as image:
            if using_scale:
                x, y = image.size
                image = image.resize((int(x * scale_factor), int(y * scale_factor)), resample=method)
            else:
                image = image.resize((size_x, size_y), resample=method)
            image.save(target)
            print(f'file saved to {target}')
elif os.path.isdir(target): # is a directory so scale its image content
    #check if empty OR no relevant files and leave message if so
    directory_content = os.listdir(target)
    if len(directory_content) == 0:
        print(f'No files found in \'{target}\'')
    else:
        if not args.force:
            if len(extensions) == 1:
                message_string = extensions
            else:
                message_string = "supported extensions"
            print(f'The target path, \'{target}\' is a directory. This script will resize all images in the folder using {message_string}. Enter \"y\" to confirm.')
            response = input()
            if response.lower().strip() != "y":
                print("Cancelling operation")
                sys.exit()
        for item in directory_content:
            item_path = os.path.join(target, item)
            if os.path.isdir(item_path):
                continue
            item_name, item_extension = os.path.splitext(item)
            if item_extension.lower() in extensions:
                with Image.open(item_path) as image:
                    if using_scale:
                        x, y = image.size
                        image = image.resize((int(x * scale_factor), int(y * scale_factor)), resample=method)
                    else:
                        image = image.resize((size_x, size_y), resample=method)
                    image.save(item_path)
else:
    print(f'No file or directory found at \'{target}\'')

from PIL import Image, ExifTags
import re
from pathlib import Path
import argparse

def exif_rotate(image):
    has_exif = False
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation]=='Orientation':
            has_exif = True
            break

    if not has_exif: return image

    exif=dict(image._getexif().items())
    if exif[orientation] == 3:
        image=image.rotate(180, expand=True)
    elif exif[orientation] == 6:
        image=image.rotate(270, expand=True)
    elif exif[orientation] == 8:
        image=image.rotate(90, expand=True)

    return image

parser = argparse.ArgumentParser()
parser.add_argument("path", type=str)
args = parser.parse_args()


current = Path(args.path)

paths_and_indices = []

for image_p in current.iterdir():
    if image_p.is_file() and re.search("\.jpe?g$", image_p.name) is not None:
        number = re.search("[0-9]+", image_p.name)
        paths_and_indices.append((image_p, 0 if number is None else int(number.group(0))))

paths_and_indices.sort(key=lambda e: e[1])

start_image_p = paths_and_indices[0][0]
start_image = Image.open(start_image_p)
append_images = []
for image_p, _ in paths_and_indices[1:]:
    image = Image.open(image_p)
    image = exif_rotate(image)
    append_images.append(image)


start_image.save("pdf.pdf", "PDF", resolution=100, save_all=True, append_images=append_images)

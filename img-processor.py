from PIL import Image, ImageOps, ImageDraw, ImageFont
import os
import sys
import re

# Append image and dependencies folder to path
image_folder = '../images/'
dependencies_folder = '../dependencies/'

sys.path.append(dependencies_folder)

# Import Name Dictionary
from name_dict import name_dictionary
from settings import output_file_name

# Returns image name given its number
def get_image_name(number):
    return name_dictionary.get(number)

def find_chars_until_dot(str):
    find = re.compile(r"^[^.]*")
    m = re.search(find, str).group(0)
    return m

# Get list of image names and a list of image paths
def get_image_paths():
    image_name = [ f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    image_path = [image_folder + f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    return image_name, image_path

# Turn list of images into a pdf
def get_pdf(image_list):
    image_list[0].save("{}.pdf".format(output_file_name), save_all=True, append_images=images[1:], quality = 90)

# Adds title and styling to an image
def create_lookbook_image(image_path, name):
    image = Image.open(image_path)
    width, height = image.size
    f = ImageFont.truetype("PlayfairDisplay-VariableFont_wght.ttf", 150)
    txt=Image.new('L', (round(height * 0.6), 350) )
    d = ImageDraw.Draw(txt)
    d.text( ( 0, 0), name,  font=f, fill=255)
    w = txt.rotate(90,  expand=1)
    text_width, text_height = w.size
    image.paste( ImageOps.colorize(w, (0,0,0), (0,0,0)), (width - text_width, height - text_height - 200),  w)

    return image

def main():
    
    # Get image names and paths
    image_names, image_paths = get_image_paths()

    # Initiate image list
    ready_images_list = []

    # For i in images
    for i in range(len(image_paths)):

        # Check number at the start
        try:
            number = int(find_chars_until_dot(image_names[i]))
        except:
            print('Error: Image name doesn\'t start with a number --> ' + str(i))
        # Get image name from number        
        image_name = get_image_name(number)
        # Print image name on image
        ready_image = create_lookbook_image(image_paths[i], image_name)
        print(type(ready_image))
        # Add image in images list
        ready_images_list.append(ready_image)
        print(type(ready_images_list))
    # Make pdf from images
    ready_images_list[0].save("{}.pdf".format(output_file_name), save_all=True, append_images=ready_images_list[1:])

if __name__ == '__main__':
    main()
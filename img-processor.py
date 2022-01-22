from PIL import Image, ImageOps, ImageDraw, ImageFont
import os
import sys

# Append image and dependencies folder to path
image_folder = '../images/'
dependencies_folder = '../dependencies/'

sys.path.append(image_folder)
sys.path.append(dependencies_folder)

# Import Name Dictionary
from name_dict import name_dictionary
from settings import output_file_name

# Returns image name given its number
def get_image_name(number):
    pass

# Get list of image paths
def get_image_paths():
    my_images = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    return my_images

# Turn list of images into a pdf
def get_pdf(image_list):
    image_list[0].save("{}.pdf".format(output_file_name), save_all=True, append_images=images[1:], quality = 90)

# Adds title and styling to an image
def create_lookbook_image(number):
    im=Image.open(path)
    width, height = im.size
    f = ImageFont.truetype("PlayfairDisplay-VariableFont_wght.ttf", 150)
    txt=Image.new('L', (round(height * 0.6), 350) )
    d = ImageDraw.Draw(txt)
    d.text( ( 0, 0), "ADONIS | TEST",  font=f, fill=255)
    w=txt.rotate(90,  expand=1)
    text_width, text_height = w.size

    im.paste( ImageOps.colorize(w, (0,0,0), (0,0,0)), (width - text_width, height - text_height - 200),  w)
    
    return im

def main():
    
    # Get image paths

    # For i in images
    # Check number at the start

    # Get image name from number

    # Print image name on image

    # Add image in images list

    # Make pdf from images

    pass

if __name__ == '__main__':
    main()
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


def get_image_name(url):
    pass

def get_images_urls():
    my_images = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    return my_images


def get_pdf(image_list):
    images = [im,im2]
    images[0].save("out.pdf", save_all=True, append_images=images[1:], quality = 90)


def create_final_image(number):
    pass

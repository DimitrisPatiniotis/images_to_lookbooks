from PIL import Image, ImageOps, ImageDraw, ImageFont
from os import listdir, path, rename, remove
import sys
import re
from PyPDF2 import PdfFileMerger

# Append image and dependencies folder to path
image_folder = '../images/'
dependencies_folder = '../dependencies/'

sys.path.append(dependencies_folder)

# Import Name Dictionary
from name_dict import name_dictionary, code_name_dictionary, length_dictionary
from settings import output_file_name, font_family, font_size, pdf_quality, page_number, init_text_height, word_spacing, separator_size

# Returns image name given its number
def get_image_name(number):
    return name_dictionary.get(number)

def find_chars_until_dot(str):
    find = re.compile(r"^[^.]*")
    m = re.search(find, str).group(0)
    return m

# Get list of image names and a list of image paths
def get_image_paths():
    image_name = [ f for f in listdir(image_folder) if path.isfile(path.join(image_folder, f))]
    image_path = [image_folder + f for f in listdir(image_folder) if path.isfile(path.join(image_folder, f))]
    return image_name, image_path

# Turn list of images into a pdf
def get_pdf(image_list):
    image_list[0].save("{}.pdf".format(output_file_name), save_all=True, append_images=images[1:], quality = 90)

# Transform text from dictionary
def text_transform(text):
    return text.replace('+', '|')


def create_separator():
    font = ImageFont.truetype(font_family, separator_size)
    sep_width = font_size + 20
    sep_height = font_size + 20
    txt= Image.new('L', (sep_width, sep_height) )
    d = ImageDraw.Draw(txt)
    d.text(( 0, 0), '|', font=font, fill=255)
    w = txt.rotate(90,  expand=1)

    return w, sep_width, sep_height

def print_page_name(name, nfont):
    namelen=len(name)

    name_width = length_dictionary.get(namelen)
    name_height = font_size + 20
    txt= Image.new('L', (name_width, name_height) )
    d = ImageDraw.Draw(txt)
    d.text(( 0, 0), text_transform(name.upper()), font=nfont, fill=255)
    w = txt.rotate(90,  expand=1)

    return w, name_width, name_height, namelen

def print_cat_name(name, nfont):
    print(name.lower())
    cat = code_name_dictionary.get(name.lower())
    cat_len = len(cat)
    cat_width = round(cat_len * font_size * 0.8)

    cat_height = font_size + 20
    txt= Image.new('L', (cat_width, cat_height) )
    d = ImageDraw.Draw(txt)
    d.text(( 0, 0), text_transform(cat.upper()), font=nfont, fill=255)
    w = txt.rotate(0,  expand=1)

    return w, cat_width, cat_height, cat

def print_page_num(number, nfont):
    page_number_len = len(str(number))
    page_number_height = font_size + 20
    number_text = Image.new('L',(page_number_len * 55, page_number_height))
    n = ImageDraw.Draw(number_text)
    n.text(( 0, 0), str(number),  font=nfont, fill=255)
    l = number_text.rotate(0,  expand=1)

    return l, page_number_height, page_number_len

# Adds title and styling to an image
def create_lookbook_image(image_path, name, pgnmbr):

    image = Image.open(image_path)
    width, height = image.size

    items = name.split(' + ')
    num_items = len(items)
    font = ImageFont.truetype(font_family, font_size)

    total_height = init_text_height
    padding = word_spacing

    page_const = 285
    if pgnmbr > 9:
        page_const = 323
    if pgnmbr > 99:
        page_const = 358
    page_number = print_page_num(pgnmbr, font)
    page_number_img = page_number[0]
    page_number_height = page_number[1]
    page_number_len = page_number[2]
    image.paste( ImageOps.colorize(page_number_img, (0,0,0), (0,0,0)), (width - (page_const - page_number_len * 10), height - (total_height + page_number_height)), page_number_img)

    total_height += page_number_height + padding + 60

    a_separator = create_separator()

    for itemn in range(len(items)):
        item = items[itemn]

        page_main_name = print_page_name(item, font)
        page_name = page_main_name[0]
        page_name_height = page_main_name[1]
        page_name_width = page_main_name[2]
        name_len = page_main_name[3]
        text_height = length_dictionary.get(name_len)

        image.paste( ImageOps.colorize(page_name, (0,0,0), (0,0,0)), (width - (180 + page_name_width), height - (total_height + text_height)), page_name)
        total_height += text_height + 30

        cat_name, cat_height, cat_width, cat =  print_cat_name(item, font)
        # image.paste( ImageOps.colorize(cat_name, (0,0,0), (0,0,0)), (width - (210 + cat_width), height - (total_height + cat_height)), cat_name)
        if len(cat) == 3:
            constw = 229
        elif len(cat) == 4:
            constw = 265
        else:
            constw = 200
        if 'I' in cat:
            constw -= 15
        if itemn == 1 and pgnmbr == 1:
            image.paste( ImageOps.colorize(cat_name, (0,0,0), (0,0,0)), (width - (constw + cat_width), height - (total_height + 10)), cat_name)
        else:
            image.paste( ImageOps.colorize(cat_name, (0,0,0), (0,0,0)), (width - (constw + cat_width), height - (total_height + 10)), cat_name)
        cat_height = 160
        total_height += (cat_height + padding)

        if itemn != len(items) - 1:
            separator_char, separator_height, separator_width = a_separator
            image.paste( ImageOps.colorize(separator_char, (0,0,0), (0,0,0)), (width - (200 + cat_width - 8), height - (total_height + 30)), separator_char)
    return image

# Get list of pdfs in directory
def get_list_of_pdfs():
    files = [f for f in listdir('.') if path.isfile(f) and f.endswith(".pdf")]
    return files

def merge_pdfs(pdf_list):
    pdfs = pdf_list
    merger = PdfFileMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write(output_file_name + '.pdf')
    merger.close()

def order_list(mlist):
    ordered_list = []
    for i in range(len(mlist)):
        for l in mlist:
            if find_chars_until_dot(l) == str(i):
                ordered_list.append(l)
    return ordered_list

def get_image_path(name, path_list):
    return [ f for f in path_list if name in f][0]

def main():
    
    # Get image names and paths
    image_names, image_paths = get_image_paths()
    image_names = order_list(image_names)

    # Initiate image list
    ready_images_list = []
    final_pdfs = 1

    images_num = len(image_names)

    for i in range(images_num):
        # Check number at the start
        try:
            number = int(find_chars_until_dot(image_names[i]))
        except:
            print('Error: Image name doesn\'t start with a number --> ' + str(i))
        # Get image name from number        
        image_name = get_image_name(number)
        image_path = get_image_path(image_names[i], image_paths)
        # Print image name on image
        ready_image = create_lookbook_image(image_path, image_name, i + 1)
        # Add image in images list
        ready_images_list.append(ready_image)
        # print(i)

        # Clear Memory
        del ready_image

        # Gets out of memory around i == 250 with 8gb ram and 4k images
        if len(ready_images_list) == 10 or i == images_num - 1:
            ready_images_list[0].save("{}.output.pdf".format(final_pdfs), save_all=True, append_images=ready_images_list[1:], quality = pdf_quality)
            del ready_images_list
            ready_images_list = []
            final_pdfs += 1
        print(i)
    # Concatinate all pdfs, if more than 1 exist
    pdf_list = get_list_of_pdfs()
    if len(pdf_list) > 1:
        merge_pdfs(pdf_list)
        # Delete temp pdfs
        for pdf in pdf_list:
            if pdf != output_file_name + '.pdf':
                remove(pdf)
    elif len(pdf_list) == 1:
        rename(pdf_list[0], output_file_name + '.pdf')

if __name__ == '__main__':
    main()
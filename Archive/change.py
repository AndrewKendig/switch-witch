##v 2.0
import PySimpleGUI as sg
import os
import shutil
import configparser
from PIL import Image

def ucombopt(files_or_folders):
    obj = os.scandir(path=source_folder)
    out = []
    for entry in obj :
        if (files_or_folders == "files" and entry.is_file()) or (files_or_folders == "folders" and entry.is_dir()):
            out.append(os.path.relpath(entry))
    return out

def resize_image(img, size):
    return img.resize(size)

def copy_item(src, dst):
    if os.path.isfile(src):
        shutil.copy(src, dst)
    else:
        shutil.copytree(src, dst)

def do_it(selected_item, size):
    global itnum
    itnum = 0
    for f in os.listdir(destination_folder):
        os.remove(os.path.join(destination_folder, f))
    if seltype == "folders":
        for f in os.listdir(selected_item):
            resize_and_copy_images((selected_item + "\\" + f), size)
    else:
        resize_and_copy_images(selected_item, size)

def resize_and_copy_images(selected_item, size):
    global itnum
    basename = os.path.basename(selected_item)
    src = selected_item
    dst = os.path.join(destination_folder, basename)
    if os.path.isfile(src):
        img = Image.open(src)
        img_resized = resize_image(img, size)
        if copy_name == "none":
            loc = os.path.splitext(dst)[0] + ".png"
        else:
            if os.path.isfile(os.path.dirname(dst) + "\\" + copy_name):
                oname = os.path.splitext(copy_name)
                itnum += 1
                loc = os.path.dirname(dst) + "\\" + oname[0] + str(itnum) + oname[1]
            else:
                loc = os.path.dirname(dst) + "\\" + copy_name

        img_resized.save(loc)
    else:
        copy_item(src, dst)

## Load the configuration
config = configparser.ConfigParser()
if not os.path.exists('config.ini'):
    config['DEFAULT'] = {'source_folder': '.\\Source\\', 'destination_folder': ".\\Display\\", 'copy_name':"none", 'image_W': 300, 'image_H': 400}
    with open('.\\config.ini', 'w') as configfile:
        config.write(configfile)
else:
    config.read('.\\config.ini')

source_folder = config['DEFAULT']['source_folder']
destination_folder = config['DEFAULT']['destination_folder']
copy_name = config['DEFAULT']['copy_name']
image_W = int(config['DEFAULT']['image_W'])
image_H = int(config['DEFAULT']['image_H'])

## Check if source folder exists, create if not
if not os.path.exists(source_folder):
    os.makedirs(source_folder)

## Check if destination folder exists, create if not
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

itnum = 0

sg.theme('DarkGrey11')   

## set file list
combopt = ucombopt("files")
seltype = "files"

## UI
combo_style = {'size': (40, 1)}
layout = [  [sg.Text('Pick the FIle or Folder')],
            [sg.Combo(combopt, **combo_style, key="list"), sg.Button('Switch')],
            [sg.Radio("Files", "RADIO1", default=True, key="files"), sg.Radio("Folders", "RADIO1", key="folders"), sg.Button('Refresh')] ]

window = sg.Window('Image Switcher', layout)

## Logic
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Refresh':
        if values['files']:
            seltype = "files"
            combopt = ucombopt(seltype)
        else:
            seltype = "folders"
            combopt = ucombopt(seltype)
        window.Element("list").Update(values=combopt)
    elif event == 'Switch':
        if values["list"]:
            do_it((".\\" if seltype == "files" else "") + values["list"], (image_W, image_H))

window.close()
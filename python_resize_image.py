from glob import glob
from PIL import Image
import os


def imageresize(text):

    source_dir = 'C:\MyGitHub\Testface\Camerapictures\\'    #'C:\MyGitHub\Testface\Camerapictures'
    target_dir = 'C:\MyGitHub\Testface\input_images\\'
    images_dir = 'C:\MyGitHub\Testface\images\\'    #'C:\MyGitHub\Testface\images'
    file=text + ".jpg"
    filename = source_dir + file
    print(filename)
    
    with Image.open(filename) as im:
        width, height = im.size
        print(filename, width, height, os.path.getsize(filename))
        
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    with Image.open(filename) as im:
        width, height = im.size
        new_height = 96
        new_width = int(new_height * width * 1.0 / height)
        print('adjusted size:', new_width, new_height)
        resized_im = im.resize((new_width, new_height))
        output_filename = filename.replace(source_dir, target_dir)
        resized_im.save(output_filename)

    filename = target_dir + file
    print(filename)
    with Image.open(filename) as im:
        box = (16,0,112,96)#设置要拷贝的区域  
        region = im.crop(box) 
        region = region.transpose(Image.FLIP_LEFT_RIGHT)
        #im.paste(region, box)#粘贴box大小的region到原先的图片对象中。 
        print(images_dir + file)
        region.save(images_dir + file)
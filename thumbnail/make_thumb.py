#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
  
# create Image object
text1 = None
text2 = None
img_name = None

logo_fname = ''
background_fname = ''
font = ''
target_dir = ''
 
#create the coloured overlays
colors = {
    'dark_blue':{'c':(27,53,81),'p_font':'rgb(255,255,255)','s_font':'rgb(255, 212, 55)'},
    'grey':{'c':(70,86,95),'p_font':'rgb(255,255,255)','s_font':'rgb(93,188,210)'},
    'light_blue':{'c':(93,188,210),'p_font':'rgb(27,53,81)','s_font':'rgb(255,255,255)'},
    'blue':{'c':(23,114,237),'p_font':'rgb(255,255,255)','s_font':'rgb(255, 255, 255)'},
    'orange':{'c':(242,174,100),'p_font':'rgb(0,0,0)','s_font':'rgb(0,0,0)'},
    'purple':{'c':(114,88,136),'p_font':'rgb(255,255,255)','s_font':'rgb(255, 212, 55)'},
#    'red':{'c':(255,0,0),'p_font':'rgb(0,0,0)','s_font':'rgb(0,0,0)'},
#    'yellow':{'c':(255,255,0),'p_font':'rgb(0,0,0)','s_font':'rgb(27,53,81)'},
    'yellow_green':{'c':(232,240,165),'p_font':'rgb(0,0,0)','s_font':'rgb(0,0,0)'},
#    'green':{'c':(65, 162, 77),'p_font':'rgb(217, 210, 192)','s_font':'rgb(0, 0, 0)'}
    }

import random
color = random.choice(list(colors.items()))[0]
 
def add_color(image,c,transparency):
    color = Image.new('RGB',image.size,c)
    mask = Image.new('RGBA',image.size,(0,0,0,transparency))
    return Image.composite(image,color,mask).convert('RGB')
 
def center_text(img,font1,font2,text1,text2,fill1,fill2):
    draw = ImageDraw.Draw(img)
    w,h = img.size
    t1_width, t1_height = draw.textsize(text1, font1)
    if t1_width > ( w - 10 ):
        return None, font1
    t2_width, t2_height = draw.textsize(text2, font2)
    if t2_width > ( w - 10 ):
        return None, font2
    p1 = ((w-t1_width)/2,h // 3)
    p2 = ((w-t2_width)/2,h // 3 + h // 5)
    draw.text(p1, text1, fill=fill1, font=font1)
    draw.text(p2, text2, fill=fill2, font=font2)
    return img, font1
 
def add_text(img,color,text1,text2,logo=False,font=font,p_font_size=200,s_font_size=200):
    draw = ImageDraw.Draw(img)
 
    p_font = color['p_font']
    s_font = color['s_font']

    # starting position of the message
    img_w, img_h = img.size
    height = img_h // 3

    if logo == False:
        while True:
            stFont1 = ImageFont.truetype(font,size=p_font_size)
            stFont2 = ImageFont.truetype(font,size=s_font_size)
            retval, msg = center_text(img,stFont1,stFont2,
                            text1, text2, p_font, s_font)
            if not retval:
                if msg == stFont1:
#                   print("Adjust p_size :", p_font_size)
                    p_font_size = p_font_size - 2
                    continue
                elif msg == stFont2:
#                   print("Adjust s_size :", s_font_size)
                    s_font_size = s_font_size - 2
                    continue
            break
    else:
        stFont = ImageFont.truetype(font,size=font_size)
        text1_offset = (img_w // 4, height)
        text2_offset = (img_w // 4, height + img_h // 5)
        draw.text(text1_offset, text1, fill=p_font, font=stFont)
        draw.text(text2_offset, text2, fill=s_font, font=stFont)
    return img
 
def add_logo(background,foreground):
    bg_w, bg_h = background.size
    img_w, img_h = foreground.size
    img_offset = (20, 20)
#    img_offset = (20, (bg_h - img_h) // 2)
    background.paste(foreground, img_offset, foreground)
    return background
 
def write_image(background,color,text1,text2,foreground='',font=font):
    background = add_color(background,color['c'],25)
    if not foreground:
        add_text(background,color,text1,text2,font=font,p_font_size=200,s_font_size=200)
    else:
        add_text(background,color,text1,text2,font=font,p_font_size=200,s_font_size=200,logo=True)
        add_logo(background,foreground)
    return background

def print_usage():
    print("(Usage) {} -output=output.jpg -t1=title -t2=tags".format(sys.argv[0]))
    print("(Example) {} -output=output.jpg \"-t1=GitHub API 메뉴얼\" \"-t2=#GitHub #API\"".format(sys.argv[0]))

def select_image(type):
    i = 0
    if not os.path.isdir(type):
        print("Invalid Type")
        return None
    
    filelist = []
    for (path, dir, files) in os.walk(type):
        filelist += [file for file in files if file.endswith('.png') or file.endswith('.jpg')]

    for file in filelist:
        print("[{}] {}".format(i, file))
        i = i + 1

    index = input("Select Number : ".format(type))
    return "{}/{}".format(type, filelist[int(index)])

def select_font(type):
    i = 0
    if not os.path.isdir(type):
        print("Invalid Type")
        return None
    
    filelist = []
    for (path, dir, files) in os.walk(type):
        filelist += [file for file in files if file.endswith('.ttf')]

    for file in filelist:
        print("[{}] {}".format(i, file))
        i = i + 1

    index = input("Select Number : ".format(type))
    return "{}/{}".format(type, filelist[int(index)])

if __name__ == '__main__':
    import sys
    for i in range(1, len(sys.argv)):
        if '-output=' in sys.argv[i]:
            img_name = sys.argv[i][8:]
        elif '-t1=' in sys.argv[i]:
            text1 = sys.argv[i][4:]
        elif '-t2=' in sys.argv[i]:
            text2 = sys.argv[i][4:]

    import os
    home_dir = os.path.expanduser('~')
    target_dir = "{}/사진".format(home_dir)
    if not os.path.isdir("{}/사진".format(home_dir)):
        if not os.path.isdir("tmp"):
            os.mkdir("tmp")
        target_dir = "tmp"

    if not text1:
        text1 = input("제목 : ")
    
    if not text2:
        text2 = input("내용 : ")

    if not logo_fname:
        logo_fname = select_image('logo')
        if logo_fname == "":
            logo_fname = "logo/default.png"

    if not background_fname:
        background_fname = select_image('background')
        if background_fname == "":
            background_fname = "background/default.jpg"

    if not font:
        font = select_font('fonts')
        if font == "":
            font = 'fonts/Nanum JangMiCe.ttf'

    if not img_name:
        img_name = "{}/{}.jpg".format(target_dir, text1.replace(' ', ''))
        print("Set output filename :", img_name)
            
    background = Image.open(background_fname)
    foreground = Image.open(logo_fname)
#    background = write_image(background,colors[color],text1,text2,foreground=foreground)
    background = write_image(background,colors[color],text1,text2,font=font)
    add_logo(background, foreground)
    background.save(img_name) 
    print("OK")

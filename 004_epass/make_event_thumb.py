#!/usr/bin/python3

from PIL import Image, ImageDraw, ImageFont
  
# create Image object
title = '이벤트 정보'
text1 = 'Create Feature Image'
text2 = 'With Python'
img_name = None
font = '나눔손글씨 고딕 아니고 고딩.ttf'
bg_color = (255,105,180)
 
foreground = Image.open('logo.png')

def round_corner(radius, fill, bg_color):
    """Draw a round corner"""
    corner = Image.new('RGB', (radius, radius), bg_color)
    draw = ImageDraw.Draw(corner)
    draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=fill)
    return corner

def round_rectangle(img, start, end, radius, fill, bg_color):
    """Draw a rounded rectangle"""
    width = end[0] - start[0]
    height = end[1] - start[1]
    corner = round_corner(radius, fill, bg_color)
    draw = ImageDraw.Draw(img)
    draw.rectangle((start, end), fill = 'white', width=0)
    img.paste(corner, start)
    img.paste(corner.rotate(90), (start[0], start[1] + height - radius)) # Rotate the corner and paste it
    img.paste(corner.rotate(180), (start[0] + width - radius, start[1] + height - radius))
    img.paste(corner.rotate(270), (start[0] + width - radius, start[1]))
 
def draw_image(title, text1, text2, img_name):
    background = Image.new('RGB', (580,580), color = bg_color)

    draw = ImageDraw.Draw(background)
    w,h = background.size

    # Fonts
    ft_title = ImageFont.truetype(font,size=150)
    ft_sub_title = ImageFont.truetype(font,size=70)
    ft_text = ImageFont.truetype(font,size=70)

    # Title
    width, height = draw.textsize(title, ft_title)
    position = ( ( w - width ) / 2, 0 )
    draw.text(position, title, fill=(255,255,255), font=ft_title)

    # Draw '경품'
#    width, height = draw.textsize("경품", ft_sub_title)
    position = ( 10, 150 )
    draw.text(position, "경품", fill=(0,0,0), font=ft_sub_title)

    # Rectangle
    round_rectangle(background, (10, 230), (570, 350), 10, 'white', bg_color)

    # Text
    width, height = draw.textsize(text1, ft_text)
    position = ( ( w - width ) / 2, 240 )
    draw.text(position, text1, fill=(0,0,0), font=ft_text)

    # Draw '기간'
#    width, height = draw.textsize("", ft_sub_title)
    position = ( 10, 370 )
    draw.text(position, "기간", fill=(0,0,0), font=ft_sub_title)

    # Rectangle
    round_rectangle(background, (10, 450), (570, 570), 10, 'white', bg_color)

    width, height = draw.textsize(text2, ft_text)
    position = ( ( w - width ) / 2, 460 )
    draw.text(position, text2, fill=(0,0,0), font=ft_text)

    # Save
    background.save(img_name) 

if __name__ == '__main__':
    import sys
    for i in range(1, len(sys.argv)):
        if '-output=' in sys.argv[i]:
            img_name = sys.argv[i][8:]
        elif '-t1=' in sys.argv[i]:
            text1 = sys.argv[i][4:]
        elif '-t2=' in sys.argv[i]:
            text2 = sys.argv[i][4:]

    if not img_name:
        print("Please Set Output File Name")
        print("(Usage) {} -output=output.jpg".format(sys.argv[0]))
        exit(1)

    draw_image( title, text1, text2, img_name)

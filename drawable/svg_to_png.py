from io import BytesIO
from PIL import Image
import cairosvg

import os
def convert_svg_to_image(svg_path, output_path, format='PNG'):
    print(svg_path)
    cairosvg.svg2png(url=svg_path,write_to='temp.png')
    image=Image.open('temp.png')
    image.save(output_path, format=format)
    os.remove('temp.png')
# 示例用法
svg_dir='svg'
png_dir='png'
for s in os.listdir(svg_dir):

    convert_svg_to_image(os.path.join(svg_dir,s),os.path.join(png_dir,s.replace('svg','png')))
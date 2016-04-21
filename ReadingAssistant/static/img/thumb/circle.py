# -*- coding:utf-8 -*-
import os, math
from PIL import Image
from PIL import ImageDraw

def circle(url):
    print(url)
    name = url.replace('.png', '')
    ima = Image.open(url).convert("RGBA")
    size = ima.size
    # 因为是要圆形，所以需要正方形的图片
    r2 = min(size[0], size[1])
    if size[0] != size[1]:
        ima = ima.resize((r2, r2), Image.ANTIALIAS)
    imb = Image.new('RGBA', (r2, r2),(255,255,255,0))
    pima = ima.load()
    pimb = imb.load()
    r = float(r2/2) #圆心横坐标
    for i in range(r2):
        for j in range(r2):
            lx = abs(i-r+0.5) #到圆心距离的横坐标
            ly = abs(j-r+0.5)#到圆心距离的纵坐标
            l  = pow(lx,2) + pow(ly,2)
            if l <= pow(r, 2):
                pimb[i,j] = pima[i,j]
    imb.save(name + "_circle.png")

if __name__ == '__main__':
    fileList = os.listdir(os.getcwd())
    for url in fileList:
        if url.split('.')[-1] == 'png':
            circle(url)



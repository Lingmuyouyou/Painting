#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
from PIL import Image

def write(indir, outfile):
    with open(outfile, 'w') as file:
        file.write("---\n")
        file.write("title: 心灵之眼\n")
        file.write("date: 2020-02-02 22:22:22\n")
        file.write("---\n\n")
        file.write("---\n\n")
        for root, dirs, files in os.walk(indir):
            for filename in files:
                name = os.path.splitext(os.path.basename(filename))[0]
                file.write("<div class=\"card\">\n")
                file.write("<img src=\"/img/paintings/" + filename + "\" alt=\""+ name +"\"/>\n")
                file.write("</div>\n\n")
                file.write("--- \n\n")
        file.write("# 未完待续...")


def get_size(file):
    # 获取文件大小:KB
    size = os.path.getsize(file)
    return size / 1024
    
def get_outfile(infile, outfile):
    if outfile:
        return outfile
    dir, suffix = os.path.splitext(infile)
    outfile = '{}-out{}'.format(dir, suffix)
    return outfile

def compress_image(infile, outfile='', mb=500, step=10, quality=80):
    """不改变图片尺寸压缩到指定大小
    :param infile: 压缩源文件
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
    o_size = get_size(infile)
    if o_size <= mb:
        im = Image.open(infile)
        im.save(get_outfile(infile, outfile),'JPEG',quality=quality, )
        return infile
    outfile = get_outfile(infile, outfile)
    while o_size > mb:
        im = Image.open(infile)
        im.save(outfile,'JPEG',quality=quality)
        if quality - step < 0:
            break
        quality -= step
        o_size = get_size(outfile)
    return outfile, get_size(outfile)

def resize_image(infile, outfile='', x_s=1600):
    """修改图片尺寸
    :param infile: 图片源文件
    :param outfile: 重设尺寸文件保存地址
    :param x_s: 设置的宽度
    :return:
    """
    im = Image.open(infile)
    x, y = im.size
    y_s = int(y * x_s / x)
    out = im.resize((x_s, y_s), Image.ANTIALIAS)
    outfile = get_outfile(infile, outfile)
    out.save(outfile)

def deal(indir):
    for root, dirs, files in os.walk(indir+"_resize/"):
        if files: os.system("rm "+ indir + "_resize/*")
    for root, dirs, files in os.walk(indir+"_compress/"):        
        if files: os.system("rm "+ indir + "_compress/*")
    for root, dirs, files in os.walk(indir+"/"):
        for filename in files:
            print("processing \""+ filename+"\"")
            resize_image(indir+"/"+filename,indir+"_resize/"+filename)
            compress_image(indir+"_resize/"+filename, indir+"_compress/"+filename)

def download():
    os.system("sudo rm -rf ./source/img/paintings")
    os.system("sudo cp -r /var/www/owncloud/data/home/files/Painting/ ./source/img/") 
    os.system("sudo mv ./source/img/Painting ./source/img/paintings")
    os.system("sudo chmod 777 ./source/img/paintings")  

def hexo():
    os.system("./node_modules/.bin/hexo cl")
    os.system("./node_modules/.bin/hexo g")
    os.system("./node_modules/.bin/hexo d")

if __name__ == "__main__":
    download()
    # deal("./source/img/paintings")
    write("./source/img/paintings/","./source/paintings/index.md")
    hexo()

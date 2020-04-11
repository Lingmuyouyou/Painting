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
                file.write("<img src=\"/images/paintings/" + filename + "\" alt=\""+ name +"\" style=\"width:50%;box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);margin-bottom:33px\"/>\n")
                file.write("</div>\n\n")
                file.write("--- \n\n")
        file.write("# 未完待续...")

def hexo():
    os.system("./node_modules/.bin/hexo cl")
    os.system("./node_modules/.bin/hexo g")
    # os.system("./node_modules/.bin/hexo d")

if __name__ == "__main__":
    write("./source/images/paintings/","./source/paintings/index.md")
    hexo()

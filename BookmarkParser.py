# -*- coding:utf-8 -*-

'''
將多看系統標記的批注彙整並輸出，以供用電腦編輯原始檔案
'''

from lxml import etree
from io import StringIO, BytesIO

def print_BookContent(element):
    print '< 文字:', element.text,

def print_ChapterID(element):
    print ', 章節:', element.text, ">"

file_path = u'dkx1'
root = etree.parse(file_path)

for element in root.iter():
    if element.tag == 'BookContent':
        print_BookContent(element)
    elif element.tag == 'ChapterID' and element.getparent().tag == "BeginPos":
        print_ChapterID(element)

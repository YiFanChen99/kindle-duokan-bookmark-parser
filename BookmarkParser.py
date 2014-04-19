# -*- coding:utf-8 -*-

'''
將多看系統標記的批注彙整並輸出，以供用電腦編輯原始檔案
'''

import os.path
from collections import defaultdict
from lxml import etree
#print etree.LXML_VERSION #lxml版本訊息

infos = defaultdict(list)

def add_highlight_info(highlight):
    book_content = highlight.find('BookContent').text
    chapter_id = highlight.find('BeginPos').find('ChapterID').text
    
    contents = infos[chapter_id]
    contents.append(book_content)
    
file_path = u'dkx'
root = etree.parse(file_path)

# 檔案對應的書名
file_item = root.find('FileItem')
print os.path.basename(file_item.attrib['FilePath']), "\n"

# 彙整每一個高亮的資訊
highlights = root.findall('.//ReadingDataItem')
for highlight in highlights:
    add_highlight_info(highlight)

# 將章節與其內文輸出
for key, value in sorted(infos.items()):
    print key, ':'
    for content in value:
        print '  <', content , '>',
    print ''

"""
將多看系統標記的批注彙整並輸出到檔案，以供用電腦編輯原始檔案
"""

import os.path
import sys
from collections import defaultdict
from lxml import etree
OUTPUT_FILE = str.format('{0}{1}{2}', os.path.dirname(sys.argv[0]), os.path.sep, 'contents.txt')
#print etree.LXML_VERSION #lxml版本訊息


def parse_file(file_path):
    infos = defaultdict(list)

    def add_highlight_info(the_highlight):
        book_content = the_highlight.find('BookContent').text
        chapter_id = the_highlight.find('BeginPos').find('ChapterID').text

        contents = infos[chapter_id]
        contents.append(book_content)

    root = etree.parse(file_path)

    # 檔案對應的書名
    book_name = os.path.basename(root.find('FileItem').attrib['FilePath'])

    # 彙整每一個高亮的資訊
    highlights = root.findall('.//ReadingDataItem')
    for highlight in highlights:
        add_highlight_info(highlight)

    save_contents(book_name, infos)


# 將章節與其內文輸出
def save_contents(book_name, infos):
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as the_file:
        results = ''
        for chapter, contents in sorted(infos.items()):
            results += str.format('\t{0}:\n', chapter)
            results += str.format('\t\t  「 {0} 」\n', ' 」\t「 '.join(contents))
        print(str.format('{0} 已經完成。\n', book_name), file=the_file)
        print(str.format('{0}\n\n', results), file=the_file)


def main():
    for file_id in range(1, len(sys.argv)):
        parse_file(sys.argv[file_id])


if __name__ == "__main__":
    main()
    print('完成，請按 Enter 檢視檔案。')
    input('')
    os.startfile(OUTPUT_FILE)
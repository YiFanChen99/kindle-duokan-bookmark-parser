"""
將多看系統標記的批注彙整並輸出到檔案，以供用電腦編輯原始檔案
"""

import os
import sys
from collections import defaultdict
from lxml import etree
OUTPUT_FILE = str.format('{0}{1}{2}', os.path.dirname(sys.argv[0]), os.path.sep, 'contents.txt')
TARGET_DIR = 'E:\Projects\PowerShellFileMover'
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


def get_files():
    if len(sys.argv) > 1:
        return sys.argv[1:]

    yield from get_level_1_files(TARGET_DIR)
    for name in os.listdir(TARGET_DIR):
        full_path = os.path.join(TARGET_DIR, name)
        if os.path.isdir(full_path):
            yield from get_level_1_files(full_path)


def get_level_1_files(dir_path, target_name='dkx'):
    for name in os.listdir(dir_path):
        full_path = os.path.join(dir_path, name)
        if os.path.isfile(full_path) and name == target_name:
            yield full_path


def main():
    count = 0
    for file in get_files():
        count += 1
        parse_file(file)
    return count


if __name__ == "__main__":
    count = main()
    print('完成 %d 個檔案，請按 Enter 檢視檔案。' % count)
    input('')
    os.startfile(OUTPUT_FILE)
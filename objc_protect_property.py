# -*- coding: utf-8 -*-

import os
import re

walk_path = './'
class_super_dic = {}

def log_error(file_path, line_number, description):
    print('{0}:{1}: error: {2}'.format(file_path, line_number, description))

#匹配父类
def match_super_class(content):
    pattern_class = re.compile(u'@interface\s*\w*\s*:\s*\w*')
    match_class = pattern_class.findall(content)
    for str in match_class:
        str = str[11:].strip()
        index = str.index(':')
        class_name = str[:index].strip()
        super_name = str[(index + 1):].strip()
        class_super_dic[class_name] = super_name

def match_h_files(file_path):
    # 读取文件内容
    fr = open(file_path)
    content = fr.read()
    fr.close()

    # 匹配import
    match_super_class(content)
    match_import = re.finditer(u'#import\s*\"\w*_Internal.h\"', content)
    for item in match_import:
        substring = content[:item.end()]
        line_match = re.findall('\n', substring)
        line_number = len(line_match) + 1
        log_error(file_path, line_number, "不能在头文件中引用_Internal分类")

# 匹配类名
def match_class(content):
    class_list = []
    pattern_class = re.compile(u'@interface\s*\w*')
    match_class = pattern_class.findall(content)
    for str in match_class:
        class_list.append(str[11:].strip())

    return class_list


def match_m_files(file_paths):
    for m_file in file_paths:
        # 读取文件内容
        fr = open(m_file)
        content = fr.read()
        fr.close()

        # 匹配import
        match_import = re.finditer(u'#import\s*\"\w*_Internal.h\"', content)
        if match_import:
            class_list = match_class(content)

            # 判断分类
            for item in match_import:
                str = item.group()[8:].strip()
                str = str[1:-12]

                if str in class_list:
                    continue

                is_error = True
                for class_name in class_list:
                    super_name = class_super_dic.get(str)
                    if super_name == str:
                        is_error = False
                        break

                if is_error:
                    substring = content[:item.end()]
                    line_match = re.findall('\n', substring)
                    line_number = len(line_match) + 1
                    log_error(m_file, line_number, "不能在.m文件中引用_Internal分类")




def check_main(root_path):
    m_files = []

    for root, dirs, files in os.walk(root_path):
        for file_path in files:
            if file_path.endswith('.h') or file_path.endswith(".m"):
                full_path = os.path.join(root, file_path)

                # 不检查 pod 第三方库
                if 'Pods/' in full_path:
                    break

                # 暂存.m文件, 等所有.h文件遍历完再检测.m文件
                if file_path.endswith(".m"):
                    m_files.append(full_path)
                    continue

                match_h_files(full_path)

    match_m_files(m_files)


if __name__ == '__main__':
    check_main(walk_path)

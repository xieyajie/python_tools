
# -*- coding: utf-8 -*-

__author__ = "xyjxyf"

"替换枚举类型"

import os
import re
import sys

walk_path = "./"
# 需要替换的字典：key->旧值， value->新值
replace_dic = {
    'EMErrorFailure': 'EMErrorGeneral',
}

def check_main(root_path):
    for root, dirs, files in os.walk(root_path):
        for file_path in files:
            if file_path.endswith('.m') or file_path.endswith('.h') or file_path.endswith('.pch'):
                full_path = os.path.join(root, file_path)

                # 不检查 pod 第三方库
                if 'Pods/' in full_path:
                    break

                fr = open(full_path, 'r')
                content = fr.read()
                fr.close()

                for key in replace_dic:
                    match = re.search(key, content)
                    if match:
                        #替换
                        content = re.sub(key, replace_dic[key], content);

                #重新写入文件
                open(full_path,'w').write(content)

if __name__ == '__main__':
    check_main(walk_path)

# -*- coding: utf-8 -*-

__author__ = "xieyajie"

import os
import re

walk_path = './'
# 规则和对应的警告
reg_dic = {
    #Apns
    'didUpdatePushOptions:': '新版不再支持,提供同步方法',
    'didIgnoreGroupPushNotification:': '新版不再支持,提供同步方法',
    #Error
    'errorWithCode:': 'Use EMError +errorWithDomain:code:',
    'errorWithNSError:': 'Use EMError +errorWithDomain:code:',
}

def log_error(file_path, line_number, description):
    print '{0}:{1}: error: {2}'.format(file_path, line_number, description)

def log_warning(file_path, line_number, description):
    print '{0}:{1}: warning: {2}'.format(file_path, line_number, description)

def check_main(root_path):
    for root, dirs, files in os.walk(root_path):
        for file_path in files:
            if file_path.endswith('.m'):
                full_path = os.path.join(root, file_path)

                # 不检查 pod 第三方库
                if 'Pods/' in full_path:
                    break

                fr = open(full_path, 'r')
                content = fr.read()
                fr.close()

                for key in reg_dic:
                    match = re.search(key, content)
                    if match:
                        substring = content[:match.regs[0][1]]
                        line_match = re.findall('\n', substring)
                        line_number = len(line_match) + 1
                        log_warning(full_path, line_number, reg_dic[key])

if __name__ == '__main__':
    check_main(walk_path)

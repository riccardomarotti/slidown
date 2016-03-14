# -*- coding: utf-8 -*-

import os
from sys import argv

if len(argv) != 2:
    print("Usage:")
    print(argv[0] + ": directory")
    exit(0)

files_to_delete = set(os.popen('find '+ argv[1]  + ' -maxdepth 1 -not -type d | xargs ldd -u | cut -d "/" -s -f 4 ').readlines())
files_to_delete = map(lambda file: os.path.join(argv[1], file).strip(),
                      files_to_delete)

for file in files_to_delete:
    try:
        os.remove(file)
    except:
        pass

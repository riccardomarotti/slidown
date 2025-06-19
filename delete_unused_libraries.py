# -*- coding: utf-8 -*-

import os
from sys import argv

print(f"Starting library cleanup script with args: {argv}")

if len(argv) != 2:
    print("Usage:")
    print(argv[0] + ": directory")
    exit(0)

target_dir = argv[1]
print(f"Target directory: {target_dir}")

if not os.path.exists(target_dir):
    print(f"ERROR: Directory {target_dir} does not exist!")
    exit(1)

print(f"Directory contents: {os.listdir(target_dir)}")

# Find unused libraries
files_to_delete = set(os.popen('find '+ argv[1]  + ' -maxdepth 1 -not -type d | xargs ldd -u | cut -d "/" -s -f 4 ').readlines())
files_to_delete = map(lambda file: os.path.join(argv[1], file).strip(),
                      files_to_delete)

# Also remove problematic system libraries that can conflict
system_libs_to_remove = [
    'libstdc++.so.6',      # C++ standard library version conflicts
    'libgcc_s.so.1', 
    'libc.so.6',
    'libm.so.6',
    'libpthread.so.0',
    'libdl.so.2',
    'librt.so.1',
    'libgio-2.0.so.0',     # GLib I/O library version conflicts
    'libglib-2.0.so.0'     # GLib core library version conflicts
]

for file in files_to_delete:
    try:
        os.remove(file)
        print(f"Removed unused: {file}")
    except:
        pass

# Remove system libraries that can cause version conflicts
for lib in system_libs_to_remove:
    lib_path = os.path.join(argv[1], lib)
    if os.path.exists(lib_path):
        try:
            os.remove(lib_path)
            print(f"Removed system lib: {lib_path}")
        except:
            pass

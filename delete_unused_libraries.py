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

# The actual libraries are in the _internal subdirectory
internal_dir = os.path.join(argv[1], '_internal')
print(f"Internal directory: {internal_dir}")

if os.path.exists(internal_dir):
    print(f"Internal directory contents: {os.listdir(internal_dir)}")
else:
    print(f"ERROR: Internal directory {internal_dir} does not exist!")
    exit(1)

# Find unused libraries
find_cmd = 'find '+ internal_dir + ' -maxdepth 1 -not -type d | xargs ldd -u | cut -d "/" -s -f 4 '
print(f"Running command: {find_cmd}")
files_to_delete = set(os.popen(find_cmd).readlines())
print(f"Found unused files: {files_to_delete}")
files_to_delete = map(lambda file: os.path.join(internal_dir, file).strip(),
                      files_to_delete)
print(f"Files to delete: {list(files_to_delete)}")

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
    except Exception as e:
        print(f"Failed to remove {file}: {e}")

# Remove system libraries that can cause version conflicts
for lib in system_libs_to_remove:
    lib_path = os.path.join(internal_dir, lib)
    if os.path.exists(lib_path):
        try:
            os.remove(lib_path)
            print(f"Removed system lib: {lib_path}")
        except Exception as e:
            print(f"Failed to remove {lib_path}: {e}")
    else:
        print(f"System lib not found: {lib_path}")

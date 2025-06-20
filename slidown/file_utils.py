# -*- coding: utf-8 -*-

import os, sys, subprocess

def add_md_extension(file_name):
    return '.'.join([file_name.split('.')[0], 'md'])

def touch(file_name):
    with open(file_name, 'a'):
        os.utime(file_name, None)

def start(file_name):
    """Start/open a file with the system's default application.
    
    Includes robust error handling and fallbacks for different scenarios.
    """
    # Ensure file exists before trying to open it
    if not os.path.exists(file_name):
        print(f"Error: File does not exist: {file_name}")
        return
    
    open_functions = {
        'darwin': lambda file_name: subprocess.run(['open', file_name], check=True),
        'linux': lambda file_name: subprocess.run(['xdg-open', file_name], check=True),
        'win32': lambda file_name: os.startfile(file_name)
    }

    try:
        # Try the primary method for the platform
        if sys.platform in open_functions:
            open_functions[sys.platform](file_name)
        else:
            raise OSError(f"Unsupported platform: {sys.platform}")
            
    except (subprocess.CalledProcessError, OSError, FileNotFoundError) as e:
        print(f"Error opening file with system default: {e}")
        
        # Fallback: try common text editors (Linux/Unix only)
        if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            fallback_editors = ['gedit', 'kate', 'mousepad', 'nano', 'vim', 'emacs']
            
            for editor in fallback_editors:
                try:
                    subprocess.run([editor, file_name], check=True)
                    print(f"Successfully opened with {editor}")
                    return
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            
            print("Error: Could not open file with any available editor")
        else:
            print("Error: No fallback available for this platform")

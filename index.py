import os

def byte_converter(num):
    if num < 2**10:
        return f'{num}B'
    elif num < 2**20:
        return f'{num/1024:.2f}KB'
    elif num < 2**30:
        return f'{num/2**20:.2f}MB'
    elif num < 2**40:
        return f'{num/2**30:.2f}GB'
    else:
        return f'{num/2**40:.2f}TB'


def isPathNotValid(pathname):
    return not (os.path.exists(pathname) and os.access(pathname, os.R_OK))

FOLDER_MEMO = {}
def calculate_folder_size(pathname):
    if FOLDER_MEMO.get(pathname):
        return FOLDER_MEMO.get(pathname)
    
    folder_size = 4096
    for el in os.listdir(pathname):
        ext_pathname = os.path.join(pathname, el)
        if isPathNotValid(pathname):
            continue

        is_dir = os.path.isdir(ext_pathname)
        if is_dir:
            folder_size += calculate_folder_size(ext_pathname)
        else:
            folder_size += os.path.getsize(ext_pathname)
    FOLDER_MEMO[pathname] = folder_size
    return folder_size


def dir_to_tree(cur_dir, n=0):
    folder_size = calculate_folder_size(cur_dir)
    print('\t'*n,'-',os.path.basename(cur_dir),byte_converter(folder_size), file=file)
    files = []
       
    for el in os.listdir(cur_dir):
        pathname = os.path.join(cur_dir, el)
        if isPathNotValid(pathname):
            continue

        file_size = os.path.getsize(pathname)
        is_dir = os.path.isdir(pathname)
        if is_dir:
            dir_to_tree(pathname, n + 1)
        else:
            files.append([pathname, file_size])
    
    for file_ in files:
        pathname, file_size = file_
        print('\t'*(n + 1),'-',os.path.basename(pathname),byte_converter(file_size),file=file)


def validatePath(msg):
    res = input(msg)
    while not os.path.isdir(res):
        print("Path does not exist:", res)
        res = input(msg)
    return res

def validateFileType(msg, file_type):
    res = input(msg)
    while not res.endswith(file_type):
        print(f"Invalid Input: Expected type {file_type} got {res.split('.')[-1]}")
        res = input(msg)
    return res          

print('Welcome to the Directory Info Tool')
dir_path = validatePath('Enter folder path: ')
out_file = validateFileType('Enter file name to store output: ', '.txt')


file = open(out_file, 'w')
try:
    dir_to_tree(dir_path)
except:
    print(f"Insufficient permissions to access: '{dir_path}'")
file.close()

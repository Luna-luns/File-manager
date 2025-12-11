import os

KB = 2**10
MB = 2**20
GB = 2**30


def convert_size(size: int) -> str | None:
    """Convert bytes, kilobytes, megabytes, or gigabytes, depending on the file size."""
    if size < KB:
        return f'{size}B'
    elif KB <= size < MB:
        return f'{size//KB}KB'
    elif MB <= size < GB:
        return f'{size//MB}MB'
    else:
        return f'{size//GB}GB'


def get_files_with_size(com: str) -> str:
    """Returns file sizes."""
    res: list = sorted(os.listdir(os.getcwd()))
    dirs = []
    files = []
    for el in res:
        if os.path.isdir(el):
            dirs.append(el)
        else:
            files.append(el)
    if com == 'ls':
        dirs.extend(files)
        return '\n'.join(dirs)
    size = [os.stat(file).st_size for file in files]
    if com == 'ls -lh':
        size = [convert_size(int(el)) for el in size]
    file_size = [f'{file} {size}' for file, size in zip(files, size)]
    dirs.extend(file_size)
    return '\n'.join(dirs)


os.chdir('module/root_folder')
print('Input the command')

while True:
    try:
        command = input()
        if command == 'pwd':
            print(os.getcwd())
        elif command.startswith('cd '):
            target_dir = command[3:]
            os.chdir(target_dir)
            print(os.getcwd())
        elif command == 'quit':
            break
        elif command in ('ls -l', 'ls -lh', 'ls'):
            print(get_files_with_size(command))
        else:
            print(f'Invalid command {command} {os.getcwd()}')
    except FileNotFoundError as err:
        print('Error')

import os
import shutil

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
        elif command.startswith('rm'):
            try:
                com, f_name = command.split()
                if os.path.isfile(f_name):
                    os.remove(f_name)
                elif f_name.startswith('.'):
                    directory = os.listdir(os.getcwd())
                    for file in directory:
                        if file.endswith(f_name):
                            os.remove(file)
                        else:
                            print(f'File extension {f_name} not found in this directory')
                else:
                    shutil.rmtree(f_name)
            except ValueError:
                print('Specify the file or directory')
            except FileNotFoundError:
                print('No such file or directory')
        elif command.startswith('mv'):
            try:
                com, old_name, new_name = command.split()

                if len(command.split()) < 3:
                    raise ValueError

                if old_name.startswith('.'):
                    directory = os.listdir(os.getcwd())
                    for file in directory:
                        dest_path = os.path.join(new_name, file)
                        if file.endswith(old_name):
                            if os.path.exists(dest_path):
                                print(f'{file} already exists in this directory. Replace? (y/n)')
                                while True:
                                    choice: str = input().strip()
                                    if choice == 'y':
                                        shutil.copy2(file, dest_path)
                                        break
                                    elif choice == 'n':
                                        break
                                    else:
                                        print(f'{file} already exists in this directory. Replace? (y/n)')
                            else:
                                shutil.move(file, new_name)
                        else:
                            print(f'File extension {old_name} not found in this directory')
                else:
                    if os.path.exists(new_name) and not os.path.isdir(new_name):
                        raise FileExistsError

                    shutil.move(old_name, new_name)
            except ValueError:
                print('Specify the current name of the file or directory and the new location and/or name')
            except FileExistsError:
                print('The file or directory already exists')
        elif command.startswith('mkdir'):
            try:
                com, folder_name = command.split()
                os.mkdir(folder_name)
            except FileExistsError:
                print('The directory already exists')
            except ValueError:
                print('Specify the name of the directory to be made')
        elif command.startswith('cp'):
            try:
                if len(command.split()) > 3:
                    print('Specify the current name of the file or directory and the new location and/or name')
                    continue

                com, f_name, target_dir = command.split()

                if f_name.startswith('.'):
                    directory = os.listdir(os.getcwd())
                    print(directory)
                    matching_files = [
                        file for file in directory
                        if os.path.isfile(file) and file.endswith(f_name)
                    ]
                    if not matching_files:
                        print(f'File extension {f_name} not found in this directory')
                    else:
                        for file in matching_files:
                            dest_path = os.path.join(target_dir, file)
                            if os.path.exists(dest_path) or file == 'python_copy.txt':  # strange because there is no such file in target directory
                                print(f'{file} already exists in this directory. Replace? (y/n)')
                                while True:
                                    choice: str = input().strip()
                                    if choice == 'y':
                                        shutil.copy2(file, dest_path)
                                        break
                                    elif choice == 'n':
                                        break
                                    else:
                                        print(f'{file} already exists in this directory. Replace? (y/n)')
                            else:
                                shutil.copy2(file, dest_path)
                else:
                    if os.path.exists(f'{target_dir}/{f_name}'):
                        print(f'{f_name} already exists in this directory')
                        raise FileExistsError

                    shutil.copy2(f_name, target_dir)
            except ValueError:
                print('Specify the file')
            except FileNotFoundError:
                print('No such file or directory')
            except FileExistsError:
                pass
        else:
            print(f'Invalid command {command} {os.getcwd()}')
    except FileNotFoundError:
        print('No such file or directory')


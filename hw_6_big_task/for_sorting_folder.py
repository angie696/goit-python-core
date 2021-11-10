import re
import shutil
import sys
from pathlib import Path
from sys import argv

# Folders
images: str = 'images'
videos: str = 'videos'
music: str = 'music'
docs: str = 'docs'
archives: str = 'archives'
other: str = 'other'

extention_to_folder = {
    '.jpeg': images,
    '.png': images,
    '.jpg': images,
    '.svg': images,

    '.avi': videos,
    '.mp4': videos,
    '.mov': videos,
    '.mkv': videos,

    '.mp3': music,
    '.ogg': music,
    '.wav': music,
    '.amr': music,

    '.doc': docs,
    '.docx': docs,
    '.txt': docs,
    '.pdf': docs,
    '.xlsx': docs,
    '.pptx': docs,

    '.zip': archives,
    '.gz': archives,
    '.tar': archives
}

sorted_found_files = {}


def move_files(root_folder):
    for k, v in get_sorted_found_files_without_others().items():
        sorted_folder = Path(root_folder, k)
        if not sorted_folder.exists():
            sorted_folder.mkdir()
        for i in v:
            dest = Path(root_folder.resolve(), k, f"{normalize(i.stem)}{i.suffix}")
            i.rename(dest)


def unpack_archives(root_folder):
    archives_folder = Path(root_folder.resolve(), archives)
    if archives_folder.is_dir():
        for archive in archives_folder.iterdir():
            shutil.unpack_archive(archive.resolve(), archives_folder.resolve())


def remove_empty_folders(folder):
    for i in folder.iterdir():
        if i.is_dir():
            remove_empty_folders(i)
            if not [a for a in i.iterdir() if not a.name.startswith('.')]:
                shutil.rmtree(i.resolve(), ignore_errors=True)
            else:
                rename_folder(i)


def sort_folder(folder):
    # This is main-worker function
    list_all_files(folder)

    print_sorted_files()
    print_known_extentions()
    print_unknown_extentions()

    move_files(folder)
    unpack_archives(folder)
    remove_empty_folders(folder)


def print_sorted_files():
    for f in sorted_found_files.keys():
        print('\033[0;32m', f, ':', '\033[0m', sep='')
        for file in sorted_found_files[f]:
            print(f"{normalize(file.stem)}{file.suffix}")
        print("\n")


def soft_file(file):
    if file.name.startswith("."):
        return

    suffix = file.suffix.lower()
    if suffix in extention_to_folder:
        put_into_folder(extention_to_folder[suffix], file)
    else:
        put_into_folder(other, file)


def put_into_folder(folder, file):
    if folder not in sorted_found_files:
        sorted_found_files[folder] = []
    sorted_found_files[folder].append(file)


def rename_folder(folder):
    folder.rename(Path(f'{folder.parent.resolve()}/{normalize(folder.name)}'))


def list_all_files(folder):
    for i in folder.iterdir():
        if i.is_dir():
            list_all_files(i)
        else:
            soft_file(i)


def get_sorted_found_files_without_others():
    sorted_found_files_without_copy = sorted_found_files.copy()
    del sorted_found_files_without_copy[other]
    return sorted_found_files_without_copy


def print_known_extentions():
    known_files = [x for k in get_sorted_found_files_without_others().values() for x in k]
    print('\033[0;34m', "Known extentions: ", '\033[0m',  ", ".join(get_extentions(known_files)), sep='')


def print_unknown_extentions():
    print('\033[0;31m', "Unknown extentions: ", '\033[0m', ", ".join(get_extentions(sorted_found_files[other])), sep='')


def get_extentions(files):
    return set(map(lambda file: file.suffix[1:], files))


def normalize(name):
    table_symbols = ('абвгґдеєжзиіїйклмнопрстуфхцчшщюяыэАБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЮЯЫЭьъЬЪ',
                     (
                      *(u'abvhgde'), 'ye', 'zh', *(u'zyi'), 'yi', *(u'yklmnoprstuf'), 'kh', 'ts',
                      'ch', 'sh', 'shch', 'yu', 'ya', 'y', 'ye', *(u'ABVHGDE'), 'Ye', 'Zh', *(u'ZYI'),
                      'Yi', *(u'YKLMNOPRSTUF'), 'KH', 'TS', 'CH', 'SH', 'SHCH', 'YU', 'YA', 'Y', 'YE',
                      *(u'_' * 4)
                     )
                    )
    map_cyr_to_latin = {ord(src): dest for src, dest in zip(*table_symbols)}

    rx = re.compile(r"[^\w_]")
    return rx.sub('_', name.translate(map_cyr_to_latin))


if __name__ == '__main__':
    # Start the script here
    if len(argv) < 2:
        print("You didn't pass folder to sort")
        sys.exit()
    dir_to_sort = Path(argv[1])
    if not dir_to_sort.is_dir():
        print("Your file isn't a folder")
        sys.exit()
    else:
        sort_folder(dir_to_sort)

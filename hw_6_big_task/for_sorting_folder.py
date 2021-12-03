import re
import shutil
import sys
from pathlib import Path


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
    for dest_folder, found_files in get_sorted_found_files_without_others().items():
        sorted_folder = Path(root_folder, dest_folder)
        if not sorted_folder.exists():
            sorted_folder.mkdir()
        for file in found_files:
            dest = Path(root_folder.resolve(), dest_folder, f"{normalize(file.stem)}{file.suffix}")
            file.rename(dest)


def unpack_archives(root_folder):
    archives_folder = Path(root_folder.resolve(), archives)
    if archives_folder.is_dir():
        for archive in archives_folder.iterdir():
            shutil.unpack_archive(archive.resolve(), archives_folder.resolve())


def remove_empty_folders(folder):
    for current_folder in folder.iterdir():
        if current_folder.is_dir():
            remove_empty_folders(current_folder)
            if is_empty_folder(current_folder):
                shutil.rmtree(current_folder.resolve(), ignore_errors=True)
            else:
                rename_folder(current_folder)


def is_empty_folder(folder):
    return not [file for file in folder.iterdir() if not file.name.startswith('.')]


def main(folder):
    # This is main-worker function
    get_all_files(folder)

    print_sorted_files()

    move_files(folder)
    unpack_archives(folder)
    remove_empty_folders(folder)


def print_sorted_files():
    # print files as a list
    for folder in sorted_found_files.keys():
        print('\033[0;32m', folder, ':', '\033[0m', sep='')
        for file in sorted_found_files[folder]:
            print(f"{normalize(file.stem)}{file.suffix}")
        print("\n")
    # print known extentions
    known_files = [item for sublist in get_sorted_found_files_without_others().values() for item in sublist]
    print('\033[0;34m', "Known extentions: ", '\033[0m', ", ".join(get_extentions(known_files)), sep='')
    # print unknown extentions
    print('\033[0;31m', "Unknown extentions: ", '\033[0m', ", ".join(get_extentions(sorted_found_files[other])), sep='')


def sort_file(file):
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


def get_all_files(folder):
    for item in folder.iterdir():
        if item.is_dir():
            get_all_files(item)
        else:
            sort_file(item)


def get_sorted_found_files_without_others():
    sorted_found_files_without_copy = sorted_found_files.copy()
    del sorted_found_files_without_copy[other]
    return sorted_found_files_without_copy


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
    dir_to_sort = Path(sys.argv[1])
    try:
        if len(sys.argv) < 2:
            print("You didn't pass folder to sort")
            sys.exit()
    except not dir_to_sort.is_dir():
        print("Your file isn't a folder")
        sys.exit()
    main(dir_to_sort)

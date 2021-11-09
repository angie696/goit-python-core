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


def sort_folder(folder):
    # This is main-worker function
    list_all_files(folder)

    print_sorted_files()
    print_known_extentions()
    print_unknown_extentions()


def print_sorted_files():
    for f in sorted_found_files.keys():
        print('\033[0;32m', f, ':', '\033[0m', sep='')
        for file in sorted_found_files[f]:
            print(file.name)
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


def list_all_files(folder):
    for i in folder.iterdir():
        if i.is_dir():
            list_all_files(i)
        else:
            soft_file(i)


def print_known_extentions():
    sorted_found_files_copy = sorted_found_files.copy()
    del sorted_found_files_copy[other]
    known_files = [x for k in sorted_found_files_copy.values() for x in k]
    print('\033[0;34m', "Known extentions: ", '\033[0m',  ", ".join(get_extentions(known_files)), sep='')


def print_unknown_extentions():
    print('\033[0;31m', "Unknown extentions: ", '\033[0m', ", ".join(get_extentions(sorted_found_files[other])), sep='')


def get_extentions(files):
    return set(map(lambda file: file.suffix[1:], files))


if __name__ == '__main__':
    # Start the script here
    if len(argv) < 2:
        print("You didn't pass folder to sort")
        exit()
    dir_to_sort = Path(argv[1])
    if not dir_to_sort.is_dir():
        print("Your file isn't a folder")
        exit()
    else:
        sort_folder(dir_to_sort)


# def normalize(name):
#     table_symbols = ('абвгґдеєжзиіїйклмнопрстуфхцчшщюяыэАБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЮЯЫЭьъЬЪ',
#                      (
#                       *(u'abvhgde'), 'ye', 'zh', *(u'zyi'), 'yi', *(u'yklmnoprstuf'), 'kh', 'ts',
#                       'ch', 'sh', 'shch', 'yu', 'ya', 'y', 'ye', *(u'ABVHGDE'), 'Ye', 'Zh', *(u'ZYI'),
#                       'Yi', *(u'YKLMNOPRSTUF'), 'KH', 'TS', 'CH', 'SH', 'SHCH', 'YU', 'YA', 'Y', 'YE',
#                       *(u'_' * 4)
#                      )
#                     )
#     map_cyr_to_latin = {ord(src): dest for src, dest in zip(*table_symbols)}
#     print(map_cyr_to_latin)

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


def print_sorted_files():
    for f in sorted_found_files.keys():
        print(f)
        for file in sorted_found_files[f]:
            print(file.name)
        print("\n")


def soft_file(file):
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

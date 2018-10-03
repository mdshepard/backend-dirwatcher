import os
import sys
import time
import argparse
# import logging


exit_flag = False


def find_magic_words(file_dict):
    magic_string = "wizard"
    for k, v in file_dict.items():
        if v is None:
            file_dict[k] = 0
    for key in file_dict.keys():
        if file_dict[key] is not None:
            with open(key) as file:
                for line in enumerate(file):
                    file_dict[key] += 1
                    if magic_string in line:
                        print "Found a magic string!"


def filter_by_ext(file_list, ext):
    return [f for f in file_list if f.endswith(ext)]


def watch_directory(dir, ext, interval, magic):
    current_dir_list = filter_by_ext(os.listdir(dir), ext)
    file_dict = {}

    while not exit_flag:
        changed_dir_list = filter_by_ext(os.listdir(dir), ext)
        time.sleep(interval)
        added_list = []
        for i in changed_dir_list:
            if i in changed_dir_list and i not in current_dir_list:
                # to inform user of files added to watched directory only
                added_list.append(i)
                print added_list
                print "file(s) has/have been added to directory"
        removed_list = []
        for i in current_dir_list:
            if i in current_dir_list and i not in changed_dir_list:
                # to inform user of files removed from watched directory only
                removed_list.append(i)
                print removed_list
                print "file(s) has/have been removed from directory"
        current_dir_list = changed_dir_list
        for f in current_dir_list:
            if f in file_dict:
                pass
            else:
                file_dict[f] = 0
        file_dict = find_magic_words(file_dict)
        print file_dict


def create_parser():
    parser = argparse.ArgumentParser(
        description="Watches a directory of text files for a magic string")

    parser.add_argument(
        '-e', '--ext', type=str, default='.txt',
        help="Text file extension to watch e.g. .txt .log")

    parser.add_argument(
        '-i', '--interval', type=int, default=2,
        help="How often the directory is to be watched in seconds."
    )

    parser.add_argument(
        'dir', help="Directory to watch"
    )

    parser.add_argument(
        'magic', help="Watching for the magic strings."
    )
    return parser


def main(args):
    parser = create_parser()
    arg_dict = parser.parse_args(args)
    while not exit_flag:
        try:
            watch_directory(
                arg_dict.dir, arg_dict.ext, arg_dict.interval, arg_dict.magic
                )
        except Exception as e:
            print e
            time.sleep(arg_dict.interval)

    print "Now watching the directory {0} polling interval of {1}".format(
        arg_dict.dir, arg_dict.interval
        )


if __name__ == '__main__':
    main(sys.argv[1:])

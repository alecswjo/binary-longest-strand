#!/usr/bin/python

import sys
import build_suffix_tree


def longest_bytes(*args):
    file_length = len(args)
    file_dict = {}

    if file_length < 2:
        print("Error! Need more than 2 binary files.")
        return

    # Looping through each file and storing its hex data (as a string) into the dictionary
    for file in args:
        with open(file, 'rb') as f:
            hexdata = f.read().hex()
            file_dict[file] = hexdata
            print('Hex data for', file, ':', file_dict[file])

    # Building the Suffix Array
    st = build_suffix_tree.SuffixTree(list(file_dict.values()))
    longest_strand, indexes, offset_list = st.longest_strand()

    print("The longest strand is:", longest_strand)
    print("The length of the strand is:", len(longest_strand))

    file_list = list(file_dict.keys())
    file_length = 0
    iter_offset_list = iter(offset_list)
    helper_list = []
    for file_number in indexes:
        file = file_list[file_number]
        helper_list.append(file)

    for file in file_list:
        if file in helper_list:
            print("The largest strand appears in:", file, "and the offset is", next(iter_offset_list) - file_length)
        file_length += len(file_dict[file]) + 1


if __name__ == '__main__':
    longest_bytes('sample.1', 'sample.2')
    # longest_bytes(sys.argv[1:])
    # dummyTest = ["rofl", "2rofl", "rofl"]
    # st = build_suffix_tree.SuffixTree(dummyTest)
    # longest_strand, indexes, offset_list = st.longest_strand()
    # print(longest_strand)
    #
    # iter_offset_list = iter(offset_list)
    # file_length = 0
    # for file_number in indexes:
    #     print("The largest strand appears in:", file_number, "and the offset is", next(iter_offset_list) - file_length)
    #     file_length += len(dummyTest[file_number]) + 1

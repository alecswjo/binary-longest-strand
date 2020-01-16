#!/usr/bin/python3

import suffix_tree
import os

def longest_strand(*args):
    """
    Given a large number of binary files, this program finds the longest strand of bytes that is identical between
    two or more files by constructing a Generalized Suffix Tree. The program then calls longest_strand to print the
    longest strand of bytes.

        :param args: a list of binary files
        :return: Prints the following:
            - the longest strand of bytes that is identical between two or more files
            - the length of the strand
            - the file names where the largest strand appears
            - the offset where the strand appears in each file

    """
    file_length = len(args)
    file_dict = {}

    if file_length < 2:
        print("Error! Need more than 2 binary files.")
        return

    # Accessing test files in a different directory
    current_directory = os.getcwd()
    file_path = current_directory + '/test_samples/'

    # Looping through each file and storing the file's name as the key and the hex data as the value in a dictionary
    for file in args:
        with open(file_path + file, 'rb') as f:
            hex_data = f.read().hex()
            file_dict[file] = hex_data

    # Building the Suffix Tree
    hex_data_list = list(file_dict.values())
    s_tree = suffix_tree.SuffixTree(hex_data_list)
    longest_strand, indexes, offset_list = s_tree.longest_strand()

    print("The longest strand is:", longest_strand)
    print("The length of the strand is:", len(longest_strand))

    # Figuring out the offset where the strand appears in each file
    file_names, iter_offset_list = list(file_dict.keys()), iter(offset_list)
    file_length = 0
    helper_list = []

    for file_number in indexes:
        file = file_names[file_number]
        helper_list.append(file)

    for file in file_names:
        if file in helper_list:
            print("The largest strand appears in:", file, "and the offset is", next(iter_offset_list) - file_length)
        file_length += len(file_dict[file]) + 1


if __name__ == '__main__':
    """
        Given the input list of ['sample.1', 'sample.2', 'sample.3', 'sample.4','sample.5', 
                  'sample.6', 'sample.7', 'sample.8', 'sample.9', 'sample.10']

        Should output:

            The longest strand is: 01b2cdb229d7110e80518755b030c1144f7741f05... (condensed because it's really long)
            The length of the strand is: 55297
            The largest strand appears in: sample.2 and the offset is 6143
            The largest strand appears in: sample.3 and the offset is 34815

    """

    longest_strand('sample.1', 'sample.2', 'sample.3', 'sample.4', 'sample.5',
                  'sample.6', 'sample.7', 'sample.8', 'sample.9', 'sample.10')

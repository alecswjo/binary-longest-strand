#!/usr/bin/python3

import suffix_tree

if __name__ == '__main__':
    """
    Test case to see if the Suffix Tree implementation works correctly. 
    
    Give the input list of ["33", "AA2222", "BBB2222", "CCC33333"],
    
    Should output:
    
        The longest strand of bytes that is identical between two or more files is: 2222
        The length of the strand is: 4
        The largest strand appears in file: 2 and the offset is 2
        The largest strand appears in file: 3 and the offset is 3
        
    """

    test = ["33", "AA2222", "BBB2222", "CCC33333"]
    suffix_tree = suffix_tree.SuffixTree(test)
    longest_strand, indexes, offset_list = suffix_tree.longest_strand()
    print("The longest strand of bytes that is identical between two or more files:", longest_strand)
    print("The length of the strand is:", len(longest_strand))

    file_length, counter = 0, 0
    iter_offset_list = iter(offset_list)

    for file in test:
        if counter in indexes:
            print("The largest strand appears in file", counter + 1, "and the offset is",
                  next(iter_offset_list) - file_length)
        file_length += len(file) + 1
        counter += 1

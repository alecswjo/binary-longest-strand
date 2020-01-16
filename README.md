# binary-longest-strand
Given a large number of binary files, this program finds the longest strand of bytes that is identical between two or more files.

The program displays:
- the longest strand
- the length of the strand
- the file names where the largest strand appears
- the offset where the strand appears in each file

## Design Philosophy 
This problem is very similar to the Longest Common Substring problem with a few alterations. The main difference is that it’s asking for the longest strand of bytes in at least two files and not for all the files. Initially, I thought of two main methods to attack this problem: Dynamic Programming and building a Generalized Suffix Tree. I decided to go with the Generalized Suffix Tree because it has a much better performance compared to Dynamic Programming (O(n<sub>1</sub> + n<sub>2</sub> + ... + n<sub>m</sub>) for Generalized Suffix Tree vs.  O(n<sub>1</sub> * n<sub>2</sub> * ... * n<sub>m</sub>) for Dynamic Programming where n is the length of each file and m is the number of files). 

Before constructing the Generalized Suffix Tree, I first converted the binary files into Hex  data (as a string) and concatenated each string with a different special character at the end (Example: $%.. etc) that wouldn’t be found in any of the strings in order to tell which string came from which file. All the strings were then concatenated with each other.

To construct the Suffix Tree, I decided to use McCreight’s Algorithm, which builds the Suffix Tree in linear time: O(n) where n is the length of the concatenated string. I used several online resources to build my own implementation of the Suffix Tree using McCreight’s Algorithm in Python. (Sources: [McCreight's Algorithm Applications of Suffix Tree](https://www.cs.helsinki.fi/u/tpkarkka/opetus/13s/spa/lecture10-2x4.pdf), [String Algorithms - McCreight's Algorithm](https://www.youtube.com/watch?v=5dgheXY8IZ0)).

After the Suffix Tree is constructed, I found the longest strand of bytes that’s identical between two or more files by using recursion to find the deepest node that has been created by at least two strings (the node's set of general_indexes is larger than 1). This deepest node contains the longest strand of bytes that is identical between two or more files. This search takes linear time as it only needs to visit each node once: O(n) where n is the number of nodes. The Suffix Tree also allows the user to easily find which files the strand was located in and the offset in each file. 

## Files
- longest_strand.py: This file calls suffix_tree.py to construct the suffix_tree and find the longest strand of bytes that's identical between two or more files. Users can input the names of different binary files into the longest_strand function.
- suffix_tree.py: Contains the classses for SuffixTree and SuffixNode. This file builds the Generalized Suffix Tree using McCreight's Algorithm and contains functionality to find the longest strand of bytes that’s identical between two or more files
- test.py: This file contains a basic test case to see if the Suffix Tree implementation works correctly. Uses strings, rather than binary files, for a more transparent example. Users can use this to find the longest substring that's identical between two or more strings (rather than binary files) by inputting their own strings into the input list.

#!/usr/bin/python3

from string import punctuation


# Class for Suffix Tree
class SuffixTree:
    """Class that represents a Generalized Suffix Tree

    :param input_list: a list of hex data
    """
    def __init__(self, input_list):
        self.root_node = SuffixNode()
        self.root_node.depth = 0
        self.root_node.index = 0
        self.root_node.parent = self.root_node
        self.root_node.add_link(self.root_node)
        self.sentinel_indexes = []
        self.build_helper(input_list)

    def build_helper(self, list):
        """Helper function before building the Suffix Tree.

        Loops through each string in the list and adds a sentinel to the end of each one. This is used to distinguish
        between all the given strings when they are concatenated into one large string to build the suffix tree.

        """

        final_string = ""
        sentinel = 0

        # Adding a sentinel to the end of each string
        for string in list:
            self.sentinel_indexes.append(len(final_string))
            final_string += string
            final_string += punctuation[sentinel]
            sentinel += 1

        self.full_string = final_string
        self.build_tree(final_string)
        self.root_node.traverse(self.label_nodes)

    def build_tree(self, text):
        """Builds a generalized suffix tree using McCreight's Algorithm"""

        current_node = self.root_node
        current_depth = 0
        for i in range(len(text)):
            while current_node.depth == current_depth and current_node.transition_verify(text[current_depth + i]):
                current_node = current_node.get_transition(text[current_depth + i])
                current_depth += 1
                while current_depth < current_node.depth and text[current_node.index + current_depth] == text[
                    i + current_depth]:
                    current_depth += 1
            if current_depth < current_node.depth:
                current_node = self.new_node(text, current_node, current_depth)
            self.new_leaf(text, i, current_node, current_depth)
            if not current_node.get_link():
                self.new_slink(text, current_node)
            current_node = current_node.get_link()
            current_depth -= 1
            if current_depth < 0:
                current_depth = 0

    def label_nodes(self, input_node):
        """Labels the nodes of the Generalized Suffix Tree with indexes of strings found in their descendants"""
        if input_node.leaf_verify():
            result = {self.first_index(input_node.index)}
        else:
            result = {node for nodes in input_node.transition_links for node in nodes[0].general_indexes}
        input_node.general_indexes = result

    def first_index(self, index):
        """Returns the index of the string based on node's starting index"""
        counter = 0
        for index2 in self.sentinel_indexes[1:]:
            if index < index2:
                return counter
            counter += 1
        return counter

    def new_node(self, input, current_node, depth):
        """Creates a new (non-leaf) node for the suffix tree"""

        index = current_node.index
        parent = current_node.parent
        result = SuffixNode(index=index, depth=depth)
        result.add_transition(current_node, input[index + depth])
        current_node.parent = result
        parent.add_transition(result, input[index + parent.depth])
        result.parent = parent
        return result

    def new_leaf(self, num, index, current_node, depth):
        """Creates a new leaf node for the suffix tree"""

        result = SuffixNode()
        result.index = index
        result.depth = len(num) - index
        current_node.add_transition(result, num[index + depth])
        result.parent = current_node
        return result

    def new_slink(self, input, current_node):
        """Creates a new slink for the suffix tree"""

        depth = current_node.depth
        result = current_node.parent.get_link()
        while result.depth < depth - 1:
            result = result.get_transition(input[current_node.index + result.depth + 1])
        if result.depth > depth - 1:
            result = self.new_node(input, result, depth - 1)
        current_node.add_link(result)

    def longest_strand(self):
        """Returns the longest strand of bytes that is identical between two or more files, the list of indexes (or
        which files where the longest strand was found), and the list of offsets (where in the files the strings were
        found)

        This function relies on longest_strand_helper to find the deepest node that has been created by
        at least two strings.
        """
        deepest_suffix_node = self.longest_strand_helper(self.root_node)
        start = deepest_suffix_node.index
        end = deepest_suffix_node.index + deepest_suffix_node.depth

        return self.full_string[start:end], deepest_suffix_node.general_indexes, [n.index for n in
                                                                                  deepest_suffix_node.get_leaves()]

    def longest_strand_helper(self, node):
        """Returns the deepest node that has been created by at least two strings.

        This function uses recursion to find deepest node that has been created by at least two strings (the node's set
        of general_indexes is larger than 1). This deepest node contains the longest strand of bytes that is identical
        between two or more files.
        """
        result = [self.longest_strand_helper(node) for (node, _) in node.transition_links if
                  len(node.general_indexes) > 1]

        if not result:
            return node

        deepest_suffix_node = max(result, key=lambda x: x.depth)
        return deepest_suffix_node


# Class for Suffix Node
class SuffixNode:
    """Class that represents a node for a Suffix Tree"""

    def __init__(self, index=-1, parent_node=None, depth=-1):
        self.index = index
        self.depth = depth
        self.parent = parent_node
        self.general_indexes = {}

        self.link = None
        self.transition_links = []

    def add_link(self, node):
        """Creates a new link for the node"""

        self.link = node

    def get_link(self):
        """Returns the link for the node"""

        if self.link is not None:
            return self.link
        return False

    def get_transition(self, suffix):
        """Returns the transition node for the suffix"""

        for node, suffix2 in self.transition_links:
            if suffix == suffix2:
                return node
        return False

    def add_transition(self, node, suffix):
        """Adds a transition node for the suffix"""

        transition = self.get_transition(suffix)
        if transition:
            self.transition_links.remove((transition, suffix))
        self.transition_links.append((node, suffix))

    def transition_verify(self, suffix):
        """Verifies transition node for the suffix"""

        for node, suffix2 in self.transition_links:
            if suffix == suffix2:
                return True
        return False

    def leaf_verify(self):
        """Verifies whether node is a leaf node"""

        return self.transition_links == []

    def traverse(self, func):
        """Takes a function as an argument and applies that to all the transition links of the tree"""

        for (node, _) in self.transition_links:
            node.traverse(func)
        func(self)

    def get_leaves(self):
        """Returns all the leaf nodes"""

        if self.leaf_verify():
            return [self]
        return [leaf for (node, _) in self.transition_links for leaf in node.get_leaves()]

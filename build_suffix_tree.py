#!/usr/bin/python

import sys
from string import punctuation


# Class for Suffix Tree
class SuffixTree():
    # Input should be all the strings concatenated
    def __init__(self, string):
        self.root_node = SuffixNode()
        self.root_node.depth = 0
        self.root_node.index = 0
        self.root_node.parent = self.root_node
        self.root_node.add_link(self.root_node)
        self.sentinel_indexes = []
        self.build_helper(string)

    def label_nodes(self, input_node):
        # Labels the nodes of the Generalized Suffix Tree with indexes of strings found in their descendants
        if input_node.leaf_verify():
            result = {self.first_index(input_node.index)}
        else:
            result = {node for nodes in input_node.transition_links for node in nodes[0].general_indexes}
        input_node.general_indexes = result

    def first_index(self, index):
        # This returns the index of the string based on  node's starting index
        counter = 0
        for index2 in self.sentinel_indexes[1:]:
            if index < index2:
                return counter
            counter += 1
        return counter

    def build_helper(self, list):
        final_string = ""
        sentinel = 0

        for string in list:
            self.sentinel_indexes.append(len(final_string))
            final_string += string
            final_string += punctuation[sentinel]
            sentinel += 1

        self.full_string = final_string
        self.build_tree(final_string)
        self.root_node.traverse(self.label_nodes)

    # This builds a suffix tree using McCreight's Algorithm
    def build_tree(self, text):
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

    def new_node(self, input, current_node, depth):
        index = current_node.index
        parent = current_node.parent
        result = SuffixNode(index=index, depth=depth)
        result.add_transition(current_node, input[index + depth])
        current_node.parent = result
        parent.add_transition(result, input[index + parent.depth])
        result.parent = parent
        return result

    def new_leaf(self, num, index, current_node, depth):
        result = SuffixNode()
        result.index = index
        result.depth = len(num) - index
        current_node.add_transition(result, num[index + depth])
        result.parent = current_node
        return result

    def new_slink(self, input, current_node):
        depth = current_node.depth
        result = current_node.parent.get_link()
        while result.depth < depth - 1:
            result = result.get_transition(input[current_node.index + result.depth + 1])
        if result.depth > depth - 1:
            result = self.new_node(input, result, depth - 1)
        current_node.add_link(result)

    def longest_strand(self):
        deepest_suffix_node = self.longest_strand_helper(self.root_node)
        start = deepest_suffix_node.index
        end = deepest_suffix_node.index + deepest_suffix_node.depth

        return self.full_string[start:end], deepest_suffix_node.general_indexes, [n.index for n in deepest_suffix_node.get_leaves()]

    def longest_strand_helper(self, node):
        result = [self.longest_strand_helper(node) for (node, _) in node.transition_links if
                  len(node.general_indexes) > 1]

        if result == []:
            return node

        deepest_suffix_node = max(result, key=lambda x: x.depth)
        return deepest_suffix_node


# Class for Suffix Node
class SuffixNode():
    def __init__(self, index=-1, parent_node=None, depth=-1):
        self.index = index
        self.depth = depth
        self.parent = parent_node
        self.general_indexes = {}

        self.link = None
        self.transition_links = []

    def add_link(self, node):
        self.link = node

    def get_link(self):
        if self.link != None:
            return self.link
        return False

    def get_transition(self, suffix):
        for node, suffix2 in self.transition_links:
            if suffix == suffix2:
                return node
        return False

    def add_transition(self, node, suffix=''):
        transition = self.get_transition(suffix)
        if transition:
            self.transition_links.remove((transition, suffix))
        self.transition_links.append((node, suffix))

    def transition_verify(self, suffix):
        for node, suffix2 in self.transition_links:
            if suffix2 == '__@__' or suffix == suffix2:
                return True
        return False

    def leaf_verify(self):
        return self.transition_links == []

    def traverse(self, func):
        for (node, _) in self.transition_links:
            node.traverse(func)
        func(self)

    def get_leaves(self):
        if self.leaf_verify():
            return [self]
        return [leaf for (node, _) in self.transition_links for leaf in node.get_leaves()]
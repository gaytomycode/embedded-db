#!/usr/bin/env python3
import os
import json
from collections import deque

class Node:
    def __init__(self, is_leaf=False):
        self.keys = []
        self.pointers = []
        self.is_leaf = is_leaf
        self.next_leaf = None

    def __str__(self):
        return f"Node(keys={self.keys}, is_leaf={self.is_leaf})"

    def to_dict(self):
        return {
            'keys': self.keys,
            'pointers': [pointer.to_dict() if not self.is_leaf else pointer for pointer in self.pointers],
            'is_leaf': self.is_leaf
        }

    @classmethod
    def from_dict(cls, data):
        node = cls(is_leaf=data['is_leaf'])
        node.keys = data['keys']
        node.pointers = [Node.from_dict(pointer) if not node.is_leaf else pointer for pointer in data['pointers']]
        return node

class BPlusTree:
    def __init__(self, order=6, tree_file="tree.json"):
        self.order = order
        self.tree_file = tree_file
        self._load_tree()

    def _load_tree(self):
        if os.path.exists(self.tree_file):
            with open(self.tree_file, "r") as file:
                tree_data = json.load(file)
                self.root = Node.from_dict(tree_data['root'])
                self.data = {int(k): v for k, v in tree_data['data'].items()}
        else:
            self.root = Node(is_leaf=True)
            self.data = {}

    def _save_tree(self):
        with open(self.tree_file, "w") as file:
            tree_data = {
                'root': self.root.to_dict(),
                'data': self.data
            }
            json.dump(tree_data, file)

    def _find_leaf(self, key):
        node = self.root
        while not node.is_leaf:
            idx = next((i for i, k in enumerate(node.keys) if k > key), len(node.keys))
            if idx < len(node.pointers):
                node = node.pointers[idx]
            else:
                break
        return node

    def insert(self, key, value):
        leaf = self._find_leaf(key)

        if key in leaf.keys:
            self.data[key] = value
        else:
            idx = next((i for i, k in enumerate(leaf.keys) if k > key), len(leaf.keys))
            leaf.keys.insert(idx, key)
            leaf.pointers.insert(idx, key)
            self.data[key] = value

        if len(leaf.keys) > self.order - 1:
            self._split_node(leaf)

        self._save_tree()

    def _split_node(self, node):
        mid = len(node.keys) // 2
        right_node = Node(is_leaf=node.is_leaf)

        right_node.keys = node.keys[mid:]
        right_node.pointers = node.pointers[mid:]
        node.keys = node.keys[:mid]
        node.pointers = node.pointers[:mid]

        if node.is_leaf:
            node.next_leaf = right_node
        else:
            for pointer in right_node.pointers:
                parent = self._find_parent(pointer)
                if parent is not None:
                    idx = next((i for i, k in enumerate(parent.keys) if k > right_node.keys[0]), len(parent.keys))
                    parent.pointers[idx] = right_node

        if node == self.root:
            new_root = Node()
            new_root.keys = [right_node.keys[0]]
            new_root.pointers = [node, right_node]
            self.root = new_root
        else:
            parent = self._find_parent(node)
            idx = next((i for i, k in enumerate(parent.keys) if k > right_node.keys[0]), len(parent.keys))
            parent.keys.insert(idx, right_node.keys[0])
            parent.pointers.insert(idx + 1, right_node)

            if len(parent.keys) > self.order - 1:
                self._split_node(parent)

    def _find_parent(self, child, node=None):
        if node is None:
            node = self.root

        for i, pointer in enumerate(node.pointers):
            if child == pointer:
                return node
            if not pointer.is_leaf:
                if i + 1 < len(node.pointers) and child.keys[0] < node.keys[i]:
                    parent = self._find_parent(child, pointer)
                    if parent is not None:
                        return parent
                elif i + 1 >= len(node.pointers) or (i + 1 < len(node.keys) and child.keys[0] < node.keys[i + 1]):
                    parent = self._find_parent(child, pointer)
                    if parent is not None:
                        return parent

    def get(self, key):
        node = self._find_leaf(key)
        while node:
            if key in node.keys:
                return self.data[key]
            node = node.next_leaf
        return None

    def get_range(self, start_key, end_key):
        leaf = self._find_leaf(start_key)
        results = []

        while leaf:
            for key in leaf.keys:
                if start_key <= key <= end_key:
                    results.append(self.data[key])
                elif key > end_key:
                    break
            leaf = leaf.next_leaf

        return results

if __name__ == "__main__":
    bplus_tree = BPlusTree(order=6)

    for i in range(1, 51):
        bplus_tree.insert(i, f"value_{i}")

    for i in range(1, 51):
        print(bplus_tree.get(i))

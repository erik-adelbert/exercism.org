"""
Binary search tree basic implementation
"""


class TreeNode:
    """Represents a node in a binary search tree."""

    def __init__(self, data, left=None, right=None):
        """Initializes a new node with the specified data.

        Args:
            data: The data stored in the node.
            left (TreeNode, optional): The left subtree of the node.
            right (TreeNode, optional): The right subtree of the node.
        """
        self.data = data
        self.left = left
        self.right = right

    def __str__(self):
        return f"TreeNode(data={self.data}, left={self.left}, right={self.right})"


class BinarySearchTree:
    """Represents a binary search tree."""

    def __init__(self, tree_data: list):
        """Initializes a new binary search tree with the specified data.

        Args:
            tree_data (list): A list containing the data to insert into the tree.
        """
        self.root = None
        list(map(self.insert, tree_data))

    def insert(self, data):
        """Inserts new data into the tree.

        Args:
            data: The data to insert into the tree.
        """
        self.root = self._reinsert(self.root, data)

    def _reinsert(self, node: TreeNode, data: any) -> TreeNode:
        """Recursively inserts new data into the tree.

        Args:
            node (TreeNode): The node from which to insert the data.
            data: The data to insert into the tree.

        Returns:
            TreeNode: The updated node after inserting the data.
        """
        if node is None:
            return TreeNode(data)
        if data <= node.data:
            node.left = self._reinsert(node.left, data)
        elif data > node.data:
            node.right = self._reinsert(node.right, data)
        return node

    def data(self):
        """Retrieves the root of the tree."""
        return self.root

    def sorted_data(self):
        """Retrieves the data from the tree sorted in ascending order."""
        ordered = []
        self._retraverse(self.root, ordered)
        return ordered

    def _retraverse(self, node, ordered):
        """Recursively traverses the tree and adds sorted data to the flat list.

        Args:
            node (TreeNode): The node to start the traversal from.
            flat (list): The flat list to add the sorted data to.
        """
        if node:
            self._retraverse(node.left, ordered)
            ordered.append(node.data)
            self._retraverse(node.right, ordered)

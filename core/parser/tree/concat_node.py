class ConcatNode:
    """
    ConcatNode determine the structure of a node in case of concatenation
    """
    def __init__(self, left, right) -> None:
        """
        Initialize the left and the right child

        :param left: Left child
        :param right: Right child
        """
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        """
        Helps in debugging

        :return: Formated String
        """
        return f"ConcatNode({self.left}, {self.right})"

class PipeNode:
    """
    PipeNode determine the structure of a node in case of `OR Operation`
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

        :return Formated String
        """
        return f"PipeNode({self.left}, {self.right})"
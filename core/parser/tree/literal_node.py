class LiteralNode:
    """
    LiteralNode define the structure of a node in case a normal literal
    """
    def __init__(self, literal) -> None:
        """
        Initialize the literal for the literal node

        :param literal: Literal
        """
        self.literal = literal

    def __repr__(self) -> str:
        """
        Helps in debugging

        :return Formated String
        """
        return f"LiteralNode('{self.literal}')"

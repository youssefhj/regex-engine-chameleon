class KleeneNode:
    """
    KleeneNode define the structure of a node in case Kleene Closure
    """
    def __init__(self, literal) -> None:
        """
        Initialize the literal for the kleene node

        :param literal: Literal
        """
        self.literal = literal

    def __repr__(self) -> str:
        """
        Helps in debugging

        :return Formated String
        """
        return f"KleeneNode({self.literal})"
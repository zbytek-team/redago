from abc import ABC, abstractmethod


class BaseCorrector(ABC):
    """Abstract base class for all correctors.

    A corrector is a class that implements a method `correct` that takes a
    string as input and returns a corrected version of the string.
    """

    @abstractmethod
    def correct(self, text: str) -> str:
        """Corrects the given text.

        Args:
            text (str): The text to correct.

        Returns:
            str: The corrected text.
        """
        pass

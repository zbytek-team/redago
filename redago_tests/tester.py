from dotenv import load_dotenv
import os
import logging
from corrector_core.comma_corrector import Corrector

load_dotenv()

logging.basicConfig(level=logging.INFO)

SAVE_INCORRECT_PREDICTIONS = os.getenv("SAVE_INCORRECT_PREDICTIONS") == "1"


class Tester:
    """
    Tester for single sentence punctuation.
    Takes correct sentence as input,
    transforms it to sentence without commas
    and checks if checker returns correct result.
    """

    def __init__(self, sentences: list[str] = []):
        self._corrector = Corrector()
        self._sentences = sentences

    def split_with_commas(self, sentence: str) -> list[str]:
        """
        Splits sentence into list of words (including commas as separate words)
        """

        return sentence.replace(",", " ,").split(" ")

    def save_incorrect(self, sentence: str, corrected_sentence: str) -> None:
        """
        Saves incorrect sentence to file.
        """

        with open("incorrect.txt", "a", encoding="utf-8") as f:
            f.write(f"ORIGINAL:\t{sentence}\n")
            f.write(f"CORRECTED:\t{corrected_sentence}\n\n")

    def _rate_sentence(
        self, corrected_sentence: str, original_sentence: str
    ) -> dict[str, int]:
        """
        Rates correctness of corrected sentence.
        """

        # create index for both documents
        corrected_pos: int = 0
        sentences_pos: int = 0

        # create dict for points
        points: dir[str, int] = {"correct": 0, "incorrect": 0, "missing": 0}

        # iterate through both documents
        while sentences_pos < len(original_sentence) and corrected_pos < len(
            corrected_sentence
        ):
            # get tokens
            original = original_sentence[sentences_pos]

            corrected = corrected_sentence[corrected_pos]

            # if both tokens are commas, add point to correct
            if original == "," and corrected == ",":
                points["correct"] += 1
            # if token in sentences is comma and token in corrected is not, add point to missing
            elif original == "," and corrected != ",":
                points["missing"] += 1
                corrected_pos -= 1
            # if token in sentences is not comma and token in corrected is, add point to incorrect
            elif original != "," and corrected == ",":
                points["incorrect"] += 1
                sentences_pos -= 1

            # increment both indexes
            sentences_pos += 1
            corrected_pos += 1

        if SAVE_INCORRECT_PREDICTIONS and (
            points["incorrect"] > 0 or points["missing"] > 0
        ):
            self.save_incorrect(original_sentence, corrected_sentence)

        return points

    def _rate(self, corrected_sentences, original_sentences) -> dict[str, int]:
        """
        Rates correctness of corrected sentences.
        """
        points: dict[str, int] = {"correct": 0, "incorrect": 0, "missing": 0}

        for corrected_sentence, original_sentence in zip(
            corrected_sentences, original_sentences
        ):
            result = self._rate_sentence(corrected_sentence, original_sentence)
            points["correct"] += result["correct"]
            points["incorrect"] += result["incorrect"]
            points["missing"] += result["missing"]

        return points

    def test(self, original_sentences: list[str] = []) -> dict[str, int]:
        # transform sentences to sentences without commas
        no_commas_sentences: list[str] = [
            sentence.replace(",", "") for sentence in original_sentences
        ]

        # correct sentence and get result
        corrected_sentences = [
            self._corrector.correct(sentence) for sentence in no_commas_sentences
        ]

        # return rated result in format {'correct': int, 'incorrect': int, 'missing': int}
        return self._rate(corrected_sentences, original_sentences)

import logging
from redago_core.correctors.ort_corrector import OrtCorrector

logging.basicConfig(level=logging.INFO)

SAVE_INCORRECT_PREDICTIONS = 1


class Tester:
    """
    Tester for single sentence ortography.
    Takes correct sentence as input,
    transforms it to sentence with ortography errors
    and checks if checker returns correct result.
    """

    def __init__(self, sentences: list[str] = []):
        self._corrector = OrtCorrector()
        self._sentences = sentences

    def split_sentence(self, sentence: str) -> list[str]:
        """
        Splits sentence into list of words
        """

        return sentence.replace(",", " ").strip().split()

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

        # split sentences into words
        corrected_sentence = self.split_sentence(corrected_sentence)
        original_sentence = self.split_sentence(original_sentence)

        # create dict for points
        points: dir[str, int] = {"correct": 0, "incorrect": 0}

        # iterate through both documents
        for word1, word2 in zip(corrected_sentence, original_sentence):
            # if words are the same
            if word1 == word2:
                points["correct"] += 1
            # if corrected word is different than original
            else:
                points["incorrect"] += 1
        

        if SAVE_INCORRECT_PREDICTIONS and (
            points["incorrect"] > 0
        ):
            self.save_incorrect(original_sentence, corrected_sentence)

        return points

    def _rate(self, corrected_sentences, original_sentences) -> dict[str, int]:
        """
        Rates correctness of corrected sentences.
        """
        points: dict[str, int] = {"correct": 0, "incorrect": 0}

        for corrected_sentence, original_sentence in zip(
            corrected_sentences, original_sentences
        ):
            result = self._rate_sentence(corrected_sentence, original_sentence)
            points["correct"] += result["correct"]
            points["incorrect"] += result["incorrect"]

        return points

    def errorify(self, sentence: str) -> str:
        """
        Transforms sentence to sentence with ortography errors.
        """

        # change polish letters to wrong ones
        sentence = sentence.replace("ą", "a")
        sentence = sentence.replace("ć", "c")
        sentence = sentence.replace("ę", "en")
        sentence = sentence.replace("ł", "l")
        sentence = sentence.replace("ń", "n")
        sentence = sentence.replace("ó", "u")
        sentence = sentence.replace("ś", "s")
        sentence = sentence.replace("ź", "z")
        sentence = sentence.replace("ż", "rz")

            

    def test(self, original_sentences: list[str] = []) -> dict[str, int]:
        # transform sentences to sentences with ortography errors
        error_sentences = [
            self.errorify(sentence) for sentence in original_sentences
        ]

        # correct sentence and get result
        corrected_sentences = [
            self._corrector.correct(sentence) for sentence in error_sentences
        ]

        # return rated result in format {'correct': int, 'incorrect': int, 'missing': int}
        return self._rate(corrected_sentences, original_sentences)

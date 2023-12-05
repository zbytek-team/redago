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

    def save_incorrect(self, sentence: str, corrected_sentence: str, error_sentence) -> None:
        """
        Saves incorrect sentence to file.
        """

        with open("incorrect.txt", "a", encoding="utf-8") as f:
            f.write(f"ORIGINAL:\t{sentence}\n")
            f.write(f"CORRECTED:\t{corrected_sentence}\n")
            f.write(f"ERROR:\t{error_sentence}\n\n")


    def _rate_sentence(
        self, corrected_sentence: str, original_sentence: str, error_sentence: str
    ) -> dict[str, int]:
        """
        Rates correctness of corrected sentence.
        """

        # split sentences into words
        corrected_sentence = self.split_sentence(corrected_sentence)
        original_sentence = self.split_sentence(original_sentence)
        error_sentence = self.split_sentence(error_sentence)

        # create dict for points
        # true positive - word was errored and corrected
        # false positive - word was errored but not corrected
        # false negative - word was not errored but corrected
        points: dir[str, int] = {"true positive": 0, "false positive": 0, "false negative": 0}

        # iterate through both documents
        for correct_word, original_word, error_word in zip(
            corrected_sentence, original_sentence, error_sentence
        ):
            # if word was errored
            if error_word != original_word:
                # if word was corrected
                if correct_word != original_word:
                    points["true positive"] += 1
                # if word was not corrected
                else:
                    points["false positive"] += 1
            # if word was not errored
            else:
                # if word was corrected
                if correct_word != original_word:
                    points["false negative"] += 1
        

        if SAVE_INCORRECT_PREDICTIONS and (
            points["false positive"] > 0 or points["false negative"] > 0
        ):
            self.save_incorrect(original_sentence, corrected_sentence, error_sentence)

        return points

    def _rate(self, corrected_sentences, original_sentences, error_sentences) -> dict[str, int]:
        """
        Rates correctness of corrected sentences.
        """
        points: dict[str, int] = {"true positive": 0, "false positive": 0, "false negative": 0}

        for corrected_sentence, original_sentence, error_sentence in zip(
            corrected_sentences, original_sentences, error_sentences
        ):
            result = self._rate_sentence(corrected_sentence, original_sentence, error_sentence)
            points["true positive"] += result["true positive"]
            points["false positive"] += result["false positive"]
            points["false negative"] += result["false negative"]

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
        sentence = sentence.replace("j", "i")

        return sentence

    def test(self, original_sentences: list[str] = []) -> dict[str, int]:
        # transform sentences to sentences with ortography errors
        error_sentences = [
            self.errorify(sentence) for sentence in original_sentences
        ]

        # join error sentences
        error_sentences = " ".join(error_sentences)

        # correct sentence and get result
        corrected_sentences = self._corrector.correct(error_sentences)
        # split by . ? !
        corrected_sentences = corrected_sentences.replace(". ", ".\n").replace("! ", "!\n").replace("? ", "?\n")

        corrected_sentences = corrected_sentences.split("\n")

        for correct, original in zip(corrected_sentences, original_sentences):
            print(f"ORIGINAL: {original}")
            print(f"CORRECTED: {correct}")
            print()

        # return rated result in format {'correct': int, 'incorrect': int, 'missing': int}
        return self._rate(corrected_sentences, original_sentences, error_sentences)

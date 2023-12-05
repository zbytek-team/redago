from redago_core.correctors.base_corrector import BaseCorrector


class SimpleCorrector(BaseCorrector):
    def correct(self, text: str) -> str:
        # if no space after ., ?, ! add it
        if ". " not in text:
            text = text.replace(".", ". ")
        if "! " not in text:
            text = text.replace("!", "! ")
        if "? " not in text:
            text = text.replace("?", "? ")

        # split text into sentences by ., ?, ! but keep the punctuation
        text = text.replace(". ", ".\n").replace("! ", "!\n").replace("? ", "?\n")

        new_text = ""

        for sentence in text.split("\n"):
            # make first letter uppercase
            sentence = sentence[0].upper() + sentence[1:]

            new_text += sentence + " "

        text = new_text

        # add a dot at the end if there is none
        if text[-1] != "." and text[-1] != "?" and text[-1] != "!":
            text += "."

        return text

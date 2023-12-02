from redago_core.correctors.base_corrector import BaseCorrector

class SimpleCorrector(BaseCorrector):
    def correct(self, text: str) -> str:
        # make first letter uppercase
        text = text[0].upper() + text[1:]

        # add a dot at the end if there is none
        if text[-1] != '.':
            text += '.'

        return text
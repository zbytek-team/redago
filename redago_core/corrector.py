from redago_core.correctors.base_corrector import BaseCorrector


class Corrector:
    def __init__(self, correctors: list[BaseCorrector]):
        self.correctors = correctors

    def correct(self, text: str) -> str:
        for corrector in self.correctors:
            text = corrector.correct(text)

        return text

from redago_core.correctors.base_corrector import BaseCorrector
import logging
import time

logging.basicConfig(level=logging.INFO)

class Corrector:
    def __init__(self, correctors: list[BaseCorrector]):
        self.correctors = correctors

    def correct(self, text: str) -> str:
        for corrector in self.correctors:
            now = time.time()
            text = corrector.correct(text)
            logging.info(f"Corrected in {time.time() - now:.2f}s")

        return text
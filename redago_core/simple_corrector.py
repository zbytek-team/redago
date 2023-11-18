# this corrector will correct sentences by:
# adding dots at the end of sentences,
# capitalizing first letter

class SimpleCorrector:
    def get_positions(self, sentence: str) -> list:
        sentence = sentence.strip()

        if sentence[0].islower():
            yield {"position": 0, "char": sentence[0].upper()}

        if sentence[-1] not in [".", "?", "!"]:
            yield {"position": len(sentence), "char": "."}



    def correct(self, sentence: str) -> str:
        sentence = sentence.strip()

        for position in self.get_positions(sentence):
            # if position char is letter, change it to uppercase
            if position["char"].isalpha():
                sentence = sentence[:position["position"]] + position["char"].upper() + sentence[position["position"] + 1:]
            else:
                sentence = sentence[:position["position"]] + position["char"] + sentence[position["position"] + 1:]
        
        return sentence
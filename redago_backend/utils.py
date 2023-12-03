def checkIfWordsAreEqual(old_word, new_word):
    return old_word == new_word


def checkIfCommaInserted(old_word, new_word):
    return old_word[-1] != "," and new_word[-1] == ","


def checkIfCommaRemoved(old_word, new_word):
    return old_word[-1] == "," and new_word[-1] != ","


def checkIfPeriodInserted(old_word, new_word):
    return old_word[-1] != "." and new_word[-1] == "."


def checkIfPeriodRemoved(old_word, new_word):
    return old_word[-1] == "." and new_word[-1] != "."


def checkIfCaseChanged(old_word, new_word):
    return old_word.lower() == new_word.lower() and old_word != new_word


def checkIfSpellingChanged(old_word, new_word):
    old_word = old_word.replace(",", "").replace(".", "")
    new_word = new_word.replace(",", "").replace(".", "")

    return old_word.lower() != new_word.lower()

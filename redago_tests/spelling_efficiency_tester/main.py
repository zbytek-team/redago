import logging
from tester import Tester
import os

logging.basicConfig(level=logging.INFO)


def load_books() -> list:
    # load books from all .txt files in books folder

    books = []
    for filename in os.listdir("books"):
        with open("books/" + filename, "r", encoding="utf-8") as f:
            # split book into sentences
            book = f.readlines()
            book = [sentence.strip() for sentence in book]
            books.extend(book)

    return books


def main():
    logging.info("Initializing tester...")
    tester = Tester()

    logging.info("Loading books...")
    books = load_books()

    logging.info("Testing corrector efficiency...")
    logging.info(tester.test(books))


if __name__ == "__main__":
    main()

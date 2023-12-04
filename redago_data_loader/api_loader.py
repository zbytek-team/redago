import requests
import logging
import random
import os


from data_preparer import DataPreparer

logging.basicConfig(level=logging.INFO)


class WolneLekturyAPILoader:
    api_url = "https://wolnelektury.pl/api/"
    data_preparer = DataPreparer()

    def fetch_books(self, limit=10, genre="epika", shuffle=True, directory="books"):
        books_url = f"{self.api_url}kinds/{genre}/books"

        logging.info(f"Fetching books from {books_url}")
        books = requests.get(books_url).json()

        if shuffle:
            random.shuffle(books)

        for book in books:
            if limit <= 0:
                break

            book_details = requests.get(book["href"]).json()

            if book_details["language"] != "pol":
                logging.warning(
                    f"Book {book_details['txt'].split('/')[-1]} is not in polish"
                )
                continue

            book_url = book_details["txt"]
            book_name = f"{book_details['txt'].split('/')[-1]}"

            if not book_url:
                logging.warning(f"Book {book_name} has no txt version")
                continue

            logging.info(f"Fetching book from {book_url}")
            book_content = requests.get(book_url).text

            if not book_content:
                logging.warning(f"Book {book_name} has no content")
                continue

            logging.info(f"Processing book {book_name}")
            processed_book = self.data_preparer.process_book(book_content)

            if not processed_book:
                logging.warning(f"Book {book_name} has no processed content")
                continue

            if os.path.exists(f"{directory}/{book_name}"):
                logging.warning(f"Book {book_name} already exists")
                continue

            logging.info(f"Yielding book {book_name}")
            yield {"name": book_name, "content": processed_book.encode("utf-8")}

            limit -= 1

    def fetch_and_save_books(
        self, limit=10, genre="epika", shuffle=True, directory="books"
    ):
        if not os.path.exists(directory):
            os.makedirs(directory)

        for book in self.fetch_books(limit=limit, genre=genre, shuffle=shuffle):
            logging.info(f"Saving book {book['name']}")
            with open(f"{directory}/{book['name']}", "wb") as f:
                f.write(book["content"])


if __name__ == "__main__":
    loader = WolneLekturyAPILoader()

    loader.fetch_and_save_books(
        limit=10, genre="epika", shuffle=True, directory="books"
    )

import logging
import os
import re
import sys

logging.basicConfig(level=logging.INFO)

PROCESSED_DIR = "processed"

SYMBOLS = r"([.,;:!?()\[\]{}„”«»–—…])"


def load(data_dir: str, training_set_size: float) -> list[list[str]]:
    """
    Loads data from files

    data_dir: directory with files to load
    training_set_size: size of training set as a fraction of all data
    """

    logging.info("Loading data...")
    files = os.listdir(data_dir)

    training_files_count = int(training_set_size * len(files))

    data: list[list[str]] = []
    for filename in files:
        if filename.endswith(".txt"):
            filepath = os.path.join(data_dir, filename)

            data.extend(get_data_from_file(filepath))

    return data[:training_files_count], data[training_files_count:]


def get_data_from_file(filepath: str) -> list[list[str]]:
    """
    Gets data from file.

    filepath: path to file
    """
    data: list[list[str]] = []

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.read().strip().split("\n")
        rows = [line.split("\t") for line in lines]
        words = [row[0] for row in rows]
        labels = [row[1] for row in rows]

        data.append([words, labels])

    return data


def process_data(data_dir: str, file: str) -> list[list[str]]:
    """
    Processes data from file.

    data_dir: directory with files to process
    file: file to process
    """

    # load file and split into words and labels (separated by tabs)
    path = os.path.join(data_dir, file)

    with open(path, "r", encoding="utf-8") as f:
        # read lines
        lines = f.read().strip().split("\n")

        # add space before each symbol
        lines = [re.sub(SYMBOLS, r" \1", line) for line in lines]

        lines = [line.split(" ") for line in lines]

        # create labels for each word
        # 1 if there is a comma after the word
        # 0 otherwise
        processed_lines: list[list[str]] = []
        for line in lines:
            for index, char in enumerate(line):
                if char == ",":
                    continue

                if index < len(line) - 1 and line[index + 1] in [","]:
                    processed_lines.append([char, "1"])
                else:
                    processed_lines.append([char, "0"])

        return processed_lines


def save_to_file(data: list[tuple[str, str]], file_path: str):
    """
    Saves data to file.

    data: data to save
    file_path: path to file
    """

    with open(file_path, "w", encoding="utf-8") as f:
        for word, label in data:
            f.write(word + "\t" + label + "\n")


if __name__ == "__main__":
    # if no arguments are given, exit
    if len(sys.argv) < 2:
        print("No arguments given.")
        print("Usage: python3 data.py <input_dir> [output_dir]")
        sys.exit(1)
    else:
        # get directory with files to process
        data_dir = sys.argv[1]

    # if output directory is given, set it
    if len(sys.argv) > 2:
        PROCESSED_DIR = sys.argv[2]

    logging.info(f"Getting files from {data_dir}...")
    files = os.listdir(data_dir)

    # create processed directory if it doesn't exist
    if not os.path.exists(PROCESSED_DIR):
        logging.info("Creating processed directory...")
        os.makedirs(PROCESSED_DIR)

    # process all files
    for file in files:
        if file.endswith(".txt"):
            logging.info(f"Processing {file}...")
            processed_lines = process_data(data_dir, file)
            logging.info(f"Processed {file}.")

            logging.info(f"Saving to {PROCESSED_DIR}/pr_{file}...")
            save_to_file(processed_lines, f"{PROCESSED_DIR}/pr_" + file)
            logging.info(f"Saved to {PROCESSED_DIR}/pr_{file}.")

    logging.info("Done.")

import json
import os
import random

class DataPreparer:
    def jsonl_to_csv(path):
        filename = path.split("/")[-1].split(".")[0]
        with open(f"data/{filename}.csv", 'w', encoding="utf8") as csv_file:
            csv_file.write("text;;expected\n")
            with open(path, 'r', encoding="utf8") as jsonl_file:
                for line in jsonl_file:
                    json_line = json.loads(line)
                    text = json_line["incorrect"]
                    expected = json_line["correct"]
                    errors = []
                    for error in json_line["errors"]:
                        # get error type
                        error_type = error["type"]
                        errors.append(error_type)
                    # if errors is empty, then skip
                    if len(errors) == 0:
                        continue
                    errors = ",".join(set(errors))
                    csv_file.write(f'{text};;{expected};;{errors}\n')

    def csv_filter_by_type(csv_path, type):
        filename = csv_path.split("/")[-1].split(".")[0]
        with open(f"data/{filename}-{type}.csv", 'w', encoding="utf8") as csv_file:
            csv_file.write("text;;expected\n")
            with open(csv_path, 'r', encoding="utf8") as r_csv_file:
                for line in r_csv_file:
                    line = line.strip()
                    if line == "text;;expected":
                        continue
                    text, expected, errors = line.split(";;")
                    errors_types = errors.split(",")
                    if len(errors_types) == 1 and errors_types[0] in type:
                        csv_file.write(f'{type + ": " + text};;{expected}\n')

    # for all csv files that ends with 'type'.csv merge them into one file named 'type'_merged.csv
    def csv_merge_by_type(path, type):
        filename = path.split("/")[-1].split(".")[0]
        with open(f"data/{type}_merged.csv", 'w', encoding="utf8") as csv_file:
            csv_file.write("text;;expected\n")
            for file in os.listdir(path):
                if file.endswith(f"{type}.csv"):
                    with open(f"{path}/{file}", 'r', encoding="utf8") as r_csv_file:
                        for line in r_csv_file:
                            line = line.strip()
                            if line == "text;;expected":
                                continue
                            text, expected = line.split(";;")
                            csv_file.write(f'{text};;{expected}\n')


    def load_data(file_path: str) -> list[str]:
        """
        Loads data from file

        file_path: file to load
        """

        data: list[list[str]] = []

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.read().strip().split("\n")
            rows = [line.strip() for line in lines]
        
        return rows

    def process_data(data: list[str]) -> list[str]:
        """
        Processes data to remove unnecessary characters and hazardous data

        data: data to process
        """

        processed_data: list[str] = []

        for row in data:
            if len(row) == 0:
                continue
            # if row contains ... somewhere, change it to .
            if "..." in row:
                row = row.replace("...", ".")

            processed_data.append(row)
        
        return processed_data

    def create_synth_data(data: list[list[str]], config: dict) -> dict[str, list[str]]:
        """
        Creates synthetic data from given data

        data: data to create synthetic data from
        """

        polish_errors_dict = {
            "sz": ["ż", "rz"],
            "rz": ["ż", "sz"],
            "ą": ["a", "on"],
            "ć": ["c", "ci"],
            "ę": ["e", "en"],
            "ł": ["l"],
            "ń": ["n", "ni"],
            "ó": ["o", "u"],
            "ś": ["s", "si"],
            "ź": ["z", "zi", "ś"],
            "ż": ["z", "rz"],
            "i": ["j"],
            "j": ["i"],
            "ch": ["h"],
            "h": ["ch"],
            "u": ["ó"]
        }
        
        letters = ["", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", \
            "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", \
            "u", "v", "w", "x", "y", "z", "ą", "ć", "ę", "ł", \
            "ń", "ó", "ś", "ź", "ż"]


        # dict["changePl"] to change polish special characters to normal characters
        # dict["changeRandom"] to change random characters in words to other random characters
        # return {str, str} where first is original sentence and second is changed sentence

        synth_data: dict[str, list[str]] = {}

        synth_data["correct"] = []
        synth_data["incorrect"] = []

        for row in data:
            # change polish special characters to normal characters
            # changePl is percentage of changing polish special characters to normal characters
            words = row.split(" ")
            sentence = []
            for word in words:
                for key, value in polish_errors_dict.items():
                    if key in word:
                        if key in ["i","I"] and len(word) <= 2:
                            continue
                        if random.random() < config["changePl"]:
                            word = word.replace(key, random.choice(value))
                    if key.capitalize() in word:
                        if key in ["i","I"] and len(word) <= 2:
                            continue
                        if random.random() < config["changePl"]:
                            word = word.replace(key.capitalize(), random.choice(value).capitalize())
                            
                sentence.append(word)
            
            words = sentence
            sentence = []
            for word in words:
                if len(word) <= 2:
                    sentence.append(word)
                    continue

                new_word: str = ""
                for char in word:
                    if random.random() < config["changeRandom"]:
                        new_word += random.choice(letters)
                    else:
                        new_word += char
                sentence.append(new_word)
            
            new_row = " ".join(sentence)
            synth_data["incorrect"].append("<ort> " + new_row)
            synth_data["correct"].append(row)

        return synth_data

    def processed_data_to_csv(data: list[dict[str, list[str]]], path: str):
        with open(path, "w", encoding="utf8") as f:
            f.write("text;;expected\n")
            for single_data in data:
                for text, expected in zip(single_data["incorrect"], single_data["correct"]):
                    f.write(f'{text};;{expected}\n')


if __name__ == "__main__":
    config = {
        "changePl": 0.2,
        "changeRandom": 0.01
    }

    books = []
    for file in os.listdir("books"):
        if file.endswith(".txt"):
            book = DataPreparer.load_data(f"books/{file}")
            processed_book = DataPreparer.process_data(book)
            synth_book = DataPreparer.create_synth_data(processed_book, config)
            books.append(synth_book)
    
    DataPreparer.processed_data_to_csv(books, "data/books.csv")
    print("books.csv created")
            
    
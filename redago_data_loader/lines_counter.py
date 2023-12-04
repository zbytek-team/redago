import os


def count_lines(file_path):
    with open(file_path, "r", encoding="utf8") as f:
        return len(f.readlines())


def count_lines_in_dir(dir_path):
    return sum([count_lines(f"{dir_path}/{file}") for file in os.listdir(dir_path)])


if __name__ == "__main__":
    print(f"Total files in books: {len(os.listdir('books'))}")
    print(f"Total lines in books: {count_lines_in_dir('books')}")

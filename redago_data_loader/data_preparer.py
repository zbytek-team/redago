import string


class DataPreparer:
    text_filter = string.ascii_letters + string.digits + " .,?!" + "ąęćłńóśźżĄĘĆŁŃÓŚŹŻ"
    lines_to_remove = 5
    words_per_line = 5

    def process_book(self, raw_data: str):
        # make one sentence per line with . ? ! as end of sentence
        raw_data = raw_data.replace(". ", ".\n")
        raw_data = raw_data.replace("! ", "!\n")
        raw_data = raw_data.replace("? ", "?\n")

        # remove sentences that have characters not belonging to self.text_filter
        data = [
            line
            for line in raw_data.split("\n")
            if all(c in self.text_filter for c in line)
        ]

        # remove empty lines
        data = [line for line in data if line]

        # in every line, remove sentences that have less than self.words_per_line words
        data = [line for line in data if len(line.split(" ")) >= self.words_per_line]

        # remove last self.lines_to_remove lines
        data = data[: -self.lines_to_remove]

        # make first letter of every sentence uppercase
        try:
            data = [line[0].upper() + line[1:] for line in data]
        except IndexError:
            pass

        # remove lines that ends with words shorter than two characters (probably abbreviations)
        data = [line for line in data if len(line.split(" ")[-1]) > 3]

        # remove lines that ends with word which contains dot not as end of sentence
        data = [line for line in data if "." not in line.split(" ")[-1][:-1]]

        return "\n".join(data)

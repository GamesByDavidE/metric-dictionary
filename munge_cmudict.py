# Derives a "metric dictionary" from the CMU Pronouncing Dictionary (available
# at https://github.com/Alexir/CMUdict/blob/master/cmudict-0.7b).

import collections
import re
import sys


# Attempts to enumerate possible meters for a stress pattern (this is not an
# exact science).
def meters_from_stresses(stresses):
    # Filter out floridly polysyllabic words and words with an unusual number of
    # primary stresses.
    if not (len(stresses) <= 4 and stresses.count("1") == 1):
        return
    if stresses == "12":
        yield "11"
    yield stresses.replace("2", "0")


def main(path_to_cmudict):
    meter_to_words = collections.defaultdict(set)
    with open(path_to_cmudict, encoding="latin-1") as file:
        for line in file:
            parts = line.split(maxsplit=1)
            if len(parts) != 2:
                continue
            word, pronunciation = parts
            if word.startswith(";"):
                continue
            word = re.sub(r"\(.*\)", "", word).lower()
            if not word.isalpha():
                continue
            stresses = "".join(c for c in pronunciation if c.isdigit())
            for meter in meters_from_stresses(stresses):
                meter_to_words[meter].add(word)
    for meter in sorted(meter_to_words):
        with open(meter + ".txt", "w") as file:
            for word in sorted(meter_to_words[meter]):
                print(word, file=file)


if __name__ == "__main__":
    main(*sys.argv[1:])

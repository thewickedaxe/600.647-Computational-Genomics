#!/usr/bin/python

import fileinput


# ************* Boilerplate *************
class Index(object):
    def __init__(self, t, k):
        """ Create index from all substrings of size 'length' """
        self.k = k  # k-mer length (k)
        self.index = {}
        for i in range(len(t) - k + 1):  # for each k-mer
            kmer = t[i:i + k]
            if kmer not in self.index:
                self.index[kmer] = [i]
            else:
                self.index[kmer].append(i)
                # could also have used collections.defaultdict

    def query(self, p):
        """ Return index hits for first k-mer of P """
        kmer = p[:self.k]  # query with first k-mer
        return self.index.get(kmer, [])


def query_index(p, t, index):
    k = index.k
    offsets = []
    for i in index.query(p):
        if p[k:] == t[i + k:i + len(p)]:  # verify that rest of P matches
            offsets.append(i)
    return offsets


# ************* Boilerplate Ends*************

sequence = ""
patterns = []
mer_index = None


def read_sequence():
    """
    Reads the shakespeare file.
    :return: None
    """
    global sequence
    file_handle = open("complete_works.txt", 'r')
    sequence = file_handle.read()


def build_index():
    """
    Builds the substr index.
    :return: None
    """
    global sequence, mer_index
    mer_index = Index(sequence, 6)


def get_patterns():
    """
    Reads input patterns.
    :return: None
    """
    global patterns
    for pattern in fileinput.input():
        patterns.append(pattern)


def find_exact_match_count(pattern):
    """
    Find the number of exact matches in the sequence.
    :param pattern: the pattern to match
    :return: None
    """
    global sequence, mer_index
    return len(query_index(pattern, sequence, mer_index))


def hamming_dist(str1, str2):
    """
    Calculates the hamming distance between 2 strings.
    :param str1: first string
    :param str2: second string
    :return: the distance
    """
    distance = 0
    for ch1, ch2 in zip(str1, str2):
        if ch1 != ch2:
            distance += 1
    return distance


def find_approx_match(pattern):
    """
    Finds an approx match with hamming distance
    :return: None 
    """
    global mer_index, sequence
    first_half, second_half = pattern[:len(pattern) / 2], pattern[len(pattern) / 2:]
    match_locations = set()
    first_match_locations = query_index(first_half, sequence, mer_index)
    second_match_locations = query_index(second_half, sequence, mer_index)

    # First half
    for location in first_match_locations:
        if hamming_dist(second_half,
                        sequence[location + len(first_half):location + len(first_half) + len(second_half)]) == 1:
            match_locations.add(location)

    # Second half
    for location in second_match_locations:
        if hamming_dist(first_half,
                        sequence[location - len(first_half): location]) == 1:
            match_locations.add(location - len(first_half))

    return len(match_locations)


def calc_specificity(exact_match_count, approx_match_count, pattern):
    """
    Calculates the specificity.
    :param exact_match_count: the number of exact matches
    :param approx_match_count: the number of approx matches
    :param pattern: the apttern
    :return: the specificity
    """
    global mer_index, sequence
    first_half, second_half = pattern[:len(pattern) / 2], pattern[len(pattern) / 2:]
    first_match_locations = query_index(first_half, sequence, mer_index)
    second_match_locations = query_index(second_half, sequence, mer_index)
    index_hits = float((len(first_match_locations) + len(second_match_locations)))
    specificity = float((exact_match_count + approx_match_count)) / index_hits
    return specificity


def print_output():
    """
    Prints the output in the desired format
    :return: None
    """
    for pattern in patterns:
        pattern = pattern.strip()
        exact_match_count = find_exact_match_count(pattern)
        approx_match_count = find_approx_match(pattern)
        print str(exact_match_count) + " " + str(approx_match_count) + " " + str(
            calc_specificity(exact_match_count, approx_match_count, pattern))


def main():
    """
    Main Sentinel.
    :return: None
    """
    read_sequence()
    get_patterns()
    build_index()
    print_output()


if __name__ == "__main__":
    main()

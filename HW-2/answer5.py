#!/usr/bin/python

import fileinput


# ************* Boilerplate *************
class Index(object):
    def __init__(self, t, bitmask):
        self.mask = bitmask
        self.index = {}

        self.mask_len = len(bitmask)

        for i in range(len(t) - self.mask_len + 1):
            subsequence = self.extract_str(t[i:i + self.mask_len])

            if subsequence not in self.index:
                self.index[subsequence] = [i]
            else:
                self.index[subsequence].append(i)

    def extract_str(self, s):
        return ''.join([s[i] for i in range(len(s)) if self.mask[i] == '1'])

    def query(self, p, offset=0):
        subsequence = self.extract_str(p[offset:self.mask_len + offset])
        return self.index.get(subsequence, [])


# ************* Boilerplate Ends*************

sequence = ""
patterns = []
index = None


def read_sequence():
    global sequence
    with open('complete_works.txt') as input:
        sequence = input.read()


def exact_match_finder(p, index):
    """
    find exact matches
    :param p: the pattern
    :param index: the index
    :return: 
    """
    mask_len = index.mask_len
    offsets = []

    index_query = index.query(p)

    for i in index_query:
        try:
            idx = index.query(p[1:]).index(i + 1)
        except ValueError:
            idx = -1

        if idx >= 0:
            offsets.append(i)

    return {'matched_offsets': list(set(offsets)), 'index_hits': list(set(index_query))}


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


def approximate_match_finder(pattern, mer_index):
    """
    find the approx matches
    :param pattern: the pattern
    :param mer_index: the index
    :return: 
    """
    global sequence
    mask_len = mer_index.mask_len
    offsets = []

    hists_forward = mer_index.query(pattern)
    hists_backward = mer_index.query(pattern, 1)

    for hit in hists_forward:
        first_half = mer_index.extract_str(pattern[1:])
        second_half = mer_index.extract_str(sequence[hit + 1:hit + len(pattern)])

        if hamming_dist(first_half, second_half) == 1:
            offsets.append(hit)

    for hit in hists_backward:
        first_half = mer_index.extract_str(pattern[:len(pattern) - 1])
        second_half = mer_index.extract_str(sequence[hit - 1:hit + mask_len - 1])

        if hamming_dist(first_half, second_half) == 1:
            offsets.append(hit - 1)

    index_hits = hists_forward + hists_backward

    return {'matched_offsets': list(set(offsets)), 'index_hits': list(set(index_hits))}


def process(pattern, mer_index):
    """
    calculates metrics.
    :param pattern: the pattern
    :param mer_index: the index
    :return: 
    """
    global sequence
    exact = exact_match_finder(pattern, mer_index)
    approx = approximate_match_finder(pattern, mer_index)

    total_occurences = len(list(set(exact['matched_offsets'] + approx['matched_offsets'])))

    index_hits = len(list(set(exact['index_hits'] + approx['index_hits'])))
    specificity = float((float(total_occurences) / float(index_hits)))

    val_map = {
        "exact_matches": len(exact["matched_offsets"]),
        "approx_matches": len(approx["matched_offsets"]),
        "specificity": specificity
    }
    return val_map


def get_patterns():
    """
    Reads input patterns.
    :return: None
    """
    global patterns
    for pattern in fileinput.input():
        patterns.append(pattern)


def main():
    """
    Main Sentinel
    :return: None
    """
    global index, sequence
    get_patterns()
    for p in patterns:
        p = p.strip()
        read_sequence()
        index = Index(sequence, '10101010101')
        metrics = process(p, index)
        print str(metrics['exact_matches']) + " " + str(metrics['approx_matches']) + " " + str(metrics['specificity'])


if __name__ == "__main__":
    main()

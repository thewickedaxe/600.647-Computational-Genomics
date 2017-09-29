#!/usr/bin/python

import sys


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

reads = []
reads_only = []
sequence = ""
mer_index = None

zero_count = 0
one_count = 0
two_count = 0
three_count = 0
four_count = 0

samp_list = []
happens = 0


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


def find_exact_match_count(pattern):
    """
    Find the number of exact matches in the text.
    :param pattern: the pattern to match
    :return: None
    """
    global sequence, mer_index
    return len(query_index(pattern, sequence, mer_index))


def parse_fastq(fh):
    """
    Parses the fastq file.
    :param fh: the file handle
    :return: a list of tuples of name, sequence, quality
    """
    global reads, reads_only
    while True:
        first_line = fh.readline()
        if len(first_line) == 0:
            break  # end of file
        name = first_line[1:].rstrip()
        seq = fh.readline().rstrip()
        fh.readline()  # ignore line starting with +
        qual = fh.readline().rstrip()
        reads.append((name, seq, qual))
    for read in reads:
        reads_only.append(read[1])
    return reads


def parse_fasta(fh):
    """
    Parses the fasta file.
    :param fh: the file handle
    :return: The fasta sequence
    """
    global sequence
    fh.readline()
    for line in fh.readlines():
        sequence = sequence + line.strip()


def build_index():
    """
    Builds the substr index.
    :return: None
    """
    global sequence, mer_index
    mer_index = Index(sequence, 30)


def generalized_mismatch_finder(pattern, num_mismatches):
    """
    Finds the index of a pattern in the sequence with a required number of mismatches.
    :param pattern: the pattern to cut up
    :param num_mismatches: the required number of mismatches
    :return: number of occurrences
    """
    global sequence, mer_index
    match_set = set()  # set of matches
    chunk_size = int(round(len(pattern) / (num_mismatches + 1)))

    z_dom = False
    o_dom = False
    t_dom = False
    th_dom = False
    f_dom = False

    for chunk_index in range(num_mismatches + 1):

        # Determine chunk start and end
        chunk_start = chunk_index * chunk_size
        chunk_end = chunk_start + chunk_size

        # Find exact matches of a chunk
        matches = mer_index.index.get(pattern[chunk_start:chunk_end], [])
        for hit in matches:
            hamming_distance = 0

            if hit < chunk_start:
                continue  # run off condition 1 -> there are more character preceding the chunk in pattern there are in the sequence
            if hit + (len(pattern) - chunk_start) > len(sequence):
                continue  # run off condition 2 -> there are fewer character left in the sequence than there are in the chunk till the end

            # Populate the mismatch counter
            for remaining_iterator in range(0, chunk_start):
                if not pattern[remaining_iterator] == sequence[hit - chunk_start + remaining_iterator]:
                    hamming_distance += 1
                    if hamming_distance > num_mismatches:
                        break
            for remaining_iterator in range(chunk_end, len(pattern)):
                if not pattern[remaining_iterator] == sequence[hit - chunk_start + remaining_iterator]:
                    hamming_distance += 1
                    if hamming_distance > num_mismatches:
                        break
            if hamming_distance <= num_mismatches:
                match_set.add(hit - chunk_start)
                if hamming_distance == 0:
                    z_dom = True
                elif hamming_distance == 1:
                    o_dom = True
                elif hamming_distance == 2:
                    t_dom = True
                elif hamming_distance == 3:
                    th_dom = True
                elif hamming_distance == 4:
                    f_dom = True
    return (z_dom, o_dom, t_dom, th_dom, f_dom)


def process():
    """
    Prints the required output.
    :return: None
    """
    global one_count, zero_count, two_count, three_count, four_count, sequence, reads

    for pattern in reads:
        zdom, o_dom, t_dom, th_dom, f_dom = generalized_mismatch_finder(pattern[1], 4)
        if zdom:
            zero_count = zero_count + 1
        elif o_dom:
            one_count = one_count + 1
        elif t_dom:
            two_count = two_count + 1
        elif th_dom:
            three_count = three_count + 1
        elif f_dom:
            four_count = four_count + 1

    # final print
    print str(zero_count) + " " + str(one_count) + " " + str(two_count) + " " + str(three_count) + " " + str(four_count)


def main():
    """
    Main Sentinel
    :return: None
    """
    parse_fastq(open(sys.argv[1], 'r'))
    parse_fasta(open(sys.argv[2], 'r'))
    build_index()
    process()


if __name__ == "__main__":
    main()

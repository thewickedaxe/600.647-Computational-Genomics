#!/usr/bin/python

from collections import defaultdict
import matplotlib.pyplot as plt
import fileinput

import sys

tree = lambda: defaultdict(tree)

# Nucleotides
ADENINE = 'A'
GUANINE = 'G'
CYTOSINE = 'C'
THYMINE = 'T'
UNKNOWN = 'N'

# phred separators
LESS20 = "less20"
MORE20 = "more20"

# The global vars
occurrence_dict = tree()
quality_dict = tree()
input_string = ""


def phred33_to_q(qual):
    """ Turn Phred+33 ASCII-encoded quality into Phred-scaled integer """
    return ord(qual) - 33


def q_to_phred33(Q):
    """ Turn Phred-scaled integer into Phred+33 ASCII-encoded quality """
    return chr(Q + 33)


def q_to_p(Q):
    """ Turn Phred-scaled integer into error probability """
    return 10.0 ** (-0.1 * Q)


def p_to_q(p):
    """ Turn error probability into Phred-scaled integer """
    import math
    return int(round(-10.0 * math.log10(p)))


def pop_dict(val):
    """
    Unit operation on dict
    :param val: the vlaue to add
    :return: None
    """
    global occurrence_dict, quality_dict
    occurrence_dict[val][ADENINE] = 0
    occurrence_dict[val][CYTOSINE] = 0
    occurrence_dict[val][GUANINE] = 0
    occurrence_dict[val][THYMINE] = 0
    occurrence_dict[val][UNKNOWN] = 0

    quality_dict[val][LESS20] = 0
    quality_dict[val][MORE20] = 0


def parse_fastq(fh):
    """ Parse reads from a FASTQ filehandle.  For each read, we
        return a name, nucleotide-string, quality-string triple. """
    reads = []
    while True:
        first_line = fh.readline()
        if len(first_line) == 0:
            break  # end of file
        name = first_line[1:].rstrip()
        seq = fh.readline().rstrip()
        fh.readline()  # ignore line starting with +
        qual = fh.readline().rstrip()
        reads.append((name, seq, qual))
    return reads


def populate_dicts():
    """
    Populates the occurrence dicts with the initial keys
    :return: None
    """
    map(pop_dict, xrange(0, 100))


def read_input_data():
    """
        Reads input data.
    """
    global input_string
    for line in fileinput.input():
        input_string = line


def process_data(reads):
    """
        Processes input data
    """
    for chunk in reads:
        ntides = chunk[1]
        qual = chunk[2]
        qual = list(map(phred33_to_q, qual))
        for i in xrange(0, len(ntides)):
            occurrence_dict[i][ntides[i]] = occurrence_dict[i][ntides[i]] + 1
            if qual[i] < 20:
                quality_dict[i][LESS20] = quality_dict[i][LESS20] + 1
            else:
                quality_dict[i][MORE20] = quality_dict[i][MORE20] + 1


def print_answer():
    """
    Prints the answer in the required format
    :return: None
    """
    lessvals = []
    for i in occurrence_dict:
        print str(occurrence_dict[i][ADENINE]) + " " + str(occurrence_dict[i][CYTOSINE]) + " " + str(
            occurrence_dict[i][GUANINE]) + " " + str(occurrence_dict[i][THYMINE]) + " " + str(
            occurrence_dict[i][UNKNOWN]) + " " + str(quality_dict[i][LESS20]) + " " + str(quality_dict[i][MORE20])
        lessvals.append(quality_dict[i][LESS20])
    #plt.xlabel("Index")
    #plt.ylabel("Count of Q < 20")
    #plt.plot(lessvals)
    #plt.show()



def main():
    global input_string
    populate_dicts()
    reads = parse_fastq(sys.stdin)
    process_data(reads)
    print_answer()


if __name__ == "__main__":
    main()

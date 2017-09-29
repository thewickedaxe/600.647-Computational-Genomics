#!/usr/bin/python
import operator
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

sequence = ""
genomes = []


def hamming_distance(str1, str2):
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


def parse_sequence(reference):
    sequence_reads = reference.split('\n')[1:]
    return ''.join(sequence_reads)


def phred33_to_q(qual):
    return ord(qual) - 33


def get_chunks(string, chunk_size):
    return [string[i:i + chunk_size] for i in range(0, len(string), chunk_size)]


def find_winner(bases, phred_values):
    base_counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0, 'N': 0}
    sorted_weights = get_ordered_phred(bases, phred_values, base_counts)
    rank = {"winner": (sorted_weights[0][0], sorted_weights[0][1])}
    if sorted_weights[1][1] != 0:
        rank["runner"] = (sorted_weights[1][0], sorted_weights[1][1])
    else:
        rank["runner"] = ('-', 0)
    return rank


def get_ordered_phred(bases, phred_values, phred_weights):
    for i, b in enumerate(bases):
        phred_weights[b] += phred_values[i]
    sorted_phred = sorted(phred_weights.items(), key=operator.itemgetter(1))
    sorted_phred.reverse()
    return sorted_phred


def approximate_match_finder(index, s, split_size):
    read_splits = get_chunks(s, split_size)
    hits = []
    process_chunks(hits, index, read_splits, s, split_size)
    return list(set(hits))


def process_chunks(hits, index, read_splits, chunk, split_size):
    for i, part in enumerate(read_splits):
        for hit in index.index.get(part, []):
            actual_hit = hit - (i * split_size)
            if len(sequence[actual_hit:actual_hit + len(chunk)]) == len(chunk):
                hits.append(actual_hit)


def main():
    global sequence
    best_matches, index, offset_read_map, phix_reads = initialize()
    process(best_matches, index, offset_read_map, phix_reads, sequence)
    col_values = {}
    get_best(col_values, offset_read_map, phix_reads, sequence)


def process(best_matches, index, offset_read_map, phix_reads, sequence):
    for locii, contents in enumerate(phix_reads):
        read = contents[1]
        max_mismatch = 5
        max_mismatch_distance = -1
        hits = approximate_match_finder(index, read, 30)
        for hit in hits:
            if hit in offset_read_map:
                offset_read_map[hit].append((read, locii))
            else:
                offset_read_map[hit] = [(read, locii)]
            hammingd = hamming_distance(read, sequence[hit: hit + len(read)])
            if hammingd < max_mismatch:
                max_mismatch = hammingd
                max_mismatch_distance = hit
                if hammingd == 1:
                    genomes.append(read + ',' + sequence[hit: hit + len(read)])
                if max_mismatch == 0:
                    break

        if max_mismatch != 5:
            best_matches[max_mismatch].append(max_mismatch_distance)


def get_best(columns, hit_map, patterns, sequence):
    for hit in hit_map:
        locus = hit_map[hit]
        if len(locus) > 0:
            bases = [locus[i][0][0] for i in range(len(locus))]
            ref_base = sequence[hit]
            if len(set(bases)) == 1 and bases[0] == ref_base:
                continue
            read_indices = [locus[i][1] for i in range(len(locus))]
            q_values = [phred33_to_q(patterns[i][2][0]) for i in read_indices]
            phred_weights = find_winner(bases, q_values)
            col = [hit, phred_weights["winner"][0], phred_weights["winner"][1], phred_weights["runner"][0],
                   phred_weights["runner"][1], ref_base]
            columns[hit] = col
    sorted_col_values = sorted(columns.items(), key=operator.itemgetter(1))
    for s in sorted_col_values:
        print(s[1])


def initialize():
    global sequence
    winner_map = {0: [], 1: [], 2: [], 3: [], 4: []}
    with open(sys.argv[2]) as ref:
        sequence = parse_sequence(ref.read())
    with open(sys.argv[1]) as reads:
        phix_reads = parse_fastq(reads)
    mer_index = Index(sequence, 30)
    hit_location = {}
    return winner_map, mer_index, hit_location, phix_reads


if __name__ == "__main__":
    main()

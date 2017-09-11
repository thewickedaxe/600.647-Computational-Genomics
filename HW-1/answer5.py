"""
    Answer to question 5
"""
import sys

ADENINE = "A"
CYTOSINE = "C"
GUANINE = "G"
THYMINE = "T"

RNA_CODON = {
    "UUU": "F","CUU": "L","AUU": "I","GUU": "V",
    "UUC": "F","CUC": "L","AUC": "I","GUC": "V",
    "UUA": "L","CUA": "L","AUA": "I","GUA": "V",
    "UUG": "L","CUG": "L","AUG": "M","GUG": "V",
    "UCU": "S","CCU": "P","ACU": "T","GCU": "A",
    "UCC": "S","CCC": "P","ACC": "T","GCC": "A",
    "UCA": "S","CCA": "P","ACA": "T","GCA": "A",
    "UCG": "S","CCG": "P","ACG": "T","GCG": "A",
    "UAU": "Y","CAU": "H","AAU": "N","GAU": "D",
    "UAC": "Y","CAC": "H","AAC": "N","GAC": "D",
    "UAA": "Stop","CAA": "Q","AAA": "K","GAA": "E",
    "UAG": "Stop","CAG": "Q","AAG": "K","GAG": "E",
    "UGU": "C","CGU": "R","AGU": "S","GGU": "G",
    "UGC": "C","CGC": "R","AGC": "S","GGC": "G",
    "UGA": "Stop","CGA": "R","AGA": "R","GGA": "G",
    "UGG": "W","CGG": "R","AGG": "R","GGG": "G" 
}

input_file = sys.argv[1]
output_file = sys.argv[2]
input_string = ""

def read_input_data():
    """
        Reads input data.
    """
    global input_string
    file_handle = open(input_file, 'r')
    input_string = file_handle.read()
    input_string = input_string.strip()


def process_data():
    """
        Processes input data
    """
    output_string = ""
    nucleotide_chunks = [input_string[i:i+3] for i in xrange(0, len(input_string), 3)]
    for chunk in nucleotide_chunks:
        if RNA_CODON[chunk] != "Stop":
            output_string = output_string + RNA_CODON[chunk]
    with open(output_file, 'w') as outfile:
        outfile.write(output_string + "\n")

def main():
    read_input_data()
    process_data()

if __name__ == "__main__":
    main()
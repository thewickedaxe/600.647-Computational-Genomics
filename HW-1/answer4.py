"""
    Answer to question 4
"""
import sys

ADENINE = "A"
CYTOSINE = "C"
GUANINE = "G"
THYMINE = "T"

input_file = sys.argv[1]
output_file = sys.argv[2]
input_strings = []

def read_input_data():
    """
        Reads input data.
    """
    global input_strings
    file_handle = open(input_file, 'r')
    input_strings = file_handle.readlines()


def process_data():
    """
        Processes input data
    """
    hamming_distance = 0
    ntides1 = input_strings[0].strip()
    ntides2 = input_strings[1].strip()
    for ntide1, ntide2 in zip(ntides1, ntides2):
        if ntide1 != ntide2: hamming_distance = hamming_distance + 1
    with open(output_file, 'w') as outfile:
        outfile.write(str(hamming_distance) + "\n") 

def main():
    read_input_data()
    process_data()

if __name__ == "__main__":
    main()
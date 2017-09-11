"""
    Answer to question 3
"""
import sys

ADENINE = "A"
CYTOSINE = "C"
GUANINE = "G"
THYMINE = "T"
COMPLEMENT_MAP = {ADENINE:THYMINE, THYMINE:ADENINE, CYTOSINE: GUANINE, GUANINE:CYTOSINE}

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


def process_data():
    """
        Processes input data
    """
    global input_string
    input_string = input_string[::-1]
    output_string = ""
    for nucelotide in input_string:
        output_string = output_string + COMPLEMENT_MAP[nucelotide]
    print output_string

def main():
    read_input_data()
    process_data()

if __name__ == "__main__":
    main()
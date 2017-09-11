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
    input_string = input_string.strip()


def process_data():
    """
        Processes input data
    """
    global input_string
    input_string = input_string[::-1]
    output_string = ""
    for nucelotide in input_string:
        output_string = output_string + COMPLEMENT_MAP[nucelotide]
    with open(output_file, 'w') as outfile:
        outfile.write(str(output_string) + "\n")

def main():
    read_input_data()
    process_data()

if __name__ == "__main__":
    main()
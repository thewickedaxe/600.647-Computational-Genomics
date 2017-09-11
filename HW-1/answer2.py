"""
    Answer to question 2
"""
import sys

ADENINE = "A"
CYTOSINE = "C"
GUANINE = "G"
THYMINE = "T"
UNKNOWNSINE = "U"

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
    with open(output_file, 'w') as outfile:
        outfile.write(str(input_string.replace(THYMINE, UNKNOWNSINE)) + "\n")


def main():
    read_input_data()
    process_data()

if __name__ == "__main__":
    main()
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


def process_data():
    """
        Processes input data
    """
    print input_string
    print input_string.replace(THYMINE, UNKNOWNSINE)


def main():
    read_input_data()
    process_data()

if __name__ == "__main__":
    main()
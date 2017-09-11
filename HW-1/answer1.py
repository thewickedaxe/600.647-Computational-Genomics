"""
    Answer to question 1
"""
import sys

ADENINE = "A"
CYTOSINE = "C"
GUANINE = "G"
THYMINE = "T"

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
    print str(input_string.count(ADENINE)) + " " + str(input_string.count(CYTOSINE)) + " " + str(input_string.count(GUANINE)) + " " + str(input_string.count(THYMINE))


def main():
    read_input_data()
    process_data()

if __name__ == "__main__":
    main()
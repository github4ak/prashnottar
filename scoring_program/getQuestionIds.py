import sys
import re


def main(argv):

    output_filename = "question_ids.txt"

    # Read the answer file
    with open(argv[0], 'r') as f:
        input_file_contents = f.readlines()

    question_ids = []

    for line in input_file_contents:
        if line.__contains__("QuestionID"):
            question_ids.append(line.rstrip().split(":")[1].strip())

    output_file_content = ""

    for q in question_ids:
        output_file_content += str(q) + "\n"

    # Clear the file
    open(output_filename, "w").close()

    # Write the output
    with open(output_filename, "a") as f3:
        f3.write(output_file_content.rstrip())


if __name__ == "__main__":
    main(sys.argv[1:])

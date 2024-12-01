import argparse
from lexer.lexer import lexer
from parser.parser import SyntaxParser


def setup_argument_parser():
    """
    Sets up and returns the argument parser for the script.
    """
    parser = argparse.ArgumentParser(description="Process a file and output its contents.")
    parser.add_argument('file_path', type=str, help='Path to the file to be read')
    return parser


def read_file(file_path: str) -> str:
    """
    Reads the contents of a file and prints them out. Handles file-related exceptions.

    :param file_path: Path to the file to be read.
    """
    try:
        with open(file_path, 'r') as file_handle:
            file_contents = file_handle.read()
        return file_contents
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as error:
        print(f"An error occurred: {error}")


def main():
    """
    Main function that serves as the entry point of the script and parses command-line arguments.
    """
    parser = setup_argument_parser()
    arguments = parser.parse_args()
    file = read_file(arguments.file_path)

    tokens = lexer(file)

    syntax_parser = SyntaxParser(tokens)
    ast = syntax_parser.parse()

    print(ast)

if __name__ == "__main__":
    main()

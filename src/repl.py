import readline

import pyparsing.exceptions

import execute
import parse


def main():
    parser = parse.Parser()
    executor = execute.Executor()

    while True:
        line = input(" > ")

        if line == "exit":
            return

        try:
            print(executor.exec(parser.parse(line)).value)
        except (SyntaxError, pyparsing.exceptions.ParseBaseException) as e:
            print(e)


if __name__ == "__main__":
    main()

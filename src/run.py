import argparse

import pyparsing.exceptions

import execute
import parse


def main(args: argparse.Namespace):
    """Execute the mira file."""
    parser = parse.Parser()
    executor = execute.Executor()

    with open(args.filename, "r", encoding="utf-8") as f:
        mira_file = f.read()

    try:
        executor.exec(parser.parse(mira_file))
    except (SyntaxError, pyparsing.exceptions.ParseBaseException) as e:
        print(e)


if __name__ == "__main__":
    _argparser = argparse.ArgumentParser()
    _argparser.add_argument("filename")
    _args = _argparser.parse_args()
    main(_args)

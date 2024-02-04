import argparse
from typing import Any

from lsprotocol import types as lsp
import pygls.server

server = pygls.server.LanguageServer("example-server", "v0.1")


def log(message: Any, logfile: str = "/home/joshua/mira-lsp-logfile"):
    with open(logfile, "a") as f:
        f.write(repr(message))
        f.write("\n")


@server.feature(
    lsp.TEXT_DOCUMENT_COMPLETION, lsp.CompletionOptions(trigger_characters=["."])
)
def completions(params: lsp.CompletionParams):
    items = []
    document = server.workspace.get_document(params.text_document.uri)
    current_line = document.lines[params.position.line].strip()
    log(current_line)
    if current_line.endswith("hello."):
        items = [
            lsp.CompletionItem(label="world"),
            lsp.CompletionItem(label="friend"),
        ]
    return lsp.CompletionList(
        is_incomplete=False,
        items=items,
    )


def add_arguments(parser: argparse.ArgumentParser):
    parser.description = "Mira Language Server"

    parser.add_argument("--tcp", action="store_true", help="Use TCP server")
    parser.add_argument("--ws", action="store_true", help="Use WebSocket server")
    parser.add_argument("--host", default="127.0.0.1", help="Bind to this address")
    parser.add_argument("--port", type=int, default=2087, help="Bind to this port")


def main():
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    args = parser.parse_args()

    if args.tcp:
        server.start_tcp(args.host, args.port)
    elif args.ws:
        server.start_ws(args.host, args.port)
    else:
        server.start_io()


if __name__ == "__main__":
    main()

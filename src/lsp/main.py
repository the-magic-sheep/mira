import argparse
from typing import Any

from lsprotocol import types as lsp
import pygls.server

import parse

LOGFILE = "/home/joshua/mira-lsp-logfile"

server = pygls.server.LanguageServer("example-server", "v0.1")
modules: dict[str, "Module"] = {}
parser = parse.Parser()


with open(LOGFILE, "w") as f:
    f.write("LSP Started.")


def log(message: Any, logfile: str = LOGFILE):
    with open(logfile, "a") as f:
        f.write(repr(message))
        f.write("\n")


def file_uri_to_path(uri: str):
    if uri.startswith("file://"):
        uri = uri[7:]

    return uri


class Module:
    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content
        self.ast = parser.parse(content)


log("created server feature")


@server.feature(lsp.TEXT_DOCUMENT_DID_OPEN)
def load_new(params: lsp.DidOpenTextDocumentParams):
    uri = params.text_document.uri
    text = params.text_document.text
    log("Opened File: " + file_uri_to_path(uri))
    log(text)
    modules[uri] = Module(uri, text)


@server.feature(
    lsp.TEXT_DOCUMENT_COMPLETION, lsp.CompletionOptions(trigger_characters=["."])
)
def completions(params: lsp.CompletionParams):
    items = []
    document = server.workspace.get_document(params.text_document.uri)
    current_line = document.lines[params.position.line].strip()
    log("Completion Requested: " + current_line)
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

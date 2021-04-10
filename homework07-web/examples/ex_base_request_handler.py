from httpserver import EchoRequestHandler, TCPServer


def main():
    server = TCPServer(
        timeout=10, port=5000, backlog_size=1, request_handler_cls=EchoRequestHandler
    )
    server.serve_forever()


if __name__ == "__main__":
    main()

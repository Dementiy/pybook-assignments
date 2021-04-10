from httpserver import BaseHTTPRequestHandler, HTTPServer


def main():
    server = HTTPServer(port=5000, backlog_size=1, request_handler_cls=BaseHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()

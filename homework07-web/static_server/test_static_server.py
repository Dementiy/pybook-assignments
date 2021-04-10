import socket
import textwrap
import unittest

import requests


class TestStaticHTTPServer(unittest.TestCase):
    host = "http://localhost"
    port = 5000

    def setUp(self):
        pass

    def test_empty_request(self):
        """Send empty request"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", self.port))
        s.sendall(b"")
        s.close()

    def test_connection_timeout(self):
        """Connection timeout"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", self.port))
        s.settimeout(5)
        s.sendall(b"")
        data = s.recv(1024)
        s.close()
        self.assertIn(b"HTTP/1.1 400 Bad Request\r\n", data)

    def test_bad_request(self):
        """Bad request"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", self.port))
        s.sendall(b"PUSH / HTTP/1.1\r\n\r\n")
        data = s.recv(1024)
        s.close()
        self.assertIn(b"HTTP/1.1 400 Bad Request\r\n", data)

    def test_server_header(self):
        """Server header exists"""
        r = requests.get(f"{self.host}:{self.port}")
        server = r.headers.get("Server")
        self.assertIsNotNone(server)

    def test_date_header(self):
        """Date header exists"""
        r = requests.get(f"{self.host}:{self.port}")
        date = r.headers.get("Date")
        self.assertIsNotNone(date)

    def test_directory_index(self):
        """Directory index file exists"""
        # fmt: off
        expected_data = textwrap.dedent("""
        <!doctype html>
        <html>
          <head><title>Index page</title></head>
          <body><p>Hello from static server!</p></body>
        </html>
        """).strip()
        # fmt: on
        r = requests.get(f"{self.host}:{self.port}")
        data = r.content.decode()
        length = r.headers.get("Content-Length")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(int(length), 119)
        self.assertEqual(data, expected_data)

    def test_index_not_found(self):
        """Directory index file absent"""
        r = requests.get(f"{self.host}:{self.port}/dir/")
        self.assertEqual(int(r.status_code), 404)

    def test_file_not_found(self):
        """Absent file returns 404"""
        r = requests.get(f"{self.host}:{self.port}/404.html")
        self.assertEqual(int(r.status_code), 404)

    def test_file_in_nested_folders(self):
        """File located in nested folders"""
        r = requests.get(f"{self.host}:{self.port}/dir1/dir2/dir3/quote.txt")
        data = r.content
        length = r.headers.get("Content-Length")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(int(length), 62)
        self.assertEqual(len(data), 62)
        self.assertEqual(
            data.decode(), "Would you tell me, please, which way I ought to go from here?\n"
        )

    def test_file_with_slash(self):
        """Slash after filename"""
        # fmt: off
        expected_data = textwrap.dedent("""
        <!doctype html>
        <html>
          <head><title>Index page</title></head>
          <body><p>Hello from static server!</p></body>
        </html>
        """).strip()
        # fmt: on
        r = requests.get(f"{self.host}:{self.port}/index.html/")
        data = r.content.decode()
        length = r.headers.get("Content-Length")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(int(length), 119)
        self.assertEqual(data, expected_data)

    def test_file_with_query_string(self):
        """Query string after filename"""
        # fmt: off
        expected_data = textwrap.dedent("""
        <!doctype html>
        <html>
          <head><title>Index page</title></head>
          <body><p>Hello from static server!</p></body>
        </html>
        """).strip()
        # fmt: on
        r = requests.get(f"{self.host}:{self.port}/index.html?arg1=value&arg2=value")
        data = r.content.decode()
        length = r.headers.get("Content-Length")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(int(length), 119)
        self.assertEqual(data, expected_data)

    def test_file_with_spaces(self):
        """Filename with spaces"""
        r = requests.get(f"{self.host}:{self.port}/space%20in%20name.txt")
        data = r.content
        length = r.headers.get("Content-Length")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(int(length), 19)
        self.assertEqual(len(data), 19)
        self.assertEqual(data.decode(), "letters and spaces\n")

    def test_file_urlencoded(self):
        """Urlencoded filename"""
        # fmt: off
        expected_data = textwrap.dedent("""
        <!doctype html>
        <html>
          <head><title>Index page</title></head>
          <body><p>Hello from static server!</p></body>
        </html>
        """).strip()
        # fmt: on
        r = requests.get(f"{self.host}:{self.port}/%69%6E%64%65%78%2e%68%74%6d%6c")
        data = r.content.decode()
        length = r.headers.get("Content-Length")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(int(length), 119)
        self.assertEqual(data, expected_data)

    def test_document_root_escaping(self):
        """Document root escaping forbidden"""
        r = requests.get(f"{self.host}:{self.port}/../passwd")
        self.assertIn(r.status_code, (400, 403, 404))

    def test_file_with_dot_in_name(self):
        """File with two dots in name"""
        r = requests.get(f"{self.host}:{self.port}/dir1/dot..txt")
        data = r.content.decode()
        length = r.headers.get("Content-Length")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(int(length), 5)
        self.assertEqual(len(data), 5)
        self.assertEqual("hello", data)

    def test_head_method(self):
        """Head method support"""
        r = requests.head(f"{self.host}:{self.port}/index.html")
        self.assertEqual(r.status_code, 200)
        data = r.content.decode()
        self.assertEqual(len(data), 0)
        content_type = r.headers.get("Content-Type")
        self.assertEqual(content_type, "text/html")

    def test_method_not_allowed(self):
        """Method not allowed"""
        r = requests.post(f"{self.host}:{self.port}/index.html")
        self.assertEqual(r.status_code, 405)
        allow = r.headers.get("Allow")
        self.assertEqual(allow, "GET, HEAD")

    def test_filetype_html(self):
        """Content-Type for .html"""
        r = requests.get(f"{self.host}:{self.port}/index.html")
        self.assertEqual(r.status_code, 200)
        ctype = r.headers.get("Content-Type")
        self.assertEqual(ctype, "text/html")

    def test_filetype_png(self):
        """Content-Type for .png"""
        r = requests.get(f"{self.host}:{self.port}/kitano.png")
        self.assertEqual(r.status_code, 200)
        ctype = r.headers.get("Content-Type")
        self.assertEqual(ctype, "image/png")


loader = unittest.TestLoader()
suite = unittest.TestSuite()
a = loader.loadTestsFromTestCase(TestStaticHTTPServer)
suite.addTest(a)


class NewResult(unittest.TextTestResult):
    def getDescription(self, test):
        doc_first_line = test.shortDescription()
        return doc_first_line or ""


class NewRunner(unittest.TextTestRunner):
    resultclass = NewResult


runner = NewRunner(verbosity=2)
runner.run(suite)

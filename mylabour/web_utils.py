
import urllib
import unittest
import subprocess
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer


class TemproraryHttpServer:
    """
    A simpe, temprorary http web server on the pure Python 3.
    It has features for processing pages with a XML or HTML content.
    """

    PORT = 7000

    class HTTPServerRequestHandler(BaseHTTPRequestHandler):
        """
        An handler of request for the server, hosting XML-pages.
        """

        def do_GET(self):
            """Handle GET requests"""

            # response from page
            self.send_response(200)

            # set up headers for pages
            content_type = 'text/{0}'.format(page_content_type)
            self.send_header('Content-type', content_type)
            self.end_headers()

            # writing data on a page
            self.wfile.write(bytes(raw_data, encoding='utf'))

            return

    def __init__(self, page_content_type, *args, **kwargs):

        if page_content_type not in ['html', 'xml']:
            raise ValueError('This server can serve only HTML or XML pages.')

        self.page_content_type = page_content_type

    def __call__(self, raw_data):

        # keep passed data
        self.raw_data = raw_data

        # kill a process, hosted on a localhost:PORT
        self._kill_used_port()

        # run a server
        self.run_http_webserver()

    def run_http_webserver(self):

        # 'Started creating a temprorary http server.
        server_address = ('127.0.0.1', self.PORT)

        self.HTTPServerRequestHandler = self.HTTPServerRequestHandler
        httpd = HTTPServer(server_address, self.HTTPServerRequestHandler)

        # run a temprorary http server
        httpd.serve_forever()

        # open in a browser URL and see a result
        url = 'http://127.0.0.1:{0}'.format(self.PORT)
        webbrowser.open(url)

    def _kill_used_port(self):
        subprocess.call(['fuser', '-k', '{0}/tcp'.format(self.PORT)])


class TemproraryHttpServerTest(unittest.TestCase):

    def setUp(self):
        self.html_raw_data = """
        <!DOCTYPE html>
        <html>
        <head>
        <title>Page Title</title>
        </head>
        <body>
        <h1>This is a Heading</h1>
        <p>This is a paragraph.</p>
        </body>
        </html>
        """

        self.xml_raw_data = """
        <note>
        <to>Tove</to>
        <from>Jani</from>
        <heading>Reminder</heading>
        <body>Don't forget me this weekend!</body>
        </note>
        """

    def test_succefull_request_to_xml_page(self):
        page_content_type = 'xml'
        TemproraryHttpServer(page_content_type)(self.xml_raw_data)
        urllib.urlopen()


if __name__ == '__main__':
    unittest.main()

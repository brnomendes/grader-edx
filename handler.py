from http.server import BaseHTTPRequestHandler
from grader import Grader


class Handler(BaseHTTPRequestHandler):

    def do_POST(self):
        body_len = int(self.headers.get('content-length', 0))
        body_content = self.rfile.read(body_len).decode()
        result = Grader().run(body_content)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(result)

from datetime import datetime
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

data = {'result': 'this is a test'}
host = ('localhost', 8001)


class Request(BaseHTTPRequestHandler):
    def do_POST(self):
        req_body = self.rfile.read(int(self.headers["Content-Length"])).decode()
        print("req_body: " + req_body)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())


# 测试收到的报文
if __name__ == '__main__':
    server = HTTPServer(host, Request)
    print('Start: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()

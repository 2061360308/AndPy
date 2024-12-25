import sys
import socketserver
from http.server import SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from . import DIRECTORY, routes, PORT


class HttpRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # 解析 URL 并获取查询参数
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        self.path = path

        # 查找路由并调用相应的处理函数
        if path in routes['GET']:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = routes['GET'][path](query)
            self.wfile.write(response.encode('utf-8'))
        else:
            if self.path == '/':
                self.path = './index.html'
            return super().do_GET()

    def do_POST(self):
        # 解析 URL 并获取查询参数
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        self.path = path

        # 查找路由并调用相应的处理函数
        if path in routes['POST']:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = routes['POST'][path](data)
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')  # 添加CORS头
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def log_message(self, format, *args):
        # 使用 sys.__stdout__.write 进行日志输出
        sys.__stdout__.write(f"{self.address_string()} - - [{self.log_date_time_string()}] {format % args}\n")


handler = HttpRequestHandler


def start_server():
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        sys.__stdout__.write(f"Serving HTTP on port {PORT}\n")
        httpd.serve_forever()

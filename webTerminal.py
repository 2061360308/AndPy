import sys

client_types = ['web', 'terminal']  # 客户端类型 网页端和终端


class WebTerminalIo:
    def __init__(self):
        pass

    def start(self):
        pass

    def send(self, data):
        pass

    def recv(self):
        pass

    def close(self):
        pass


class WebTerminal:
    def __init__(self):
        self.websocket_server = None
        self.io = WebTerminalIo

        sys.stdin = self.io
        sys.stdout = self.io
        sys.stderr = self.io


class TerminalServer:
    def __init__(self):
        self.terminals = []
        self.websocket_server = None
        self.output_buffer = {}  # 输出缓冲区
        self.input_buffer = {}  # 输入缓冲区

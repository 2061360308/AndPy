"""
维护WebSocket服务器
连接并管理多个终端，连接前端交互
"""
import asyncio
import sys
from enum import Enum

import unicodedata
import websockets

from tools import Buffer

HOST = "localhost"
PORT = 8765

DEBUG = False

script_items = [
    {
        'name': '超星学习通自动刷课脚本',
        'icon': './images/python.jpg',
        'website': 'chaoxing.com'
    },
    {
        'name': 'B站视频自动刷弹幕脚本',
        'icon': './images/python.jpg',
        'website': 'bilibili.com'
    },
    {
        'name': '起点自动签到脚本',
        'icon': './images/python.jpg',
        'website': 'qidian.com'
    },
]


class DeviceType(Enum):
    WEB = 1
    TERMINAL = 2

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


class Terminal:
    def __init__(self, _id):
        self._id = _id
        self.input_buffer = Buffer()
        self.output_buffer = Buffer()

        self.accepting_input = False

    def write(self, message):
        """
        产生消息，发送给Web设备显示或存入输出缓存
        """
        # 发送消息给Web设备显示
        if self._id in TerminalManager.web_connections.keys():
            web_device = TerminalManager.web_connections[self._id]
            # asyncio.run(web_device.send(message))
            asyncio.create_task(web_device.send(message))  # 调度异步操作
        else:
            # 未找到Web设备，存入输出缓存
            self.output_buffer.write(message)

    def readline(self):
        """
        读取一行输入
        """
        self.input_buffer.clear()
        self.accepting_input = True
        while True:
            if '\r\n' in self.input_buffer.look():
                self.accepting_input = False
                return self.input_buffer.read()

    def read(self):
        if DEBUG:
            sys.__stdout__.write('[CustomIO] Waiting for input...\n')

    def flush(self):
        if DEBUG:
            sys.__stdout__.write('[CustomIO] Flushing...\n')
        pass

    async def handle(self, websocket, con_type, message):
        """
        处理消息
        websocket: WebSocket连接
        con_type: 连接类型
        message: 消息
        """
        if con_type == DeviceType.WEB.value:
            # Web界面发来用户输入的消息

            response = ''

            for char in message:
                if ord(char) == 13:  # 判断是否是回车键
                    self.accepting_input = True
                    response += '\r\n'
                    self.input_buffer.write('\n')
                elif ord(char) == 127:  # 判断是否是退格键
                    print("backspace")
                    last_char = self.input_buffer.look_last(1)
                    print(f"Last char:{last_char}")
                    if last_char:
                        if unicodedata.east_asian_width(last_char) in 'WF':
                            response += '\b \b\b'
                        else:
                            response += '\b \b'
                    self.input_buffer.read_last(1)  # 从输入缓冲区删除一个字符
                else:
                    response += char
                    self.input_buffer.write(char)

            self.write(response)

            print(f"Input buffer: {self.input_buffer.buffer}")
        else:
            # 终端发来的消息
            self.write(message)


async def websocket_callback(websocket):
    """
    处理新的WebSocket连接
    """

    self = TerminalManager()

    # 解析path /DeviceType/ID
    path = websocket.request.path
    con_type, con_id = path.replace('\\', '/').strip('/').split('/')
    con_type = int(con_type)

    # 判断连接类型和ID是否有效
    if not (DeviceType.has_value(con_type) and con_id):
        return

    # 记录对象
    if con_type == DeviceType.WEB.value:
        if con_id not in self.web_connections.keys():
            self.web_connections[con_id] = websocket
    elif con_type == DeviceType.TERMINAL.value:
        if con_id not in self.program_connections.keys():
            self.program_connections[con_id] = websocket

    try:
        # 记录连接并处理客户端消息
        async for message in websocket:
            terminal = self.terminals[con_id]
            await terminal.handle(websocket, con_type, message)

    except websockets.ConnectionClosed:
        print(f"Client {con_id} | Type: {con_type} disconnected")
    finally:
        # 移除断开的客户端
        if con_type == DeviceType.WEB:
            self.web_connections.pop(con_id)
        elif con_type == DeviceType.TERMINAL:
            self.program_connections.pop(con_id)


class TerminalManager:
    _instance = None

    program_connections = {}  # 程序连接的字典 {id: Terminal}
    web_connections = {}  # Web连接的字典 {id: Web}
    interface_connections = {}  # 接口连接的字典 {id: Interface}

    terminals = {}  # 终端实例的字典 {id: Terminal}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            print(f"WebSocket Server started at ws://{HOST}:{PORT}")
            asyncio.run(self.start_server())

    async def start_server(self):
        async with websockets.serve(websocket_callback, HOST, PORT) as server:
            await server.serve_forever()


if __name__ == '__main__':
    print(f"WebSocket Server started at ws://{HOST}:{PORT}")
    TerminalManager()

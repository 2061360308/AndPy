
class Buffer:
    """
    模拟维护一个缓冲区，用于存储终端的输入输出
    """

    def __init__(self, max_size=1024):
        self.max_size = max_size
        self.current_size = 0
        self.buffer = ""

    def write(self, data):
        data_size = len(data.encode('utf-8'))
        while self.current_size + data_size > self.max_size:
            self._remove_oldest()
        self.buffer += data
        self.current_size += data_size

    def read(self, size=None):
        if size is None or size > self.current_size:
            size = self.current_size
        data = self.buffer[:size]
        self.buffer = self.buffer[size:]
        self.current_size -= len(data.encode('utf-8'))
        return data

    def look(self, size=None):
        if size is None or size > self.current_size:
            size = self.current_size
        data = self.buffer[:size]
        return data

    def read_last(self, size=None):
        if size is None or size > self.current_size:
            size = self.current_size
        data = self.buffer[-size:]
        self.buffer = self.buffer[:-size]
        self.current_size -= len(data.encode('utf-8'))
        return data

    def look_last(self, size=None):
        if size is None or size > self.current_size:
            size = self.current_size
        data = self.buffer[-size:]
        return data

    def _remove_oldest(self):
        if self.buffer:
            # 移除最旧的一个字符
            oldest_data = self.buffer[0]
            self.buffer = self.buffer[1:]
            self.current_size -= len(oldest_data.encode('utf-8'))

    def clear(self):
        self.buffer = ""
        self.current_size = 0

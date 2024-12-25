from . import route


@route('GET', '/hello')
def hello(query):
    return '{"message": "Hello, world!"}'


@route('POST', '/goodbye')
def goodbye(data):
    return '{"message": "Goodbye, world!"}'

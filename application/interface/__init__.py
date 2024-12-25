from config import DEBUG, INTERFACE_PORT, INTERFACE_DIRECTORY

PORT = INTERFACE_PORT
DIRECTORY = INTERFACE_DIRECTORY

# 路由表
routes = {
    'GET': {},
    'POST': {}
}


# 路由装饰器
def route(method, path):
    def decorator(func):
        routes[method][path] = func
        return func

    return decorator

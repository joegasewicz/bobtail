class Request:
    path: str
    method: str

    def __init__(self, path: str, method: str):
        self.path = path
        self.method = method

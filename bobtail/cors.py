from bobtail import Request, Response
from bobtail.middleware import AbstractMiddleware, Tail


class BobtailCors(AbstractMiddleware):

    def __init__(self):
        pass

    def init(self, req: Request, res: Response, tail: Tail) -> None:
        res.set_headers({
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Authorization, Content-Type",
            "Access-Control-Allow-Methods": "GET,POST,DELETE,PUT",
        })
        print(f"CORS MIDDLEWARE")
        tail(req, res)


class BobtailLogger(AbstractMiddleware):

    def __init__(self):
        pass

    def init(self, req: Request, res: Response, tail: Tail) -> None:
        print(f"LOGGING MIDDLEWARE")
        tail(req, res)

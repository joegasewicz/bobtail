#'QUERY_STRING': 'name=joe&age=48', 'RAW_URI': '/posts?name=joe&age=48'

mock_environ = {
    'wsgi.errors': '<gunicorn.http.wsgi.WSGIErrorsWrapper object at 0x102260d30>',
    'wsgi.version': (1, 0),
    'wsgi.multithread': False,
    'wsgi.multiprocess': False,
    'wsgi.run_once': False,
    'wsgi.file_wrapper': "<class 'gunicorn.http.wsgi.FileWrapper'>",
    'wsgi.input_terminated': True,
    'SERVER_SOFTWARE': 'gunicorn/20.1.0',
    'wsgi.input': "<gunicorn.http.body.Body object at 0x102274490>",
    'gunicorn.socket': "<socket.socket fd=9, family=2, type=1, proto=0, laddr=('127.0.0.1', 8000), raddr=('127.0.0.1', 56963)>",
    'REQUEST_METHOD': 'GET',
    'QUERY_STRING': '',
    'RAW_URI': '/',
    'SERVER_PROTOCOL': 'HTTP/1.1',
    'HTTP_HOST': '127.0.0.1:8000',
    'HTTP_CONNECTION': 'keep-alive',
    'HTTP_CACHE_CONTROL': 'max-age=0',
    'HTTP_UPGRADE_INSECURE_REQUESTS': '1',
    'HTTP_USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'HTTP_SEC_GPC': '1',
    'HTTP_ACCEPT_LANGUAGE': 'en-GB,en',
    'HTTP_SEC_FETCH_SITE': 'none',
    'HTTP_SEC_FETCH_MODE': 'navigate',
    'HTTP_SEC_FETCH_USER': '?1',
    'HTTP_SEC_FETCH_DEST': 'document',
    'HTTP_ACCEPT_ENCODING': 'gzip, deflate, br',
    'HTTP_COOKIE': 'my_cookie=some_value',
    'wsgi.url_scheme': 'http',
    'REMOTE_ADDR': '127.0.0.1',
    'REMOTE_PORT': '56963',
    'SERVER_NAME': '127.0.0.1',
    'SERVER_PORT': '8000',
    'PATH_INFO': '/',
    'SCRIPT_NAME': '',
}

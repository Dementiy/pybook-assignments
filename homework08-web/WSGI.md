**Что такое WSGI?**

WSGI (Web Server Gateway Interface) это не сервер, не модуль python, не фреймворк, это спецификация интерфейса взаимодействия сервера и веб-приложения. Подробное изложение спецификации как для сервера, так и для приложения можно найти в [PEP 3333](https://www.python.org/dev/peps/pep-3333/).

Установим два популярных WSGI-сервера:

```sh
$ pip install gunicorn
$ pip install uwsgi
```

Установим два микро фреймворка:

```sh
$ pip install falcon
$ pip install bottle
```

Пример приолжения из документации фреймворка falcon:

```python
import falcon

class QuoteResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        quote = {
            'quote': (
                "I've always been more interested in "
                "the future than in the past."
            ),
            'author': 'Grace Hopper'
        }
        resp.media = quote

app = falcon.App()
app.add_route('/quote', QuoteResource())
```

```sh
$ gunicorn falcon_quotes:app
$ uwsgi --http :8000 --wsgi-file falcon_quotes.py  --callable app
```

Аналогично для bottle:

```python
from bottle import route, template

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

import bottle
app = bottle.default_app()
```

```sh
$ gunicorn bottle_hello:app
$ uwsgi --http :8000 --wsgi-file bottle_hello.py  --callable app
```

<img src="https://ruslanspivak.com/lsbaws-part2/lsbaws_part2_wsgi_interop.png" style="zoom: 67%;" />

См. https://ruslanspivak.com/lsbaws-part2/

**Интерфейс приложения**

WSGI-приложение должно быть вызываемым (callable) объектом, то есть функцией или классом с переопределенным методом `__call__`. В качестве аргуметов при вызове передаются: словарь с [переменными окружения](https://www.python.org/dev/peps/pep-3333/#environ-variables) и функция-callback, которая будет вызвана приложением, чтобы передать на сервер статус ответа и заголовки (третий, необязательный параметр `exc_info` должен использоваться только при обработке ошибок и должен быть кортежем, который возвращает функция `sys.exc_info()`). Возвращаемым значением является тело ответа, которое должно быть представлено итерируемым объектом со строками в качестве элементов. Давайте рассмотрим простой пример:

```python
def application(environ, start_response):
    status = "200 OK"
    response_body = "Hello World!".encode()
    response_headers = [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(response_body))),
    ]
    start_response(status, response_headers)
    return [response_body]
```

```sh
$ gunicorn simple_app:application
```

В python есть уже готовая реализация простого WSGI-сервера:

```python
from wsgiref.simple_server import make_server

def application(...):
    # ...

if __name__ == "__main__":
    server = make_server("localhost", 8000, application)
    # обработать только один запрос
    server.handle_request()
```

**Задание**

Вашей задачей является реализовать WSGI-сервер, который бы позволил запускать существующие синхронные WSGI-фреймворки.

```python
# request.py
@dataclasses.dataclass
class WSGIRequest(HTTPRequest):
    def to_environ(self) -> tp.Dict[str, tp.Any]:
        environ = {}
        # Тут надо наполнить словарик данными
        return environ
```

Переменные словаря environ:

- `REQUEST_METHOD` - HTTP-метод запроса, например, GET/HEAD/POST и т.п.
- `SCRIPT_NAME`
- `PATH_INFO` - запрашиваемый ресурс
- `QUERY_STRING` - строка запроса (то что следует после знака `?`, например, `a=1&b=2`)
- `CONTENT_TYPE` - заголовок `Content-Type` из запроса
- `CONTENT_LENGTH` - заголовок `Content-Length` из запроса
- `SERVER_NAME` и `SERVER_PORT` - адрес сервера
- `SERVER_PROTOCOL` - версия протокола который использует клиент для посылки запроса, например "HTTP/1.0", или "HTTP/1.1"
- `HTTP_Variables` - переменные соответствующие заголовкам запроса переданным клиентом

- `wsgi.version` - кортеж (1, 0) из пары значений представляющий собой версию WSGI
- `wsgi.url_scheme` - строка представляющая схему из URL, обычно "http", или "https"
- `wsgi.input` - объект похожий на файл, из которого может быть прочитано тело запроса
- `wsgi.errors` - объект похожий на файл, в который приложение может выводить сообщения об ошибках
- `wsgi.multithread` - True если объект приложения может быть одновременно вызван из нескольких потоков
- `wsgi.multiprocess` - True если соответствующие объекты приложения могут быть одновременно вызваны в нескольких процессах
- `wsgi.run_once` - True если сервер предполагает (но не гарантирует), что приложение будет вызвано только один раз во время жизни текущего процесса

```python
# response.py
@dataclasses.dataclass
class WSGIResponse(HTTPRequest):
    status: int = 200

    def start_response(self, status: str, response_headers: tp.List[tp.Tuple[str, str]], exc_info=None) -> None:
        pass
```

```python
# server.py
class WSGIServer(HTTPServer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.app: tp.Optional[ApplicationType] = None

    def set_app(self, app: ApplicationType) -> None:
        self.app = app

    def get_app(self) -> tp.Optional[ApplicationType]:
        return self.app


class WSGIRequestHandler(BaseHTTPRequestHandler):
    request_klass = WSGIRequest
    response_klass = WSGIResponse

    def handle_request(self, request: WSGIRequest) -> WSGIResponse:
        # сформировать словарь с переменными окружения
        # дополнить словарь информацией о сервере
        # вызвать приложение передав ему словарь с переменными окружения и callback'ом
        # ответ приложения представить в виде байтовой строки
        # вернуть объект класса WSGIResponse
        pass
```

**Пара слов об ASGI**

https://asgi.readthedocs.io/en/latest/introduction.html

```python
async def application(scope, receive, send):
    name = scope["path"].split("/", 1)[-1] or "world"
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [[b"content-type", b"text/plain"],],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": f"Hello, {name}!".encode(),
            "more_body": False,
        }
    )
```

```sh
$ uvicorn asgi-hello:application
```

https://florimond.dev/blog/articles/2019/08/introduction-to-asgi-async-python-web/

- Speed: the async nature of ASGI apps and servers make them [really fast](https://www.techempower.com/benchmarks/#section=data-r18&hw=ph&test=fortune&l=zijzen-f&w=zik0zh-zik0zj-e7&d=b) (for Python, at least) — we're talking about 60k-70k req/s (consider  that Flask and Django only achieve 10-20k in a similar situation).
- Features: ASGI servers and frameworks gives you access to inherently concurrent features (WebSocket, Server-Sent Events, HTTP/2) that are  impossible to implement using sync/WSGI.
- Stability: ASGI as a spec has been around for about 3 years now, and version 3.0 is considered very stable. Foundational parts of the  ecosystem are stabilizing as a result.


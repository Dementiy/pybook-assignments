### Задача 1

Вашей задачей является реализация простого in-memory хранилища по типу ключ-значение.
Ваш сервер должен уметь обрабатывать следущие запросы:

```python
import requests

host = "127.0.0.1"
port = 10000
address = f"http://{host}:{port}"

# d = {}
# d["a"] = 1
resp = requests.post(f"{address}", data={"a": 1}, headers={"content-type": "application/json"})
assert resp.status_code == 201

# d["b"] = 1
resp = requests.post(f"{address}", data={"b": 1}, headers={"content-type": "application/json"})
assert resp.status_code == 201

# d["a"] = 1 # Error
resp = requests.post(f"{address}", data={"a": 2}, headers={"content-type": "application/json"})
assert resp.status_code == 409

# d["a"] = 2 # Ok
resp = requests.put(f"{address}", data={"a": 2}, headers={"content-type": "application/json"})
assert resp.status_code == 200

# "a" in d # True
resp = requests.head(f"{address}/a")
assert resp.status_code == 200

# "c" in 1 # False
resp = requests.head(f"{address}/c")
assert resp.status_code == 404

# d["a"]
resp = requests.get(f"{address}/a")
assert resp.status_code == 200
assert resp.json() == {"value": 1}

# d["c"]
resp = requests.get(f"{address}/с")
assert resp.status_code == 404

# del d["a"]
resp = requests.delete(f"{address}/a")
assert resp.status_code == 200
```

На плохие запросы мы должны отвечать ошибкой `Bad Request`. Если есть ошибки в данных, то мы должны
уведомить пользователя `{"error": "описание ошибки"}`.

Для реализации вы должны использовать httpserver из первой работы и определить соответствующий класс-обработчик запросов:

```python
from httpserver import BaseHTTPRequestHandler, HTTPServer


class CacheRequestHandler(BaseHTTPRequestHandler):
    # ...


class CacheServer(HTTPServer):
    # ...
```


### Задача 2

Есть формат данных, который нужно научиться парсить в удобную структуру:

```
DATES
26 JUN 2021 /
/

KEYWORD
-- с двух тире начинается комментарий
ID1 V1 V2 3* V6 V7 / -- и комментарии могут быть
/ -- практически где угодно

DATES
27 JUN 2021 /
/

UNINTERESTING_KEYWORD -- могут быть и другие ключевые слова, но нас интересует только KEYWORD
ID V1 V2 /
/

-- на эту дату нет интересующих нас секций

DATES
28 JUN 2021 /
/

KEYWORD
ID1 V1 V2 3* V6 V7 /
/

KEYWORD
-- если у нас несколько секций на одну дату, то их имеет смысл объединить в одну
ID2 V1 V2 V3 V4 V5 V6 V7 /
ID1 V11 V22 1* V44 V5 V6 V7 /
ID3 V1 V2 2* V5 V6 V7 /
/

-- comment

END -- это конца значимой части данных

-- дальше данные могут быть, но они нас не интересуют
DATES
29 JUN 2021 /
/
```

Где `N*` означает, что следующие `N` параметров заполняются значениями по умолчанию.

В итоге хотим получить удобную структуру, которая бы позволяла нам делать запросы по дате и идентификатору:

```
26.06.2021:
    ID1 - [V1 V2 D3 D4 D5 V6 V7]
28.06.2021:
    ID1 - [V1 V2 D3 D4 D5 V6 V7, V11 V22 D3 V44 V5 V6 V7]
    ID2 - [V1 V2 V3 V4 V5 V6 V7]
    ID3 - [V1 V2 D3 D4 V5 V6 V7]
```

Также стараемся не упасть при парсинге, а распарсить как можно больше.
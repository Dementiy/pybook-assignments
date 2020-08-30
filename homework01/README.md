## Шаблоны заданий для [первой работы](https://dementiy.github.io/assignments/cypher/)

Автоматическое форматирование при помощи [black](https://github.com/psf/black):

```sh
$ black -l 100 caesar.py vigenere.py rsa.py
```

Автоматическая сортировка импортируемых модулей при помощи [isort](https://github.com/timothycrosley/isort):

```sh
$ isort caesar.py vigenere.py rsa.py
```

Проверить аннотации типов при помощи [mypy](https://github.com/python/mypy):

```sh
$ mypy caesar.py vigenere.py rsa.py
```

Запустить доктесты можно так:

```sh
$ python -m doctest caesar.py
$ python -m doctest vigenere.py
$ python -m doctest rsa.py
```

Запустить юнит-тесты с помощью модуля [unittest](https://docs.python.org/3/library/unittest.html) можно так:

```sh
$ python -m unittest discover
```

Или с помощью модуля [pytest](https://docs.pytest.org/en/stable/):

```sh
$ pytest tests/test_caesar.py
$ pytest tests/test_vigenere.py
$ pytest tests/test_rsa.py
```

Для запуска всех тестов:

```sh
$ pytest
```

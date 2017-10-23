Пример запуска тестов для шифра Цезаря (для остальных заданий запуск тестов аналогичен):

```
$ go test -v ./caesar
=== RUN   TestEncryptCaesar
--- PASS: TestEncryptCaesar (0.00s)
=== RUN   TestDecryptCaesar
--- PASS: TestDecryptCaesar (0.00s)
PASS
ok  _/homework01-go/caesar  0.010s
```

Запустить алгоритм RSA можно с помощью следующей команды:
```
$ go run main.go -p=11 -q=17 -text=very_secret
Encrypted message: [84 50 113 110 184 174 50 143 113 50 24]
Decrypted message: very_secret
```

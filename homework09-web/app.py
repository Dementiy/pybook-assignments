import datetime as dt
import json
import typing as tp

import jwt

from slowapi import JsonResponse, SlowAPI, Request
from slowapi.middlewares import CORSMiddleware

app = SlowAPI()
notes: tp.Dict[int, tp.Dict[str, tp.Any]] = {}

JWT_SECRET = "secret"
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 300


def dt_json_serializer(o):
    if isinstance(o, (dt.date, dt.datetime)):
        return o.isoformat()


@app.post("/api/jwt-auth/")
def login(request: Request) -> JsonResponse:
    user_data = request.json()
    users.add(user_data["email"])
    payload = {
        "email": user_data["email"],
        "exp": dt.datetime.utcnow() + dt.timedelta(seconds=JWT_EXP_DELTA_SECONDS),
    }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return JsonResponse(data={"token": jwt_token})


@app.post("/api/notes")
def add_note(request: Request) -> JsonResponse:
    note = request.json()
    note_id = len(notes) + 1
    note["id"] = note_id
    note["pub_date"] = dt.datetime.now()
    notes[note_id] = note
    return JsonResponse(data=note, serializer=dt_json_serializer)


@app.get("/api/notes")
def get_notes(request: Request) -> JsonResponse:
    notes_list = list(notes.values())
    return JsonResponse(data={"notes": notes_list}, serializer=dt_json_serializer)


@app.get("/api/notes/{id}")
def get_note(request: Request, id: int) -> JsonResponse:
    note_id = int(id)
    return JsonResponse(data=notes[note_id], serializer=dt_json_serializer)


@app.patch("/api/notes/{id}")
def update_note(request: Request, id: int) -> JsonResponse:
    note_id = int(id)
    data = request.json()
    note = notes[note_id]
    note["title"] = data["title"]
    note["body"] = data["body"]
    return JsonResponse(data={})


app.add_middleware(CORSMiddleware)


def main():
    # TODO: Добавить автоматическое приведение типов аргументов
    # TODO: Добавить авторизацию пользователей
    # TODO: Добавить обработку завершающего слеша

    from wsgiserver import WSGIRequestHandler, WSGIServer

    server = WSGIServer(port=8080, request_handler_cls=WSGIRequestHandler)
    server.set_app(app)
    server.serve_forever()


if __name__ == "__main__":
    main()

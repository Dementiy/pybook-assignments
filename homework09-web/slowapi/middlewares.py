from slowapi.response import Response, JsonResponse


class Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)


class CORSMiddleware(Middleware):
    def __call__(self, request):
        cors_headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
            "Access-Control-Allow-Methods": "GET,POST,PATCH,PUT,DELETE",
        }
        if request.method == "OPTIONS":
            return Response(200, body="", headers=cors_headers)
        else:
            response = self.get_response(request)
            response.headers.update(cors_headers)
            return response


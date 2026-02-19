class FirstMiddleware:
    def __init__(self, get_respone):
        self.get_response = get_respone

    def __call__(self, request):
        response = self.get_response(request)
        return response

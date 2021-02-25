class ChatbotException(Exception):
    def __init__(self, detail, status, title="Exception"):
        self.title = title
        self.detail = detail
        self.status = status

class InternalServerError(Exception):
    def __init__(self, detail='Request failed due to Internal Server Error'):
        self.title = "Internal Server Error"
        self.status = 500
        self.detail = detail
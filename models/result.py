class Result:

    def __init__(self, res, state, message, code):
        self.res = res
        self.state = state
        self.message = message
        self.code = code

    def get_message(self):
        return {"res": self.res, "status": {f"{self.state}: {self.message}"}, "code": self.code}
class RequestValidator:
    def __init__(self, request) -> None:
        self.request = request

    def fieldsIsNotEmpty(data, fields) -> bool:
        for field in fields:
            if not data[field]:
                return False
        
        return True

    def contain(self, fields) -> bool:
        for field in fields:
            if not field in self.request.data:
                return False
        
        return True

    def containNotEmpty(self, fields) -> bool:
        return self.contain(fields) and RequestValidator.fieldsIsNotEmpty(self.request.data, fields)
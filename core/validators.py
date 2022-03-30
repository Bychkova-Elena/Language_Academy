class RequestValidator:
    @staticmethod
    def checkFieldsInRequest(data, fields):
        for field in fields:
            if not field in data:
                return False
        
        return True
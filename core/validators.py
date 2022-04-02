class RequestValidator:
    def fieldsIsNotEmpty(data, fields) -> bool:
        for field in fields:
            if not data[field]:
                return False
        
        return True

    def contain(data, fields) -> bool:
        for field in fields:
            if not field in data:
                return False
        
        return True

    def containNotEmpty(data, fields) -> bool:
        return RequestValidator.contain(data=data, fields=fields) and RequestValidator.fieldsIsNotEmpty(data=data, fields=fields)
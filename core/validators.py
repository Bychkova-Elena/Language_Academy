class RequestValidator:
    @staticmethod
    def FieldsIsNotEmpty(data, fields) -> bool:
        for field in fields:
            if not data[field]:
                return False

        return True

    @staticmethod
    def Contain(data, fields) -> bool:
        for field in fields:
            if not field in data:
                return False

        return True

    @staticmethod
    def ContainNotEmpty(data, fields) -> bool:
        return (
            RequestValidator.Contain(data=data, fields=fields) and
            RequestValidator.FieldsIsNotEmpty(data=data, fields=fields)
        )

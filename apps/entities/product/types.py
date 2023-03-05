class UPC(int):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            upc_as_int = int(v)
        except ValueError:
            raise TypeError("UPC format error")
        if len(v.strip()) > 12:
            raise TypeError("UPC format error")
        return upc_as_int

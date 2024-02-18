class BaseException(SystemExit):
    def __init__(self, type, message):
        super().__init__(f"Error: {type}\nDetails: {message}")


class InvalidConfigFileException(BaseException):
    def __init__(self, message):
        super().__init__("Invalid Configuration", message)


class UnableToCreateNamespace(BaseException):
    def __init__(self, message):
        super().__init__("Unable to Create Namespace:", message)


class UnableToDeleteNamespace(BaseException):
    def __init__(self, message):
        super().__init__("Unable to Delete Namespace:", message)


class NamespaceAlreadyExists(BaseException):
    def __init__(self, message):
        super().__init__("Namespace Already Exists:", message)


class UnableToCreateInterface(BaseException):
    def __init__(self, message):
        super().__init__("Unable to Create Interface:", message)


class UnableToEditInterface(BaseException):
    def __init__(self, message):
        super().__init__("Unable to Edit Interface:", message)

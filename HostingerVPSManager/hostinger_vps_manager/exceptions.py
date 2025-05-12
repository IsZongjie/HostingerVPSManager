class HostingerAPIError(Exception):
    def __init__(self, code: int, message: str, raw_error: Exception = None):
        self.code = code
        self.message = message
        self.raw_error = raw_error
        super().__init__(f"Hostinger API错误 [{code}]: {message}")

    def __str__(self):
        return f"{self.code}: {self.message}"
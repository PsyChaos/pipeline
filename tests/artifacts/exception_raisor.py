class ExceptionRaiser:
    def handle(self, data, next):
        raise ValueError("Intentional error for testing")

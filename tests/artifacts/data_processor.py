class DataProcessor:
    def __init__(self, operation):
        self.operation = operation

    def handle(self, data, next):
        processed = self.operation(data)
        return next(processed)

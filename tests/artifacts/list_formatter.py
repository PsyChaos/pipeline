class ListFormatter:
    def __call__(self, items, next):
        formatted = [f"Item: {item}" for item in items]
        return next(formatted)

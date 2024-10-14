class StringManipulator:
    def process(self, string, next):
        return next(string.upper())

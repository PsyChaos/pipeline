class NumberMultiplier:
    def handle(self, number, next):
        return next(number * 2)

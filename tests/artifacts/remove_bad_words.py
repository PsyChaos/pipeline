class RemoveBadWords:
    def handle(self, content, next):
        return next(content.replace("badword", ""))

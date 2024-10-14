class ShortenUrls:
    def handle(self, content, next):
        return next(content.replace("http://", "https://short.ly/"))

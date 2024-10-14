from src.pipeline import Pipeline
from src.hub import Hub
from tests.artifacts.remove_bad_words import RemoveBadWords
from tests.artifacts.shorten_urls import ShortenUrls

class GenerateLinks:
    def process(self, content, next_func):
        processed_content = content.replace("content", "🔗 Link")
        return next_func(processed_content)
    
class FaultyPipe:
    def handle(self, content, next_func):
        raise ValueError("An error occurred!")
    
def error_handler(content, exception):
    print(f"Error handling content: {exception}")
    return "Default Content"

def main():
    hub = Hub()

    def process_message(pipeline, message):
        return (
            pipeline
            .send(message)
            .through([RemoveBadWords(), ShortenUrls()])
            .then_return()
        )

    hub.pipeline("message_processing", process_message)

    try:
        processed_message = hub.pipe("This is a test http://example.com with badword", "message_processing")
        print(processed_message)
    except ValueError as e:
        print(f"Error: {e}")

    try:
        hub.pipe("Some data", "non_existent_pipeline")
    except ValueError as e:
        print(f"Error: {e}")

    # Output 1: "This is a test https://short.ly/example.com with "
    # Output 2: "Error: Pipeline 'non_existent_pipeline' not found"
        
if __name__ == "__main__":
    main()
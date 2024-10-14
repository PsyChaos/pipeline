# Pipeline and Hub System

## Overview

This repository provides a flexible and customizable `Pipeline` class that allows for the sequential execution of various processing steps (pipes) on a given input. It is heavily inspired by Laravel's pipeline system and designed to handle complex workflows. Additionally, the `Hub` class manages multiple named pipelines, providing centralized access to pipeline instances.

## Features

- Chainable processing using pipes.
- Custom method invocation on each pipe.
- Conditional pipe inclusion via the `when` method.
- Failure handling with `on_failure` for exceptions.
- Ability to define and manage multiple pipelines using the `Hub` class.

## Usage

### Basic Pipeline Usage

The `Pipeline` class allows you to pass data through a series of "pipes", where each pipe processes the data in some way. Below is a basic usage example.

### Example:

```python
class RemoveBadWords:
    def handle(self, content, next_func):
        cleaned_content = content.replace("badword", "")

        return next_func(cleaned_content)

class ShortenUrls:
    def handle(self, content, next_func):
        shortened_content = content.replace("http://", "https://short.ly/")

        return next_func(shortened_content)

pipeline = Pipeline()

result = (
    pipeline
    .send("This is a test message with badword and a URL: http://example.com")
    .through([RemoveBadWords(), ShortenUrls()])
    .then_return()
)

print(result)
# Output: "This is a test message with  and a URL: https://short.ly/example.com"
```

### Pipeline with a Custom Method

By default, the `Pipeline` class calls the `handle` method on each pipe. However, you can specify a custom method using the `via` method.

```python
class GenerateLinks:
    def process(self, content, next_func):
        processed_content = content.replace("content", "🔗 Link")
        return next_func(processed_content)

pipeline = Pipeline()

result = (
    pipeline
    .send("This content contains links.")
    .via('process')  # Custom method for pipes
    .through([GenerateLinks()])
    .then_return()
)

print(result)
# Output: "This 🔗 Link contains links."
```

### Handling Exceptions

You can provide an `on_failure` callback that will be triggered if any of the pipes raise an exception. This allows you to gracefully handle errors.

```python
class FaultyPipe:
    def handle(self, content, next_func):
        raise ValueError("An error occurred!")

pipeline = Pipeline()

def error_handler(content, exception):
    print(f"Error handling content: {exception}")
    return "Default Content"

result = (
    pipeline
    .send("Some content")
    .through([FaultyPipe()])
    .on_failure(error_handler)  # Error handling
    .then_return()
)

print(result)
# Output: Error handling content: An error occurred!
# "Default Content"
```

### Conditional Pipes

The `when` method allows you to add pipes conditionally, depending on some logic.

```python
pipeline = Pipeline()

result = (
    pipeline
    .send("Message for non-admin user. badword URL: http://example.com")
    .through([RemoveBadWords()])
    .when(not user_is_admin, lambda content, next: next(ShortenUrls().handle(content, next)))  # Conditional
    .then_return()
)
```

In this example, if the user is not an admin, `ShortenUrls` will be added to the pipeline.

### Using the Hub to Manage Pipelines

The `Hub` class allows you to define and manage multiple named pipelines.

```python
hub = Hub()

# Define a pipeline for processing messages
hub.pipeline("message_processing", lambda pipeline, message: (
    pipeline
    .send(message)
    .through([RemoveBadWords(), ShortenUrls()])
    .then_return()
))

# Process a message through the "message_processing" pipeline
processed_message = hub.pipe("This is a test http://example.com with badword", "message_processing")

print(processed_message)
# Output: "This is a test https://short.ly/example.com with "
```

### Failure Handling in Hub

You can also define failure handlers in the pipelines managed by the `Hub` class, just as in the basic `Pipeline` usage.

```python
hub = Hub()

hub.pipeline("error_handling", lambda pipeline, data: (
    pipeline
    .send(data)
    .through([FaultyPipe()])
    .on_failure(error_handler)  # Error handling in Hub
    .then_return()
))

result = hub.pipe("Some data", "error_handling")

print(result)

# Output: Error handling content: An error occurred!
# "Default Content"
```

```python
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
```

## Method Reference

### `Pipeline` Methods

- **send(data)**: Sends the initial data to the pipeline.
- **via(method)**: Specifies which method should be called on each pipe. Defaults to `handle`.
- **through(pipes)**: Passes the data through the provided pipes. Accepts a list of classes.
- **when(condition, callback)**: Adds pipes conditionally based on the result of `condition`.
- **on_failure(callback)**: Sets the failure handler for exceptions encountered in the pipeline.
- **then(final_callback)**: Final processing step of the pipeline.
- **then_return()**: Returns the processed data after passing through the pipeline.

### `Hub` Methods

- **pipeline(name, callback)**: Defines a named pipeline.
- **pipe(data, pipeline_name)**: Sends data through the specified named pipeline.
- **defaults(callback)**: Defines a default pipeline to use when no name is provided.

## Conclusion

This pipeline system is highly customizable, and designed for flexibility. It allows you to organize complex workflows with ease, providing options for conditional logic, error handling, and managing multiple pipelines.
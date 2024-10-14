from typing import NoReturn

import pytest

from hub import Hub
from tests.artifacts.data_processor import DataProcessor
from tests.artifacts.number_multiplier import NumberMultiplier
from tests.artifacts.square import square
from tests.artifacts.string_manipulator import StringManipulator


def test_hub_pipeline() -> None:
    def example_pipeline(pipeline, obj):
        return (
            pipeline.send(obj)
            .through([lambda x, next: next(x * 2), lambda x, next: next(x + 1)])
            .then(lambda x: x)
        )

    hub = Hub()
    hub.pipeline("example", example_pipeline)
    result = hub.pipe(5, "example")

    assert result == 11


def test_hub_defaults() -> None:
    def default_pipeline(pipeline, obj):
        return (
            pipeline.send(obj).through([lambda x, next: next(x + 1)]).then(lambda x: x)
        )

    hub = Hub()
    hub.defaults(default_pipeline)
    result = hub.pipe(5)

    assert result == 6


def test_hub_pipeline_with_on_failure() -> None:
    def failing_pipeline(pipeline, obj):
        def raise_exception(x, next) -> NoReturn:
            raise ValueError("Test exception")

        def handle_failure(passable, exception) -> str:
            return f"Handled in hub: {passable}, {str(exception)}"

        return (
            pipeline.send(obj)
            .through([raise_exception])
            .on_failure(handle_failure)
            .then(lambda x: x)
        )

    hub = Hub()
    hub.pipeline("failing", failing_pipeline)
    result = hub.pipe(5, "failing")

    assert result == "Handled in hub: 5, Test exception"


def test_hub_with_class_based_pipelines() -> None:
    def string_pipeline(pipeline, obj):
        return (
            pipeline.send(obj)
            .via("process")
            .through([StringManipulator(), lambda x, next: next(x.split())])
            .then_return()
        )

    def number_pipeline(pipeline, obj):
        return (
            pipeline.send(obj)
            .through([NumberMultiplier(), DataProcessor(square)])
            .then_return()
        )

    hub = Hub()
    hub.pipeline("string", string_pipeline)
    hub.pipeline("number", number_pipeline)

    assert hub.pipe("hello world", "string") == ["HELLO", "WORLD"]
    assert hub.pipe(3, "number") == 36


def test_hub_pipeline_not_found() -> None:
    hub = Hub()

    with pytest.raises(ValueError, match="Pipeline 'non_existent' not found"):
        hub.pipe(5, "non_existent")

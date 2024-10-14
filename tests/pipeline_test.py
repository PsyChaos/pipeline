from typing import NoReturn

import pytest

from pipeline import Pipeline
from tests.artifacts.data_processor import DataProcessor
from tests.artifacts.exception_raisor import ExceptionRaiser
from tests.artifacts.list_formatter import ListFormatter
from tests.artifacts.number_multiplier import NumberMultiplier
from tests.artifacts.remove_bad_words import RemoveBadWords
from tests.artifacts.shorten_urls import ShortenUrls
from tests.artifacts.square import square
from tests.artifacts.string_manipulator import StringManipulator


def test_pipeline_send() -> None:
    pipeline = Pipeline()

    assert pipeline.send(10).passable == 10


def test_pipeline_through() -> None:
    pipeline = Pipeline()

    assert pipeline.through([1, 2, 3]).pipes == [1, 2, 3]


def test_pipeline_when_condition_true() -> None:
    pipeline = Pipeline()

    result = (
        pipeline.send("This is a badword and a URL: http://example.com")
        .through([RemoveBadWords()])
        .when(True, ShortenUrls())
        .then_return()
    )

    assert result == "This is a  and a URL: https://short.ly/example.com"


def test_pipeline_when_condition_false() -> None:
    pipeline = Pipeline()

    result = (
        pipeline.send("This is a badword and a URL: http://example.com")
        .through([RemoveBadWords()])
        .when(False, ShortenUrls())
        .then_return()
    )

    assert result == "This is a  and a URL: http://example.com"


def test_pipeline_when_with_multiple_conditions() -> None:
    pipeline = Pipeline()

    result = (
        pipeline.send("This is a badword and a URL: http://example.com")
        .through([RemoveBadWords()])
        .when(True, ShortenUrls())
        .when(False, StringManipulator())
        .then_return()
    )

    assert result == "This is a  and a URL: https://short.ly/example.com"


def test_pipeline_when_with_failure_handler() -> NoReturn:
    pipeline = Pipeline()

    def handle_failure(passable, exception) -> str:
        return f"Handled error for {passable}: {str(exception)}"

    def raise_exception(content, next) -> NoReturn:
        raise ValueError("Test Exception")

    result = (
        pipeline.send("This will raise an error")
        .through([raise_exception])
        .on_failure(handle_failure)
        .when(True, ShortenUrls())
        .then_return()
    )

    # Failure handler çalışmalı
    assert result == "Handled error for This will raise an error: Test Exception"


def test_pipeline_via() -> None:
    pipeline = Pipeline()

    assert pipeline.via("process").method == "process"


def test_pipeline_then() -> None:
    def add_one(x):
        return x + 1

    def multiply_by_two(x, next):
        return next(x * 2)

    pipeline = Pipeline()
    result = pipeline.send(5).through([multiply_by_two]).then(add_one)

    assert result == 11


def test_pipeline_then_return() -> None:
    pipeline = Pipeline()
    result = (
        pipeline.send(5)
        .through([lambda x, next: next(x * 2), lambda x, next: next(x + 1)])
        .then_return()
    )

    assert result == 11


def test_pipeline_with_exception() -> None:
    def raise_exception(x, next) -> NoReturn:
        raise ValueError("Test exception")

    def add_one(x):
        return x + 1

    pipeline = Pipeline()

    with pytest.raises(ValueError):
        pipeline.send(5).through([raise_exception]).then(add_one)


def test_pipeline_with_on_failure() -> None:
    def raise_exception(x, next) -> NoReturn:
        raise ValueError("Test exception")

    def add_one(x):
        return x + 1

    def handle_failure(passable, exception) -> str:
        return f"Handled error for {passable}: {str(exception)}"

    pipeline = Pipeline()
    result = (
        pipeline.send(5)
        .through([raise_exception])
        .on_failure(handle_failure)
        .then(add_one)
    )

    assert result == "Handled error for 5: Test exception"


def test_pipeline_with_string_manipulator() -> None:
    pipeline = Pipeline()
    result = (
        pipeline.send("hello")
        .via("process")
        .through([StringManipulator()])
        .then_return()
    )

    assert result == "HELLO"


def test_pipeline_with_number_multiplier() -> None:
    pipeline = Pipeline()
    result = pipeline.send(5).through([NumberMultiplier()]).then_return()

    assert result == 10


def test_pipeline_with_list_formatter() -> None:
    pipeline = Pipeline()
    result = pipeline.send(["a", "b", "c"]).through([ListFormatter()]).then_return()

    assert result == ["Item: a", "Item: b", "Item: c"]


def test_pipeline_with_data_processor() -> None:
    pipeline = Pipeline()
    processor = DataProcessor(square)
    result = pipeline.send(4).through([processor]).then_return()

    assert result == 16


def test_pipeline_with_multiple_classes():
    pipeline = Pipeline()
    result = (
        pipeline.send(5)
        .through(
            [NumberMultiplier(), DataProcessor(square), lambda x, next: next(str(x))]
        )
        .then_return()
    )

    assert result == "100"


def test_pipeline_with_exception_handling() -> None:
    def handle_failure(passable, exception) -> str:
        return f"Caught an error: {str(exception)}"

    pipeline = Pipeline()
    result = (
        pipeline.send("test data")
        .through([ExceptionRaiser()])
        .on_failure(handle_failure)
        .then_return()
    )

    assert result == "Caught an error: Intentional error for testing"

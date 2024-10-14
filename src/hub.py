from typing import Any, Callable

from src.contracts.hub_contract import HubContract
from src.pipeline import Pipeline


class Hub(HubContract):
    def __init__(self) -> None:
        self.pipelines = {}

    def defaults(self, callback: Callable) -> None:
        """Define the default pipeline configuration.

        Args:
            callback (Callable): The default pipeline setup function.
        """
        return self.pipeline("default", callback)

    def pipeline(self, name: str, callback: Callable) -> None:
        """Define a named pipeline configuration.

        Args:
            name (str): The name of the pipeline.
            callback (Callable): The setup function for the pipeline.
        """
        self.pipelines[name] = callback

    def pipe(self, obj: Any, pipeline: str = None) -> Any:
        """Execute the specified pipeline with the given object.

        Args:
            obj (Any): The object that will be processed through the pipeline.
            pipeline (str, optional): The name of the pipeline to use. Defaults to None, which uses the default pipeline.

        Returns:
            Any: The processed result.
        """
        pipeline = pipeline or "default"

        if pipeline not in self.pipelines:
            raise ValueError(f"Pipeline '{pipeline}' not found")

        return self.pipelines[pipeline](Pipeline(), obj)

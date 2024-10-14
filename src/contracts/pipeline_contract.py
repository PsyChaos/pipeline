from abc import ABC, abstractmethod
from typing import Any, Callable, List, Self, Union


class PipelineContract(ABC):
    @abstractmethod
    def send(self, traveler: Any) -> Self:
        """Send the initial data to the pipeline.

        Args:
            traveler (Any): The data (traveler) that will go through the pipeline.

        Returns:
            Self: The pipeline instance.
        """
        pass

    @abstractmethod
    def through(self, stops: Union[List[Any], Any]) -> Self:
        """Specify the pipes (processing stages) that the data should pass through.

        Args:
            stops (Union[List[Any], Any]): A list of pipes or a single pipe.

        Returns:
            Self: The pipeline instance.
        """
        pass

    @abstractmethod
    def when(self, condition: bool, pipe: Any) -> Self:
        """Add a pipe to the pipeline only if the condition is True.

        Args:
            condition (bool): The condition to check.
            pipe (Any): The pipe (or list of pipes) to add if the condition is met.

        Returns:
            Self: The pipeline instance.
        """
        pass

    @abstractmethod
    def via(self, method: str) -> Self:
        """Specify the method that will be called on each pipe.

        Args:
            method (str): The name of the method to call on each pipe.

        Returns:
            Self: The pipeline instance.
        """
        pass

    @abstractmethod
    def then(self, destination: Callable) -> Any:
        """Define the final destination callback after all pipes are executed.

        Args:
            destination (Callable): The final function to call after processing.

        Returns:
            Any: The result of the destination callback.
        """
        pass

    @abstractmethod
    def then_return(self) -> Any:
        """Return the final result after all pipes without needing a destination callback.

        Returns:
            Any: The final processed data.
        """
        pass

    @abstractmethod
    def on_failure(self, handler: Callable) -> Self:
        """Set a callback to handle exceptions or failures during pipeline execution.

        Args:
            handler (Callable): The failure handler function.

        Returns:
            Self: The pipeline instance.
        """
        pass

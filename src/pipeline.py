import functools
from typing import Any, Callable, List, Self, Union

from src.contracts.pipeline_contract import PipelineContract


class Pipeline(PipelineContract):
    def __init__(self) -> None:
        # The data (traveler) that will go through the pipeline
        self.passable = None
        
        # The list of pipes (processing stages) that the data should pass through
        self.pipes: list = []
        
        # The method that will be called on each pipe
        self.method: str = "handle"
        
        # The callback to handle exceptions or failures during pipeline execution
        self.failure_handler = None

    def send(self, traveler: Any) -> Self:
        """Send the initial data to the pipeline.

        Args:
            traveler (Any): The data (traveler) that will go through the pipeline.

        Returns:
            Self: The pipeline instance.
        """
        self.passable = traveler

        return self

    def through(self, stops: Union[List[Any], Any]) -> Self:
        """Specify the pipes (processing stages) that the data should pass through.

        Args:
            stops (Union[List[Any], Any]): A list of pipes or a single pipe.

        Returns:
            Self: The pipeline instance.
        """
        self.pipes = stops if isinstance(stops, list) else [stops]

        return self
    
    def when(self, condition: bool, pipe: Any) -> Self:
        """Add a pipe to the pipeline only if the condition is True.

        Args:
            condition (bool): The condition to check.
            pipe (Any): The pipe (or list of pipes) to add if the condition is met.

        Returns:
            Self: The pipeline instance.
        """
        if condition:
            self.pipes.append(pipe)
            
        return self

    def via(self, method: str) -> Self:
        """Specify the method that will be called on each pipe.

        Args:
            method (str): The name of the method to call on each pipe.

        Returns:
            Self: The pipeline instance.
        """
        self.method: str = method

        return self

    def on_failure(self, handler: Callable) -> Self:
        """Set a callback to handle exceptions or failures during pipeline execution.

        Args:
            handler (Callable): The failure handler function.

        Returns:
            Self: The pipeline instance.
        """
        self.failure_handler = handler

        return self

    def then(self, destination: Callable) -> Any:
        """Execute the pipeline and call the final destination function.

        Args:
            destination (Callable): The final function to process the result after all pipes.

        Returns:
            Any: The result of the destination function.
        """
        pipeline = functools.reduce(
            self._carry(), self.pipes[::-1], self._prepare_destination(destination)
        )

        return pipeline(self.passable)

    def then_return(self) -> Any:
        """Return the processed result directly after all pipes.

        Returns:
            Any: The final processed data.
        """
        return self.then(lambda passable: passable)

    def _carry(self):
        def wrapper(stack, pipe):
            def inner(passable):
                try:
                    if callable(pipe):
                        return pipe(passable, stack)
                    else:
                        pipe_obj = pipe
                        parameters = [passable, stack]

                    return (
                        getattr(pipe_obj, self.method)(*parameters)
                        if hasattr(pipe_obj, self.method)
                        else pipe_obj(*parameters)
                    )
                except Exception as e:
                    return self._handle_exception(passable, e)
                
            return inner
        
        return wrapper

    def _prepare_destination(self, destination: Callable):
        def wrapper(passable):
            try:
                return destination(passable)
            except Exception as e:
                return self._handle_exception(passable, e)
            
        return wrapper

    def _handle_exception(self, passable, exception):
        """Handle exceptions during the pipeline process.

        Args:
            passable (Any): The current object being processed.
            exception (Exception): The exception that occurred.

        Returns:
            Any: The result of the failure handler, if set, or raises the exception.
        """
        if self.failure_handler:
            return self.failure_handler(passable, exception)

        raise exception

from abc import ABC, abstractmethod
from typing import Any


class HubContract(ABC):
    @abstractmethod
    def pipe(self, obj: Any, pipeline: str = None) -> Any:
        """Execute the specified pipeline.

        Args:
            obj (Any): The object that will be processed through the pipeline.
            pipeline (str, optional): The name of the pipeline to use. Defaults to None, which uses the default pipeline.

        Returns:
            Any: The processed result.
        """
        pass

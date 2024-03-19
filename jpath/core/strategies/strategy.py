from jpath.core.result import Result
from jpath.core.step import Step
from abc import ABC, abstractmethod
from typing import List


class Strategy:
    @abstractmethod
    def apply(self, result: Result, step: Step) -> List[Result]:
        pass

from jpath.core.strategies.strategy import Strategy
from jpath.core.result import Result
from jpath.core.step import *

"""
This strategy is used to select all children of the current result
ONLY SUPPORTS NODE_TEST OF "NAME" for now
"""


class ChildStrategy(Strategy):
    def apply(self, result, step):
        json_data = result.json_data
        node_test = step.node_test

        if node_test.type != NodeTestType.NAME:
            raise NotImplementedError("Only NAME node test is supported for now")

        results = []
        if type(json_data) == list:
            for item in json_data:
                result = self.apply(Result(item), step)
                if result:
                    results.extend(result)
        elif type(json_data) == dict:
            if node_test.value in json_data:
                results.append(Result(json_data[node_test.value]))
        else:
            results = []  # assume str/int values have no children

        return results

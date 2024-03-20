from jpath.core.strategies.strategy import Strategy
from jpath.core.result import Result
from jpath.core.step import *


class DescendentStrategy(Strategy):
    def apply(result, step):
        json_data = result.json_data
        node_test = step.node_test

        if node_test.type != NodeTestType.NAME:
            raise NotImplementedError("Only NAME node test is supported for now")

        results = []
        if type(json_data) == list:
            for item in json_data:
                result = DescendentStrategy.apply(Result(item), step)
                if result:
                    results.extend(result)
        elif type(json_data) == dict:
            for key, value in json_data.items():
                if key == node_test.value:
                    results.append(Result(value))
                else:
                    result = DescendentStrategy.apply(Result(value), step)
                    if result:
                        results.extend(result)
        else:
            results = []  # assume str/int values have no  descendent

        return results

from jpath.core.query import Query
from jpath.core.result import Result
from jpath.core.strategies.strategy_manager import StrategyManager
from typing import List


class Evaluator:
    def __init__(self, debug=False):
        self.strategy_manager = StrategyManager()
        self.debug = debug

    def evaluate(self, query: Query, json_data):
        results = [Result(json_data)]
        if self.debug:
            print(f"Initial results: {results}")

        for step in query.steps:
            strategies = self.strategy_manager.get_strategies(step)
            if self.debug:
                print(f"Got strategies: {strategies} for step {step}")
            for strategy in strategies:
                results = self.apply_strategy(strategy, results, step)
                if self.debug:
                    print(f"Applied strategy: {strategy} for step {step}. Results: {results}")

        return results

    def apply_strategy(self, strategy, results, step) -> List[Result]:
        new_results = []
        for result in results:
            new_result: List[Result] = strategy.apply(result, step)
            if new_result:
                new_results.extend(new_result)

        return new_results

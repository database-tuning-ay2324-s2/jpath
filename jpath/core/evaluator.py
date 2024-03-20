from jpath.core.query import Query
from jpath.core.result import Result
from jpath.core.strategies.strategy_manager import StrategyManager
from jpath.core.step import *
from typing import List


class Evaluator:
    def __init__(self, debug=False):
        self.strategy_manager = StrategyManager()
        self.debug = debug

    def evaluate(self, query: Query, json_data):
        results = [Result(json_data)]
        if self.debug:
            print(f"Initial results: {results}, query: {query}")

        for step in query.steps:
            axis_strategy = self.strategy_manager.get_axis_strategy(step)
            results = self.apply_strategy(axis_strategy, results, step)

            results = self.apply_predicate(results, step)
        return results

    def apply_strategy(self, strategy, results, step) -> List[Result]:
        new_results = []
        for result in results:
            new_result: List[Result] = strategy.apply(result, step)
            if new_result:
                new_results.extend(new_result)

        return new_results

    def apply_predicate(self, results: List[Result], step: Step) -> List[Result]:
        def compare(r, predicate_operator, right_operand):
            if right_operand[0] == '"' and right_operand[-1] == '"':
                right_operand = right_operand[1:-1]
            if r[0] == '"' and r[-1] == '"':
                r = r[1:-1]

            if predicate_operator == Operator.EQUALS:
                return r == right_operand
            elif predicate_operator == Operator.NOT_EQUALS:
                return r != right_operand
            else:
                raise ValueError(f"Unknown operator: {predicate_operator}")

        if not step.predicates:
            # no predicate to apply
            return results

        #  only supports 1 predicate for now (i.e. no AND or OR predicates)
        if len(step.predicates) > 1:
            raise NotImplementedError("Only 1 predicate is supported for now")
        predicate: Predicate = step.predicates[0]

        left_operand = predicate.left_operand
        new_results = []

        for result in results:
            # for each curr result, see if the left operand can evaluate to true
            query = Query()
            query.steps = left_operand
            json_data = result.json_data

            if type(json_data) == list:
                starting_points = json_data
            else:
                starting_points = [json_data]

            for starting_point in starting_points:
                left_operand_results = self.evaluate(query, starting_point)
                if not left_operand_results:
                    # does not evaluate to true, skip this result
                    continue

                if predicate.operator:
                    # has operator e.g. [child::age > 20]
                    if all(
                        [
                            (type(r) == str or type(r == int))
                            and compare(
                                str(r), predicate.operator, predicate.right_operand
                            )
                            for r in left_operand_results
                        ]
                    ):
                        new_results.append(Result(starting_point))

                else:
                    # no operator e.g. [child::age]
                    new_results.append(Result(starting_point))

        return new_results

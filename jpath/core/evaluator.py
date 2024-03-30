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

            def parse_to_desired_type(value):
                try:
                    return float(value) # a number
                except ValueError:
                    return value[1:-1] # a string
                                
            r = parse_to_desired_type(r)
            right_operand = parse_to_desired_type(right_operand)

            if predicate_operator == Operator.EQUALS:
                return r == right_operand
            elif predicate_operator == Operator.NOT_EQUALS:
                return r != right_operand
            elif predicate_operator == Operator.GREATER_THAN:
                return r > right_operand
            elif predicate_operator == Operator.LESS_THAN:
                return r < right_operand
            elif predicate_operator == Operator.GREATER_THAN_OR_EQUAL:
                return r >= right_operand
            elif predicate_operator == Operator.LESS_THAN_OR_EQUAL:
                return r <= right_operand
            else:
                raise ValueError(f"Unknown operator: {predicate_operator}")
            
        if not step.predicates:
            # no predicate to apply
            return results

        # Do not support multiple parallel predicates (i.e. no AND or OR predicates)
        # Support result(s) selection by array index/index range
        new_results = []
        for predicate in step.predicates:
            predicate: Predicate = predicate

            if len(new_results) > 0 and len(step.predicates) > 1:
                # Array select slice
                if predicate.operator is Operator.ARRAY_SELECT_SLICE:
                    new_results_slices = []

                    max_bound = len(new_results)
                    left_bound, right_bound = map(int, predicate.left_operand.split(":"))
                    slice_step = int(predicate.right_operand)
                    right_bound = min(right_bound, max_bound)

                    if 0 <= left_bound <= right_bound <= max_bound:
                        for next_index in range(left_bound, right_bound, slice_step):
                            new_results_slices.append(new_results[next_index])
                        new_results = new_results_slices
                    else:
                        new_results = []
                # Array select single
                else:
                    isInteger = True
                    try:
                        index = int(predicate.left_operand)
                    except:
                        isInteger = False
                    
                    if isInteger and 0 <= index < len(new_results):
                        new_results = [new_results[index]]
            else:
                left_operand = predicate.left_operand

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

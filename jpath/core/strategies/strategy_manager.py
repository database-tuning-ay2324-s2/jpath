from jpath.core.step import Axis
from jpath.core.strategies.axis.child import ChildStrategy
from jpath.core.strategies.strategy import Strategy
from jpath.core.step import Step


class StrategyManager:
    def __init__(self):
        self.axis_strategy_map = {Axis.CHILD: ChildStrategy()}
        self.predicate_strategy = None

    def add_axis_strategy(self, axis: Axis, strategy: Strategy):
        if axis in self.axis_strategy_map:
            raise ValueError(f"Strategy for axis {axis} already exists")
        self.axis_strategy_map[axis] = strategy

    def get_strategies(self, step: Step):
        strategies = []
        if step.axis not in self.axis_strategy_map:
            raise ValueError(f"No strategy for axis {step.axis}")
        strategies.append(self.axis_strategy_map[step.axis])
        if step.predicates:
            strategies.append(self.predicate_strategy)
        return strategies

from jpath.core.step import Axis
from jpath.core.strategies.axis.child import ChildStrategy
from jpath.core.strategies.axis.descendent import DescendentStrategy
from jpath.core.strategies.strategy import Strategy
from jpath.core.step import Step


class StrategyManager:
    def __init__(self):
        self.axis_strategy_map = {
            Axis.CHILD: ChildStrategy,
            Axis.DESCENDANT: DescendentStrategy,
        }

    def add_axis_strategy(self, axis: Axis, strategy: Strategy):
        if axis in self.axis_strategy_map:
            raise ValueError(f"Strategy for axis {axis} already exists")
        self.axis_strategy_map[axis] = strategy

    def get_axis_strategy(self, step: Step):
        if step.axis not in self.axis_strategy_map:
            raise ValueError(f"No strategy for axis {step.axis}")
        return self.axis_strategy_map[step.axis]

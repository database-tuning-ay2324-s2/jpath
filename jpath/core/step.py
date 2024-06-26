from enum import Enum
from typing import List


# XPATH preceding/following are excluded because json is not ordered
class Axis(Enum):
    SELF = 1
    CHILD = 2
    DESCENDANT = 3
    # PARENT = 4
    # ANCESTOR = 5
    # ANCESTOR_OR_SELF = 10
    # DESCENDANT_OR_SELF = 11
    # VALUE = 12  # same as attribute from xpath, but VALUE gives the value of json keys


class NodeTestType(Enum):
    # A node name selects nodes with the given name e.g. /bookstore selects all bookstore elements;
    NAME = 1
    # text() | text() selects nodes of type text;
    # TEXT = 2
    # # node() | node() selects all types
    # NODE = 3
    # # * | selects nodes of type element or attribute depending on the axis;
    # WILDCARD = 8


class NodeTest:
    def __init__(self, type: NodeTestType, value: str):
        self.type = type
        self.value = value


class Operator(Enum):
    EQUALS = 1
    NOT_EQUALS = 2
    GREATER_THAN = 3
    LESS_THAN = 4
    GREATER_THAN_OR_EQUAL = 5
    LESS_THAN_OR_EQUAL = 6
    ARRAY_SELECT_SINGLE = 7
    ARRAY_SELECT_SLICE = 8

class Predicate:
    # Example 1: [child::car_code = '1234'] Check if the element has a child element with the name car_code and the value is 1234
    # Example 2: [child::car_code] Check if the element has a child element with the name car_code. Note that in this case, operator and right operand are None
    def __init__(
        self, left_operand: List["Step"], operator: Operator = None, right_operand: str =None, support_nested = True
    ):
        self.left_operand =left_operand
        self.operator = operator
        self.right_operand = right_operand
        self.support_nested = support_nested

    def __repr__(self) -> str:
        if self.operator:
            return f"{self.left_operand} {self.operator} {self.right_operand} {self.support_nested}"
        else:
            return f"{self.left_operand} {self.support_nested}"


# A location path is a sequence of location steps. The locations steps are separated by a slash. e.g. /step1/step2/step3
class Step:
    def __init__(self, axis: Axis, node_test: NodeTest):
        self.axis = (
            axis  # The axis of the step e.g. child, parent, ancestor, descendant, etc.
        )
        self.node_test = node_test
        self.predicates = (
            []
        )  # The predicates of the step e.g.  [name='value'], etc.

    def add_predicate(self, predicate: Predicate):
        self.predicates.append(predicate)

    def __repr__(self):
        out = f"{self.axis.name}::{self.node_test.value}"
        if self.predicates:
            out += f"{self.predicates}"
        return out

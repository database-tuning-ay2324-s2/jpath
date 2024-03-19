from enum import Enum

# XPATH preceding/following are excluded because json is not ordered
class Axis(Enum):
    SELF = 1
    CHILD = 2
    DESCENDANT = 3
    PARENT = 4
    ANCESTOR = 5
    ANCESTOR_OR_SELF = 10
    DESCENDANT_OR_SELF = 11
    VALUE = 12  # same as attribute from xpath, but VALUE gives the value of json keys


class NodeTestType(Enum):
    # A node name selects nodes with the given name e.g. /bookstore selects all bookstore elements;
    NAME = 1
    # text() | text() selects nodes of type text;
    TEXT = 2
    # node() | node() selects all types
    NODE = 3
    # * | selects nodes of type element or attribute depending on the axis;
    WILDCARD = 8

class NodeTest:
    def __init__(self, type: NodeTestType, value: str):
        self.type = type
        self.value = value


class Operator(Enum):
    EQUALS = 1
    NOT_EQUALS = 2
    LESS_THAN = 3
    LESS_THAN_OR_EQUALS = 4
    GREATER_THAN = 5
    GREATER_THAN_OR_EQUALS = 6


class Predicate:
    def __init__(self, left_operand: "Step", operator: Operator, right_operand: str):
        self.left_operand = None
        self.operator = None
        self.right_operand = None


# A location path is a sequence of location steps. The locations steps are separated by a slash. e.g. /step1/step2/step3
class Step:
    def __init__(self, axis: Axis, node_test: NodeTest):
        self.axis = (
            axis  # The axis of the step e.g. child, parent, ancestor, descendant, etc.
        )
        self.node_test = node_test
        self.predicates = (
            []
        )  # The predicates of the step e.g. [1], [name='value'], etc.

    def add_predicate(self, predicate: Predicate):
        self.predicates.append(predicate)

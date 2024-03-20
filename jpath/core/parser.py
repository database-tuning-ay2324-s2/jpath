from jpath.core.query import Query
from jpath.core.step import Step, Axis, NodeTest, NodeTestType, Predicate, Operator


class Parser:
    def __init__(self):
        pass

    def parse(self, query: str) -> Query:
        query_obj = Query()
        current_step = ""
        current_predicate = ""
        in_predicate = False

        for char in query:
            if char == "/":
                if not in_predicate:
                    if current_step:
                        step, predicates = self._parse_step(
                            current_step, current_predicate
                        )
                        step.predicates.extend(predicates)
                        query_obj.add_step(step)
                        current_step = ""
                        current_predicate = ""
                else:
                    current_predicate += char
            elif char == "[":
                in_predicate = True
                current_predicate += char
            elif char == "]":
                in_predicate = False
                current_predicate += char
            elif char == "/" and not in_predicate:
                current_step += char
            else:
                if in_predicate:
                    current_predicate += char
                else:
                    current_step += char

        # Parsing the last step if any
        if current_step:
            step, predicates = self._parse_step(current_step, current_predicate)
            step.predicates.extend(predicates)
            query_obj.add_step(step)

        return query_obj

    def _parse_step(self, step_str: str, predicate_str: str) -> (Step, list):
        axis_str, node_test_str = step_str.split("::", 1)
        axis = self._parse_axis(axis_str)
        node_test, predicates = self._parse_node_test(node_test_str, predicate_str)
        step = Step(axis, node_test)
        return step, predicates

    def _parse_axis(self, axis_str: str) -> Axis:
        axis_map = {
            "self": Axis.SELF,
            "child": Axis.CHILD,
            "descendant": Axis.DESCENDANT,
            # "parent": Axis.PARENT,
            # "ancestor": Axis.ANCESTOR,
            # "ancestor_or_self": Axis.ANCESTOR_OR_SELF,
            # "descendant_or_self": Axis.DESCENDANT_OR_SELF,
            # "value": Axis.VALUE,
        }
        return axis_map[axis_str]

    def _parse_node_test(
        self, node_test_str: str, predicate_str: str
    ) -> (NodeTest, list):
        # Parsing NodeTestType
        if node_test_str == "text()":
            node_test_type = NodeTestType.TEXT
            value = None
        elif node_test_str == "node()":
            node_test_type = NodeTestType.NODE
            value = None
        elif node_test_str == "*":
            node_test_type = NodeTestType.WILDCARD
            value = None
        else:
            node_test_type = NodeTestType.NAME
            value = node_test_str

        node_test = NodeTest(node_test_type, value)
        predicates = []

        # Parsing predicates
        if "[" in predicate_str and "]" in predicate_str:
            predicate = self._parse_predicate(predicate_str)
            predicates.append(predicate)

        return node_test, predicates

    # TODO: parse nested predicates e.g. /child::A[child::B[child::C = 3]]
    def _parse_predicate(self, predicate_str: str) -> Predicate:
        operator_map = {"=": Operator.EQUALS, "!=": Operator.NOT_EQUALS}

        # take out brackets
        predicate_str = predicate_str[1:-1]

        operator_str = None
        if "=" in predicate_str:
            operator_str = "="
        elif "!=" in predicate_str:
            operator_str = "!="

        if operator_str:
            left_operand_str, right_operand_str = predicate_str.split(operator_str, 1)
            left_operand_str = left_operand_str.strip()

            left_operand = self.parse(left_operand_str).steps
            right_operand_str = right_operand_str.strip()
            return Predicate(
                left_operand, operator_map[operator_str], right_operand_str
            )
        else:
            left_operand_str = predicate_str.strip()
            left_operand = self.parse(left_operand_str).steps
            return Predicate(left_operand)

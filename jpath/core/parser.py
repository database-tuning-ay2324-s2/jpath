import re
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
        nested_pred = True
        sub_predicate_str = predicate_str.split("]")
        if not sub_predicate_str:
            nested_pred = False
        else:
            if not sub_predicate_str[-1] and len(sub_predicate_str) > 1:
                sub_predicate_str.pop()
            last_sub_pred = sub_predicate_str[-1]
            operator_strings = [">", "<", ">=", "<=", "=", "!="]
            has_operator = any(operator_strings in last_sub_pred for operator_strings in operator_strings)
            if (not has_operator) and re.match(r"^\d*$", last_sub_pred[1:-1]):
                nested_pred = False
            if (":" in last_sub_pred) and re.match(r"[0-9]:[0-9]", last_sub_pred[1:]):
                nested_pred = False
        
        if not nested_pred:
            for sub_p_str in sub_predicate_str:
                sub_p_str += "]"
                if "[" in predicate_str and "]" in sub_p_str:
                    predicate = self._parse_predicate_slice(sub_p_str)
                    predicate.support_nested = False
                    predicates.append(predicate)
        else:
            if "[" in predicate_str and "]" in predicate_str:
                predicate = self._parse_predicate(predicate_str, [])
                predicates.extend(predicate)

        return node_test, predicates
    
    def _parse_predicate_slice(self, predicate_str: str) -> Predicate:
        operator_map = {"=": Operator.EQUALS, "!=": Operator.NOT_EQUALS, "<": Operator.LESS_THAN, ">": Operator.GREATER_THAN, ">=": Operator.GREATER_THAN_OR_EQUAL, "<=": Operator.LESS_THAN_OR_EQUAL, "sel": Operator.ARRAY_SELECT_SINGLE, ":": Operator.ARRAY_SELECT_SLICE}
        # take out brackets
        predicate_str = predicate_str[1:-1]

        operator_str = None
        if ">=" in predicate_str:
            operator_str = ">="
        elif "!=" in predicate_str:
            operator_str = "!="
        elif "<=" in predicate_str:
            operator_str = "<="
        elif "=" in predicate_str:
            operator_str = "="
        elif "<" in predicate_str:
            operator_str = "<"
        elif ">" in predicate_str:
            operator_str = ">"
        elif re.match(r"^\d*$", predicate_str):
            operator_str = "sel"
        elif ":" in predicate_str and re.match(r"[0-9]:[0-9]", predicate_str):
            operator_str = ":"

        if operator_str == "sel":
            return Predicate(predicate_str)
        if operator_str == ":":
            if re.match(r"[0-9]:[0-9]:[0-9]", predicate_str):
                left_operand_str = predicate_str.split(":")[0] + ":" + predicate_str.split(":")[1]
                right_operand_str = predicate_str.split(":")[-1]
            else:
                left_operand_str = predicate_str
                right_operand_str = "1"

            return Predicate(
                left_operand_str, operator_map[operator_str], right_operand_str
            )
        elif operator_str:
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

    # TODO: parse nested predicates e.g. /child::A[child::B[child::C = 3]]
    # /child::A[child::B and child::C]
    # /child::A[(child::B and child::C) or child::D]
    # /child::A[((child::B and child::C) and child::F) or child::D]
    # /child::A[child::B[child::C = 3] or child::B[child::D=7]]
    def _parse_predicate(self, predicate_str: str, predicate_list: list) -> []:
        operator_map = {"=": Operator.EQUALS, "!=": Operator.NOT_EQUALS, "<": Operator.LESS_THAN, ">": Operator.GREATER_THAN, ">=": Operator.GREATER_THAN_OR_EQUAL, "<=": Operator.LESS_THAN_OR_EQUAL, "sel": Operator.ARRAY_SELECT_SINGLE, ":": Operator.ARRAY_SELECT_SLICE}
        # operator_map = {"=": Operator.EQUALS, "!=": Operator.NOT_EQUALS}

        # take out brackets
        # predicate_str = predicate_str[1:-1]
        # print(predicate_str)
        if "[" in predicate_str[1:]:
            # strip first bracket
            predicate_str = predicate_str[1:]
            next_square_bracket = predicate_str.find("[")
            # TODO: no support for AND and OR predicates
            curr_predicate = predicate_str[:next_square_bracket]
            left_operand_str = curr_predicate.strip()
            left_operand = self.parse(left_operand_str).steps
            predicate_list.append(Predicate(left_operand))
            return self._parse_predicate(predicate_str[next_square_bracket:], predicate_list)

        predicate_str = predicate_str[1:predicate_str.find("]")]
        operator_str = None
        if "!=" in predicate_str:
            operator_str = "!="
        elif ">=" in predicate_str:
            operator_str = ">="
        elif "<=" in predicate_str:
            operator_str = "<="
        elif "=" in predicate_str:
            operator_str = "="
        elif "<" in predicate_str:
            operator_str = "<"
        elif ">" in predicate_str:
            operator_str = ">"
        elif re.match(r"^\d*$", predicate_str):
            operator_str = "sel"
        elif ":" in predicate_str and re.match(r"[0-9]:[0-9]", predicate_str):
            operator_str = ":"

        if operator_str:
            left_operand_str, right_operand_str = predicate_str.split(operator_str, 1)
            left_operand_str = left_operand_str.strip()

            left_operand = self.parse(left_operand_str).steps
            right_operand_str = right_operand_str.strip()
            predicate_list.append(
                Predicate(left_operand, operator_map[operator_str], right_operand_str)
            )
            return predicate_list
        else:
            left_operand_str = predicate_str.strip()
            left_operand = self.parse(left_operand_str).steps
            predicate_list.append(Predicate(left_operand))
            return predicate_list

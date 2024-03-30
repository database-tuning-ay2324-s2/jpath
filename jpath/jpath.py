import json
from jpath.core.evaluator import Evaluator
from jpath.core.parser import Parser


class JPath:
    def __init__(self, json_data, debug=False):
        self.debug = debug
        self.parser = Parser()
        self.evaluator = Evaluator(debug=self.debug)

        # Parse JSON data
        if type(json_data) == str:
            try:
                self.json_data = json.loads(json_data)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON data: {e}")
        elif type(json_data) == dict:
            self.json_data = json_data
        else:
            raise ValueError(f"Invalid JSON data type: {type(json_data)}")

    def query(self, jpath_expr) -> str:
        query = self.parser.parse(jpath_expr)
        return self._query(query)

    # Query by a provided query object
    def _query(self, query):
        results = self.evaluator.evaluate(query, self.json_data)
        return JPath.format_results(results)

    def format_results(results):
        return "\n".join([str(result) for result in results])


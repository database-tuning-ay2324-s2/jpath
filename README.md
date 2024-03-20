# JPath: XPath for JSON

JPath is a Python library that enables XPath-like querying of JSON data. JPath allows users to apply XPath expressions to JSON, facilitating complex data retrieval with the ease and flexibility of XPath. Since the syntax of JPath is almost similar to XPath, there is no need to relearn a new language. You can simply apply your current skill of XPath querying!

Features

Apply XPath-like expressions to JSON data.
Extract specific parts of JSON based on the query.

Installation

Currently, JPath is not available as a package in PyPI. To use JPath, clone the repository or copy the code into your project.

## Sample JSON data

```
from jpath.jpath import JPath

JSON_STRING = """
{
	"employees": [
		{"id": 1, "name": "John Doe", "department": "Engineering", "salary": 60000, "good": true},
		{"id": 2, "name": "Jane Smith", "department": "Marketing", "salary": 55000},
		{"id": 3, "name": "Alice Johnson", "department": "Sales", "salary": 58000}
	],
    "employers": [
		{"id": 4, "name": "ggman", "role": {"title": "CEO", "department": "Engineering", "salary": 60000}},
		{"id": 5, "name": "jon", "role": {"title": "CTO", "department": "Engineering", "salary": 70000}},
		{"id": 6, "name": "sydney", "role": {"title": "COO", "department": "Operations", "salary": 80000}}
	]
}
"""
```

## Initialize JPath with JSON data

```
jpath = JPath(JSON_STRING,debug=False)
```

## Query the data

```
result = jpath.query("/child::employees/child::department") # returns "Engineering" "Marketing" "Sales"
```

#### For more examples, see examples/demo.ipynb

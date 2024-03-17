# JPath: XPath for JSON

JPath is a Python library that enables XPath-like querying of JSON data. By converting JSON data into an XML-like structure internally, JPath allows users to apply XPath expressions to JSON, facilitating complex data retrieval with the ease and flexibility of XPath.

Features
Convert JSON data to an XML-like structure for querying.
Apply XPath expressions to JSON data.
Extract specific parts of JSON based on the query.
Installation
Currently, JPath is not available as a package in PyPI. To use JPath, clone the repository or copy the code into your project.

Dependencies
JPath relies on the following Python libraries:

lxml for XPath support and XML handling.
xml.etree.ElementTree as part of Python's standard library for initial XML conversion.

Run the command below to start contributing
```
pip install -r requirements.txt
```

## Sample JSON data

```
json_data = {
    "employees": [
        {"id": 1, "name": "John Doe", "department": "Engineering", "salary": 60000},
        {"id": 2, "name": "Jane Smith", "department": "Marketing", "salary": 55000},
        {"id": 3, "name": "Alice Johnson", "department": "Sales", "salary": 58000}
    ]
}
```

## Initialize JPath with JSON data
```
jpath_instance = JPath(json_data)
```

## Query the data
```
results = jpath_instance.query("/root/employees/item[name='John Doe']/salary") # returns 60000
```

### Examples
Below are additional examples of using JPath to query JSON data:

Querying for a List of Names
```
names = jpath_instance.query("/root/employees/item/name")
```
print(names)
Finding Specific Employee Details
```
employee_details = jpath_instance.query("/root/employees/item[id='2']")
```

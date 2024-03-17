import json
import xml.etree.ElementTree as ET
import lxml.etree as etree

class JPath:
    def __init__(self, json_data):
        self.json_data = json_data

    def query(self, xpath_expr):
        try:
            # Convert JSON to XML
            json_xml = self._convert_to_xml("root", self.json_data)
            
            # Convert XML ElementTree to string and parse again with lxml for XPath support
            xml_str = ET.tostring(json_xml, encoding='unicode')
            json_xml_lxml = etree.fromstring(xml_str)
            
            # Evaluate XPath expression adjusted for the actual XML structure
            xpath_results = json_xml_lxml.xpath(xpath_expr)
            
            return [result.text for result in xpath_results]
        except Exception as e:
            raise ValueError(f"Error executing XPath expression: {e}")

    def _convert_to_xml(self, tag_name, json_obj):
        element = ET.Element(tag_name)
        if isinstance(json_obj, dict):
            for key, val in json_obj.items():
                child = self._convert_to_xml(key, val)
                element.append(child)
        elif isinstance(json_obj, list):
            for item in json_obj:
                child = self._convert_to_xml("item", item)  # This creates <item> for each element in a list
                element.append(child)
        else:
            element.text = str(json_obj)
        return element

if __name__ == "__main__":
    json_data = {
        "employees": [
            {"id": 1, "name": "John Doe", "department": "Engineering", "salary": 60000},
            {"id": 2, "name": "Jane Smith", "department": "Marketing", "salary": 55000},
            {"id": 3, "name": "Alice Johnson", "department": "Sales", "salary": 58000}
        ]
    }

    xpath_json = JPath(json_data)

    results = xpath_json.query("/root/employees/item[name='John Doe']/salary")

    print(results)  

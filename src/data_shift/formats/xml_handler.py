"""XML format handler for DataShift."""

import pathlib
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Union

try:
    import lxml.etree as LET

    HAVE_LXML = True
except ImportError:
    HAVE_LXML = False


def _element_to_dict(element: ET.Element) -> Union[Dict[str, Any], str]:
    """Convert an XML element to a dictionary."""
    result: Dict[str, Any] = {}

    # Add attributes
    if element.attrib:
        result.update(element.attrib)

    # Add children
    for child in element:
        child_data = _element_to_dict(child)
        if child.tag in result:
            if not isinstance(result[child.tag], list):
                result[child.tag] = [result[child.tag]]
            result[child.tag].append(child_data)
        else:
            result[child.tag] = child_data

    # Add text content if there are no children
    text = element.text.strip() if element.text else ""
    if not result and text:
        return text
    elif text:
        result["#text"] = text

    return result


def _dict_to_element(
    data: Union[Dict[str, Any], List[Dict[str, Any]], str],
    root_name: str = "root",
) -> ET.Element:
    """Convert a dictionary to an XML element."""
    if isinstance(data, str):
        element = ET.Element(root_name)
        element.text = data
        return element

    if isinstance(data, list):
        element = ET.Element(root_name)
        for item in data:
            element.append(_dict_to_element(item, "item"))
        return element

    element = ET.Element(root_name)

    for key, value in data.items():
        if key == "#text":
            element.text = str(value)
        elif isinstance(value, dict):
            element.append(_dict_to_element(value, key))
        elif isinstance(value, list):
            for item in value:
                element.append(_dict_to_element(item, key))
        else:
            # Treat as attribute
            element.set(key, str(value))

    return element


def read(path: pathlib.Path, **kwargs: Any) -> Dict[str, Any]:
    """
    Read data from an XML file.

    Args:
        path: Path to the XML file
        **kwargs: Additional options for XML reading

    Returns:
        Dictionary representing the XML data
    """
    use_lxml = kwargs.get("use_lxml", HAVE_LXML)

    if use_lxml and HAVE_LXML:
        tree = LET.parse(str(path))
        root = tree.getroot()
    else:
        tree = ET.parse(path)
        root = tree.getroot()

    return {root.tag: _element_to_dict(root)}


def write(
    data: Union[List[Dict[str, Any]], Dict[str, Any]],
    path: pathlib.Path,
    **kwargs: Any,
) -> None:
    """
    Write data to an XML file.

    Args:
        data: Data to write (list of dictionaries or dictionary)
        path: Path to the XML file
        **kwargs: Additional options for XML writing
    """
    use_lxml = kwargs.get("use_lxml", HAVE_LXML)
    root_name = kwargs.get("root_name", "root")

    # Create root element
    if isinstance(data, dict) and len(data) == 1:
        # If data has a single key, use it as the root name
        root_name = next(iter(data.keys()))
        root_data = data[root_name]
        root = _dict_to_element(root_data, root_name)
    else:
        root = _dict_to_element(data, root_name)

    # Create tree and write to file
    tree = ET.ElementTree(root)

    if use_lxml and HAVE_LXML:
        # Use lxml for pretty printing
        lxml_tree = LET.ElementTree(LET.fromstring(ET.tostring(root, encoding="utf-8")))
        lxml_tree.write(
            str(path), pretty_print=True, encoding="utf-8", xml_declaration=True
        )
    else:
        # Use standard library
        tree.write(path, encoding="utf-8", xml_declaration=True)

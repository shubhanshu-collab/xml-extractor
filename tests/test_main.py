import unittest
import xml.etree.ElementTree as ET
from io import StringIO
import sys
import os
import csv  # Import the csv module

# Add the src directory to the system path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if src_path not in sys.path:
    sys.path.append(src_path)
from xml_extractor.extractor import XmlExtractor

class TestXmlExtractor(unittest.TestCase):

    def setUp(self):
        # Sample XML data for testing
        self.sample_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <document>
            <omsection>
                <head>Section Title 1</head>
                <block>
                    <head>Subsection Title 1.1</head>
                    <para>Content of subsection 1.1.</para>
                </block>
                <block>
                    <head>Subsection Title 1.2</head>
                    <para>Content of subsection 1.2.</para>
                </block>
            </omsection>
            <omsection>
                <head>Section Title 2</head>
                <para>Content of section 2 without block.</para>
            </omsection>
        </document>
        """
        self.test_xml_file = StringIO(self.sample_xml)
        self.tree = ET.ElementTree(file=self.test_xml_file)
        self.extractor = XmlExtractor.__new__(XmlExtractor)
        self.extractor.tree = self.tree

    def test_parse_xml_file(self):
        # Test parsing XML file
        extractor = XmlExtractor("data/omdxe11330.xml")
        extractor.tree = self.tree
        self.assertIsNotNone(extractor.tree)

    def test_get_text_content(self):
        # Test extracting text content from an element
        element = self.tree.getroot().find(".//omsection/head")
        text_content = self.extractor._get_text_content(element)
        self.assertEqual(text_content, "Section Title 1")

    def test_extract_structured_data(self):
        # Test extracting structured data from XML
        data = self.extractor.extract_structured_data()
        self.assertEqual(len(data), 198)

    def test_process_element_content(self):
        # Test processing element content
        element = self.tree.getroot().find(".//omsection")
        content = self.extractor._process_element_content(element)
        expected_content = "Content of subsection 1.1.\nContent of subsection 1.2."
        self.assertEqual(content, expected_content)

    def test_clean_text(self):
        # Test cleaning text
        text = "This is a /block test."
        cleaned_text = self.extractor._clean_text(text)
        self.assertEqual(cleaned_text, "This is a test.")

    def test_save_to_csv(self):
        # Test saving data to CSV
        data = [
            {'section': 'Section 1', 'subsection': 'Subsection 1.1', 'content': 'Content 1.1'},
            {'section': 'Section 1', 'subsection': 'Subsection 1.2', 'content': 'Content 1.2'},
            {'section': 'Section 2', 'subsection': '', 'content': 'Content 2'}
        ]
        output_file = "output_test.md"
        self.extractor.save_to_csv(data, output_file)
        with open(output_file, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            self.assertEqual(len(rows), 3)
            self.assertEqual(rows[0]['section'], 'Section 1')
            self.assertEqual(rows[0]['subsection'], 'Subsection 1.1')
            self.assertEqual(rows[0]['content'], 'Content 1.1')

if __name__ == "__main__":
    unittest.main()

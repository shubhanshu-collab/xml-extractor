#!/usr/bin/env python3
"""
XML Extractor module - Provides the XmlExtractor class for processing XML files.
"""

import csv
import logging
import re
import xml.etree.ElementTree as ET


class XmlExtractor:
    """
    Extracts structured content from XML files with sections and subsections.

    Processes XML files where <omsection> elements represent sections and
    <block> elements represent subsections. Extracts text from paragraphs
    and converts tables to Markdown format.
    """

    def __init__(self, file_path):
        """Initialize with the path to the XML file to process."""
        self.file_path = file_path
        self.tree = self._parse_xml_file()

    def _parse_xml_file(self):
        """Parse the XML file and return an ElementTree."""
        try:
            tree = ET.parse(self.file_path)
            logging.info(f"Successfully parsed XML file: {self.file_path}")
            return tree
        except Exception as e:
            logging.error(f"Error parsing XML file: {e}")
            raise

    def _get_text_content(self, element):
        """Recursively collect and return all text from an element."""
        return " ".join(element.itertext()).strip() if element is not None else ""

    def extract_structured_data(self):
        """
        Extract text content from sections and subsections.

        Returns:
            list: A list of dictionaries with keys: 'section', 'subsection', and 'content'.
        """
        root = self.tree.getroot()
        data = []

        for section in root.findall(".//omsection"):
            section_head = section.find("head")
            section_title = self._get_text_content(section_head) if section_head is not None else "No Section Title"
            blocks = section.findall("block")

            if not blocks:
                content = self._process_element_content(section)
                data.append({
                    'section': section_title,
                    'subsection': '',
                    'content': content
                })
            else:
                for block in blocks:
                    block_head = block.find("head")
                    subsection_title = self._get_text_content(block_head) if block_head is not None else "No Subsection Title"
                    content = self._process_element_content(block)
                    data.append({
                        'section': section_title,
                        'subsection': subsection_title,
                        'content': content
                    })

        return data

    def _process_element_content(self, element):
        """
        Process the content of an element, extracting text and tables.

        Args:
            element: XML element to process

        Returns:
            str: Combined text content from paragraphs and tables
        """
        texts = []
        inside_table = False

        for child in element.iter():
            if child.tag == "table":
                inside_table = True
                md_table = self._table_to_markdown(child)
                if md_table:
                    texts.append(md_table)
            elif child.tag == "para" and not inside_table:
                para_text = child.text.strip() if child.text else ""
                if para_text:
                    texts.append(para_text)
            elif child.tag == "table" and inside_table:
                inside_table = False

        return "\n".join(texts)

    def _table_to_markdown(self, table_element):
        """
        Convert an XML table to Markdown format.

        Args:
            table_element: XML table element to convert

        Returns:
            str: Markdown representation of the table
        """
        lines = []

        # Extract caption if it exists
        caption_elem = table_element.find("caption")
        if caption_elem is not None and caption_elem.text:
            caption = self._clean_text(caption_elem.text)
            lines.append(f"**{caption}**")
            lines.append("")  # blank line

        # Process header rows
        header_rows = []
        thead = table_element.find("tgroup/thead")
        if thead is not None:
            for row in thead.findall("row"):
                entries = []
                for entry in row.findall("entry"):
                    para = entry.find("para")
                    text = self._clean_text(para.text) if (para is not None and para.text) else ""
                    entries.append(text)
                if entries:
                    header_rows.append(" | ".join(entries))

            if header_rows:
                lines.append("**Header:**")
                lines.extend(header_rows)
                lines.append("")

        # Process body rows
        body_rows = []
        tbody = table_element.find("tgroup/tbody")
        if tbody is not None:
            for row in tbody.findall("row"):
                entries = []
                for entry in row.findall("entry"):
                    para = entry.find("para")
                    text = self._clean_text(para.text) if (para is not None and para.text) else ""
                    entries.append(text)
                if entries:
                    body_rows.append(" | ".join(entries))

            if body_rows:
                lines.append("**Rows:**")
                lines.extend(body_rows)

        markup = "\n".join(lines)
        logging.debug(f"Converted table markup: {markup[:60]}...")
        return markup

    @staticmethod
    def _clean_text(text):
        """
        Remove meta tokens that start with a slash (e.g., '/block').

        Args:
            text: Text to clean

        Returns:
            str: Cleaned text
        """
        if not text:
            return ""

        # Split text into words and remove any that start with "/"
        words = text.split()
        cleaned_words = [word for word in words if not re.match(r'^/[A-Za-z]+$', word)]

        # Also remove stray occurrences like '/block' within a string using regex
        cleaned = re.sub(r'/[A-Za-z]+', '', " ".join(cleaned_words), flags=re.IGNORECASE)
        return cleaned.strip()

    def save_to_csv(self, data, output_file):
        """
        Write the extracted data to a CSV file.

        Args:
            data: List of dictionaries with keys: 'section', 'subsection', and 'content'
            output_file: Path to the output CSV file
        """
        try:
            with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ['section', 'subsection', 'content']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
            logging.info(f"Data successfully written to CSV file: {output_file}")
        except Exception as e:
            logging.error(f"Error writing CSV file: {e}")
            raise
 
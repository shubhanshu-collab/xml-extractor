# XML Extractor

This Python application processes XML files by extracting text data from sections and subsections. It converts table elements to Markdown and outputs the results in a CSV file.

## Features

- XML Parsing: Uses Python’s built-in xml.etree.ElementTree module.
- Data Extraction: Extracts text from <omsection> and <block> elements.
- Markdown Conversion: Converts XML <table> elements to Markdown.
- CSV Output: Saves extracted data to a CSV file.
- Unit Testing: Includes unit tests using Python’s unittest framework.

## Pre-requisites
 - Python 3.x

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/xml-extractor.git
cd xml-extractor

# Create Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install the package
pip install -e .
```

## Usage

```bash
# Basic usage
python src/xml_extractor/main.py -i omdxe11330.xml

# With explicit output file
python src/xml_extractor/main.py -i omdxe11330.xml -o output.csv

# With custom log file and verbose logging
python src/xml_extractor/main.py -i omdxe11330.xml -l custom.log -v

# Run Unittest
python -m unittest discover -s tests

# Coverage
coverage run -m unittest discover -s tests

# Coverage Report
coverage report
```

## Project Structure

```
xml_extractor/                # Root project directory
│
├── src/                      # Source code
│   ├── xml_extractor/        # Main package
│   │   ├── __init__.py       # Package initialization
│   │   ├── extractor.py      # XmlExtractor class
│   │   └── main.py           # Command-line interface
│   │   └── logging_utils.py  # Logging utilities
│   │
│   └── __init__.py           # Makes src a package
│
├── tests/                    # Test directory
│   ├── __init__.py           # Makes tests a package
│   ├── test_main.py     # Tests for XmlExtractor
│
├── requriments.txt            # Dependencies
└── README.md                 # Project documentation
```

 ## Logging and Coverage

   -The application uses Python's logging module to provide informative messages about the XML parsing process and CSV file  generation. These logs are output to the console.
   -The application uses Python's coverage module to provide test coverage with more than 90% coverage for test cases.
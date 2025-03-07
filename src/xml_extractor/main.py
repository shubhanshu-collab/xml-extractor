#!/usr/bin/env python3
"""
Command-line interface for the XML Extractor tool.
"""

import argparse
import logging
import os
import sys

# Add the src directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from xml_extractor.extractor import XmlExtractor
from xml_extractor.logging_utils import setup_logging




def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Process XML files and extract data to CSV")
    parser.add_argument("--input","-i", help="Input XML file path")
    parser.add_argument("--output", "-o", help="Output CSV file path")
    parser.add_argument("--log", "-l", help="Log file path", default="xml_processor.log")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    # Set up logging
    setup_logging(args.log, args.verbose)

    # Determine output file name if not provided
    output_file = args.output
    if not output_file:
        base_name = os.path.splitext(args.input)[0]
        output_file = f"{base_name}.csv"

    try:
        logging.info("Starting XML processing")
        extractor = XmlExtractor(args.input)
        data = extractor.extract_structured_data()
        extractor.save_to_readme(data, output_file)
        logging.info("XML processing completed successfully")
        print(f"CSV file '{output_file}' generated successfully.")
        return 0
    except Exception as e:
        logging.error(f"Processing failed: {e}", exc_info=True)
        print(f"An error occurred: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
 

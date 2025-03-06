#!/usr/bin/env python3
"""
Logging utilities for the XML Extractor application.
"""
import logging


def setup_logging(log_file, verbose):
    """
    Configure logging with the specified file path and verbosity level.

    Args:
        log_file: Path to the log file
        verbose: Boolean indicating whether to use DEBUG level logging
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=log_file
    )

 
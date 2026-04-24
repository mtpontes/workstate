import pytest
from src.utils.utils import format_file_size

def test_format_size_bytes():
    assert format_file_size(500) == "500.0 B"

def test_format_size_kilobytes():
    assert format_file_size(1024) == "1.0 KB"

def test_format_size_megabytes():
    assert format_file_size(1024 * 1024) == "1.0 MB"

def test_format_size_gigabytes():
    assert format_file_size(1024 * 1024 * 1024) == "1.0 GB"

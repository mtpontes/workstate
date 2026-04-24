import zipfile
from pathlib import Path
import pytest
from src.services import file_service

def test_selective_unzip_specific_file(tmp_path):
    """Garante que apenas o arquivo específico é extraído."""
    zip_path = tmp_path / "test.zip"
    extract_dir = tmp_path / "extracted"
    extract_dir.mkdir()
    
    # Create a zip with multiple files
    with zipfile.ZipFile(zip_path, 'w') as z:
        z.writestr("file1.txt", "content1")
        z.writestr("dir/file2.txt", "content2")
        z.writestr("dir/sub/file3.txt", "content3")
    
    # Test selective extraction of file1.txt
    file_service.unzip(zip_path, extract_to=extract_dir, path_filters=["file1.txt"])
    
    assert (extract_dir / "file1.txt").exists()
    assert not (extract_dir / "dir").exists()

def test_selective_unzip_directory(tmp_path):
    """Garante que uma pasta inteira é extraída."""
    zip_path = tmp_path / "test.zip"
    extract_dir = tmp_path / "extracted"
    extract_dir.mkdir()
    
    with zipfile.ZipFile(zip_path, 'w') as z:
        z.writestr("file1.txt", "content1")
        z.writestr("dir/file2.txt", "content2")
        z.writestr("dir/sub/file3.txt", "content3")
    
    # Test selective extraction of 'dir/'
    file_service.unzip(zip_path, extract_to=extract_dir, path_filters=["dir/"])
    
    assert not (extract_dir / "file1.txt").exists()
    assert (extract_dir / "dir/file2.txt").exists()
    assert (extract_dir / "dir/sub/file3.txt").exists()

def test_selective_unzip_glob_pattern(tmp_path):
    """Garante que padrões glob funcionam."""
    zip_path = tmp_path / "test.zip"
    extract_dir = tmp_path / "extracted"
    extract_dir.mkdir()
    
    with zipfile.ZipFile(zip_path, 'w') as z:
        z.writestr("data1.json", "{}")
        z.writestr("data2.txt", "text")
        z.writestr("logs/app.log", "log")
    
    # Test selective extraction of *.json
    file_service.unzip(zip_path, extract_to=extract_dir, path_filters=["*.json"])
    
    assert (extract_dir / "data1.json").exists()
    assert not (extract_dir / "data2.txt").exists()
    assert not (extract_dir / "logs").exists()

def test_selective_unzip_no_match(tmp_path):
    """Garante que não extrai nada se não houver match."""
    zip_path = tmp_path / "test.zip"
    extract_dir = tmp_path / "extracted"
    extract_dir.mkdir()
    
    with zipfile.ZipFile(zip_path, 'w') as z:
        z.writestr("file.txt", "content")
        
    file_service.unzip(zip_path, extract_to=extract_dir, path_filters=["nonexistent/*"])
    
    # Should be empty
    assert len(list(extract_dir.rglob("*"))) == 0

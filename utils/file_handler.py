"""
File handling utilities for the AI PowerPoint Framework.

This module provides robust file operations, ZIP extraction, and
file system management with proper error handling.
"""

import os
import zipfile
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Tuple
from dataclasses import dataclass
import mimetypes
import hashlib

from core.exceptions import FileHandlingError


@dataclass
class FileInfo:
    """Information about a file."""
    
    path: str
    name: str
    size: int
    extension: str
    mime_type: str
    is_directory: bool = False
    modified_time: Optional[float] = None
    
    @classmethod
    def from_path(cls, file_path: Union[str, Path]) -> "FileInfo":
        """Create FileInfo from file path."""
        path = Path(file_path)
        
        if not path.exists():
            raise FileHandlingError(f"File not found: {file_path}")
        
        stats = path.stat()
        mime_type, _ = mimetypes.guess_type(str(path))
        
        return cls(
            path=str(path),
            name=path.name,
            size=stats.st_size,
            extension=path.suffix.lower(),
            mime_type=mime_type or "application/octet-stream",
            is_directory=path.is_dir(),
            modified_time=stats.st_mtime,
        )


class FileHandler:
    """
    Robust file handling with proper error handling and cleanup.
    
    This class provides safe file operations with automatic cleanup,
    proper error handling, and cross-platform compatibility.
    """
    
    def __init__(self, temp_dir: Optional[str] = None):
        """
        Initialize file handler.
        
        Args:
            temp_dir: Directory for temporary files. If None, uses system temp.
        """
        self.temp_dir = temp_dir or tempfile.gettempdir()
        self.temp_files: List[str] = []
        self.temp_dirs: List[str] = []
    
    def ensure_directory(self, directory: Union[str, Path]) -> str:
        """
        Ensure directory exists, creating it if necessary.
        
        Args:
            directory: Directory path to ensure
            
        Returns:
            str: Absolute path to the directory
        """
        try:
            dir_path = Path(directory).resolve()
            dir_path.mkdir(parents=True, exist_ok=True)
            return str(dir_path)
        except Exception as e:
            raise FileHandlingError(
                f"Failed to create directory: {directory}",
                file_path=str(directory)
            ) from e
    
    def create_temp_file(self, suffix: str = "", prefix: str = "ai_ppt_") -> str:
        """
        Create a temporary file.
        
        Args:
            suffix: File suffix (e.g., ".txt", ".json")
            prefix: File prefix
            
        Returns:
            str: Path to the temporary file
        """
        try:
            fd, temp_path = tempfile.mkstemp(
                suffix=suffix,
                prefix=prefix,
                dir=self.temp_dir
            )
            os.close(fd)  # Close the file descriptor
            
            self.temp_files.append(temp_path)
            return temp_path
        except Exception as e:
            raise FileHandlingError(
                f"Failed to create temporary file with suffix '{suffix}'"
            ) from e
    
    def create_temp_dir(self, prefix: str = "ai_ppt_") -> str:
        """
        Create a temporary directory.
        
        Args:
            prefix: Directory prefix
            
        Returns:
            str: Path to the temporary directory
        """
        try:
            temp_path = tempfile.mkdtemp(prefix=prefix, dir=self.temp_dir)
            self.temp_dirs.append(temp_path)
            return temp_path
        except Exception as e:
            raise FileHandlingError(
                f"Failed to create temporary directory with prefix '{prefix}'"
            ) from e
    
    def read_file(self, file_path: Union[str, Path], encoding: str = "utf-8") -> str:
        """
        Read text file content.
        
        Args:
            file_path: Path to the file
            encoding: Text encoding (default: utf-8)
            
        Returns:
            str: File content
        """
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except Exception as e:
            raise FileHandlingError(
                f"Failed to read file: {file_path}",
                file_path=str(file_path)
            ) from e
    
    def write_file(
        self,
        file_path: Union[str, Path],
        content: str,
        encoding: str = "utf-8",
        create_dirs: bool = True,
    ) -> str:
        """
        Write content to file.
        
        Args:
            file_path: Path to the file
            content: Content to write
            encoding: Text encoding (default: utf-8)
            create_dirs: Whether to create parent directories
            
        Returns:
            str: Absolute path to the written file
        """
        try:
            path = Path(file_path)
            
            if create_dirs:
                path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding=encoding) as file:
                file.write(content)
            
            return str(path.resolve())
        except Exception as e:
            raise FileHandlingError(
                f"Failed to write file: {file_path}",
                file_path=str(file_path)
            ) from e
    
    def copy_file(self, src: Union[str, Path], dst: Union[str, Path]) -> str:
        """
        Copy file from source to destination.
        
        Args:
            src: Source file path
            dst: Destination file path
            
        Returns:
            str: Absolute path to the copied file
        """
        try:
            src_path = Path(src)
            dst_path = Path(dst)
            
            if not src_path.exists():
                raise FileHandlingError(f"Source file not found: {src}")
            
            # Create destination directory if needed
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(src_path, dst_path)
            return str(dst_path.resolve())
        except Exception as e:
            raise FileHandlingError(
                f"Failed to copy file from {src} to {dst}",
                file_path=str(src)
            ) from e
    
    def move_file(self, src: Union[str, Path], dst: Union[str, Path]) -> str:
        """
        Move file from source to destination.
        
        Args:
            src: Source file path
            dst: Destination file path
            
        Returns:
            str: Absolute path to the moved file
        """
        try:
            src_path = Path(src)
            dst_path = Path(dst)
            
            if not src_path.exists():
                raise FileHandlingError(f"Source file not found: {src}")
            
            # Create destination directory if needed
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.move(str(src_path), str(dst_path))
            return str(dst_path.resolve())
        except Exception as e:
            raise FileHandlingError(
                f"Failed to move file from {src} to {dst}",
                file_path=str(src)
            ) from e
    
    def delete_file(self, file_path: Union[str, Path]) -> bool:
        """
        Delete file if it exists.
        
        Args:
            file_path: Path to the file to delete
            
        Returns:
            bool: True if file was deleted or didn't exist
        """
        try:
            path = Path(file_path)
            if path.exists():
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    shutil.rmtree(path)
                return True
            return True  # File didn't exist, consider it "deleted"
        except Exception as e:
            raise FileHandlingError(
                f"Failed to delete file: {file_path}",
                file_path=str(file_path)
            ) from e
    
    def get_file_info(self, file_path: Union[str, Path]) -> FileInfo:
        """
        Get information about a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            FileInfo: File information
        """
        return FileInfo.from_path(file_path)
    
    def list_files(
        self,
        directory: Union[str, Path],
        pattern: str = "*",
        recursive: bool = False,
        include_dirs: bool = False,
    ) -> List[FileInfo]:
        """
        List files in directory.
        
        Args:
            directory: Directory to list
            pattern: File pattern (glob style)
            recursive: Whether to search recursively
            include_dirs: Whether to include directories
            
        Returns:
            List[FileInfo]: List of file information
        """
        try:
            dir_path = Path(directory)
            
            if not dir_path.exists():
                raise FileHandlingError(f"Directory not found: {directory}")
            
            if not dir_path.is_dir():
                raise FileHandlingError(f"Path is not a directory: {directory}")
            
            files = []
            
            if recursive:
                paths = dir_path.rglob(pattern)
            else:
                paths = dir_path.glob(pattern)
            
            for path in paths:
                if path.is_file() or (include_dirs and path.is_dir()):
                    files.append(FileInfo.from_path(path))
            
            return files
        except Exception as e:
            raise FileHandlingError(
                f"Failed to list files in directory: {directory}",
                file_path=str(directory)
            ) from e
    
    def get_file_hash(self, file_path: Union[str, Path], algorithm: str = "sha256") -> str:
        """
        Get file hash.
        
        Args:
            file_path: Path to the file
            algorithm: Hash algorithm (md5, sha1, sha256, etc.)
            
        Returns:
            str: File hash
        """
        try:
            hash_algo = hashlib.new(algorithm)
            
            with open(file_path, 'rb') as file:
                for chunk in iter(lambda: file.read(4096), b""):
                    hash_algo.update(chunk)
            
            return hash_algo.hexdigest()
        except Exception as e:
            raise FileHandlingError(
                f"Failed to calculate {algorithm} hash for file: {file_path}",
                file_path=str(file_path)
            ) from e
    
    def cleanup(self) -> None:
        """Clean up temporary files and directories."""
        # Clean up temporary files
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            except Exception:
                pass  # Ignore cleanup errors
        
        # Clean up temporary directories
        for temp_dir in self.temp_dirs:
            try:
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
            except Exception:
                pass  # Ignore cleanup errors
        
        self.temp_files.clear()
        self.temp_dirs.clear()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.cleanup()


class ZipExtractor:
    """
    Robust ZIP file extraction with security checks.
    
    This class provides safe ZIP extraction with path traversal protection,
    file size limits, and proper error handling.
    """
    
    def __init__(
        self,
        max_file_size: int = 100 * 1024 * 1024,  # 100MB
        max_total_size: int = 500 * 1024 * 1024,  # 500MB
        allowed_extensions: Optional[List[str]] = None,
    ):
        """
        Initialize ZIP extractor.
        
        Args:
            max_file_size: Maximum size for individual files
            max_total_size: Maximum total size of extracted files
            allowed_extensions: List of allowed file extensions
        """
        self.max_file_size = max_file_size
        self.max_total_size = max_total_size
        self.allowed_extensions = allowed_extensions or []
        self.file_handler = FileHandler()
    
    def extract_zip(
        self,
        zip_path: Union[str, Path],
        extract_to: Optional[Union[str, Path]] = None,
        preserve_structure: bool = True,
    ) -> Dict[str, Any]:
        """
        Extract ZIP file with security checks.
        
        Args:
            zip_path: Path to ZIP file
            extract_to: Directory to extract to (if None, creates temp dir)
            preserve_structure: Whether to preserve directory structure
            
        Returns:
            dict: Extraction results with file list and metadata
        """
        try:
            zip_path = Path(zip_path)
            
            if not zip_path.exists():
                raise FileHandlingError(f"ZIP file not found: {zip_path}")
            
            if extract_to is None:
                extract_to = self.file_handler.create_temp_dir("zip_extract_")
            else:
                extract_to = self.file_handler.ensure_directory(extract_to)
            
            extraction_results = {
                "extract_path": extract_to,
                "files": [],
                "total_size": 0,
                "file_count": 0,
                "errors": [],
            }
            
            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                # Check ZIP file integrity
                if zip_file.testzip() is not None:
                    raise FileHandlingError(f"ZIP file is corrupted: {zip_path}")
                
                # Get file list and validate
                file_list = zip_file.infolist()
                total_size = sum(info.file_size for info in file_list)
                
                if total_size > self.max_total_size:
                    raise FileHandlingError(
                        f"ZIP file too large: {total_size} bytes (max: {self.max_total_size})"
                    )
                
                # Extract files
                for info in file_list:
                    try:
                        self._extract_file(zip_file, info, extract_to, preserve_structure)
                        extraction_results["files"].append({
                            "name": info.filename,
                            "size": info.file_size,
                            "path": os.path.join(extract_to, info.filename)
                        })
                        extraction_results["total_size"] += info.file_size
                        extraction_results["file_count"] += 1
                    except Exception as e:
                        extraction_results["errors"].append({
                            "file": info.filename,
                            "error": str(e)
                        })
            
            return extraction_results
            
        except Exception as e:
            raise FileHandlingError(
                f"Failed to extract ZIP file: {zip_path}",
                file_path=str(zip_path)
            ) from e
    
    def _extract_file(
        self,
        zip_file: zipfile.ZipFile,
        file_info: zipfile.ZipInfo,
        extract_to: str,
        preserve_structure: bool,
    ) -> None:
        """Extract a single file from ZIP with security checks."""
        # Security check: prevent path traversal
        if self._is_path_traversal(file_info.filename):
            raise FileHandlingError(f"Path traversal attempt detected: {file_info.filename}")
        
        # Check file size
        if file_info.file_size > self.max_file_size:
            raise FileHandlingError(
                f"File too large: {file_info.filename} ({file_info.file_size} bytes)"
            )
        
        # Check file extension
        if self.allowed_extensions:
            file_ext = os.path.splitext(file_info.filename)[1].lower()
            if file_ext not in self.allowed_extensions:
                raise FileHandlingError(
                    f"File extension not allowed: {file_info.filename} ({file_ext})"
                )
        
        # Skip directories
        if file_info.is_dir():
            return
        
        # Determine extraction path
        if preserve_structure:
            extract_path = os.path.join(extract_to, file_info.filename)
        else:
            extract_path = os.path.join(extract_to, os.path.basename(file_info.filename))
        
        # Create directory if needed
        os.makedirs(os.path.dirname(extract_path), exist_ok=True)
        
        # Extract file
        with zip_file.open(file_info) as source, open(extract_path, 'wb') as target:
            shutil.copyfileobj(source, target)
    
    def _is_path_traversal(self, filename: str) -> bool:
        """Check if filename contains path traversal attempts."""
        # Normalize path and check for traversal
        normalized = os.path.normpath(filename)
        return normalized.startswith('..') or os.path.isabs(normalized)
    
    def analyze_zip(self, zip_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Analyze ZIP file without extracting.
        
        Args:
            zip_path: Path to ZIP file
            
        Returns:
            dict: ZIP file analysis
        """
        try:
            zip_path = Path(zip_path)
            
            if not zip_path.exists():
                raise FileHandlingError(f"ZIP file not found: {zip_path}")
            
            analysis = {
                "file_count": 0,
                "total_size": 0,
                "compressed_size": 0,
                "files": [],
                "directories": [],
                "file_types": {},
                "largest_file": None,
                "compression_ratio": 0.0,
            }
            
            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                for info in zip_file.infolist():
                    if info.is_dir():
                        analysis["directories"].append(info.filename)
                    else:
                        analysis["file_count"] += 1
                        analysis["total_size"] += info.file_size
                        analysis["compressed_size"] += info.compress_size
                        
                        # Track file types
                        ext = os.path.splitext(info.filename)[1].lower()
                        analysis["file_types"][ext] = analysis["file_types"].get(ext, 0) + 1
                        
                        # Track largest file
                        if (analysis["largest_file"] is None or 
                            info.file_size > analysis["largest_file"]["size"]):
                            analysis["largest_file"] = {
                                "name": info.filename,
                                "size": info.file_size
                            }
                        
                        analysis["files"].append({
                            "name": info.filename,
                            "size": info.file_size,
                            "compressed_size": info.compress_size,
                            "modified": info.date_time,
                        })
                
                # Calculate compression ratio
                if analysis["total_size"] > 0:
                    analysis["compression_ratio"] = (
                        1 - (analysis["compressed_size"] / analysis["total_size"])
                    )
            
            return analysis
            
        except Exception as e:
            raise FileHandlingError(
                f"Failed to analyze ZIP file: {zip_path}",
                file_path=str(zip_path)
            ) from e

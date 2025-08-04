"""
Input validation utilities for the AI PowerPoint Framework.

This module provides comprehensive validation functions for various input types
and data structures used throughout the framework.
"""

import re
import os
from typing import Any, Dict, List, Optional, Union, Tuple
from pathlib import Path
from urllib.parse import urlparse

from core.exceptions import ValidationError


class InputValidator:
    """Main validator class for input validation."""
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """
        Validate API key format.
        
        Args:
            api_key: The API key to validate
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If API key is invalid
        """
        if not api_key:
            raise ValidationError("API key cannot be empty")
        
        if not isinstance(api_key, str):
            raise ValidationError("API key must be a string")
        
        # Basic format validation (length and characters)
        if len(api_key) < 20:
            raise ValidationError("API key appears to be too short")
        
        if not re.match(r'^[A-Za-z0-9_-]+$', api_key):
            raise ValidationError("API key contains invalid characters")
        
        return True
    
    @staticmethod
    def validate_file_path(file_path: Union[str, Path]) -> bool:
        """
        Validate file path.
        
        Args:
            file_path: Path to validate
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If path is invalid
        """
        if not file_path:
            raise ValidationError("File path cannot be empty")
        
        path = Path(file_path)
        
        # Check if path is absolute or relative
        if not path.is_absolute() and not path.exists():
            # Try to resolve relative path
            try:
                path = path.resolve()
            except Exception:
                raise ValidationError(f"Cannot resolve path: {file_path}")
        
        # Check if parent directory exists
        if not path.parent.exists():
            raise ValidationError(f"Parent directory does not exist: {path.parent}")
        
        return True
    
    @staticmethod
    def validate_zip_file(file_path: Union[str, Path]) -> bool:
        """
        Validate ZIP file.
        
        Args:
            file_path: Path to ZIP file
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If ZIP file is invalid
        """
        InputValidator.validate_file_path(file_path)
        
        path = Path(file_path)
        
        if not path.exists():
            raise ValidationError(f"ZIP file does not exist: {file_path}")
        
        if path.suffix.lower() != '.zip':
            raise ValidationError(f"File is not a ZIP file: {file_path}")
        
        # Check if file is readable
        try:
            with open(path, 'rb') as f:
                # Read first few bytes to check ZIP signature
                header = f.read(4)
                if header != b'PK\x03\x04' and header != b'PK\x05\x06':
                    raise ValidationError(f"Invalid ZIP file format: {file_path}")
        except Exception as e:
            raise ValidationError(f"Cannot read ZIP file: {file_path} - {str(e)}")
        
        return True
    
    @staticmethod
    def validate_slide_data(slide_data: Dict[str, Any]) -> bool:
        """
        Validate slide data structure.
        
        Args:
            slide_data: Slide data dictionary
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If slide data is invalid
        """
        if not isinstance(slide_data, dict):
            raise ValidationError("Slide data must be a dictionary")
        
        # Check for required fields
        if 'title' not in slide_data:
            raise ValidationError("Slide data must contain 'title' field")
        
        if not isinstance(slide_data['title'], str):
            raise ValidationError("Slide title must be a string")
        
        if not slide_data['title'].strip():
            raise ValidationError("Slide title cannot be empty")
        
        # Validate points if present
        if 'points' in slide_data:
            if not isinstance(slide_data['points'], list):
                raise ValidationError("Slide points must be a list")
            
            for i, point in enumerate(slide_data['points']):
                if not isinstance(point, str):
                    raise ValidationError(f"Point {i} must be a string")
                
                if not point.strip():
                    raise ValidationError(f"Point {i} cannot be empty")
        
        # Validate content if present
        if 'content' in slide_data:
            content = slide_data['content']
            if not isinstance(content, (str, list, dict)):
                raise ValidationError("Slide content must be string, list, or dict")
        
        return True
    
    @staticmethod
    def validate_presentation_config(config: Dict[str, Any]) -> bool:
        """
        Validate presentation configuration.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If configuration is invalid
        """
        if not isinstance(config, dict):
            raise ValidationError("Configuration must be a dictionary")
        
        # Validate max_slides
        if 'max_slides' in config:
            max_slides = config['max_slides']
            if not isinstance(max_slides, int):
                raise ValidationError("max_slides must be an integer")
            
            if max_slides < 1 or max_slides > 50:
                raise ValidationError("max_slides must be between 1 and 50")
        
        # Validate max_points_per_slide
        if 'max_points_per_slide' in config:
            max_points = config['max_points_per_slide']
            if not isinstance(max_points, int):
                raise ValidationError("max_points_per_slide must be an integer")
            
            if max_points < 1 or max_points > 20:
                raise ValidationError("max_points_per_slide must be between 1 and 20")
        
        # Validate theme
        if 'theme' in config:
            theme = config['theme']
            if not isinstance(theme, str):
                raise ValidationError("theme must be a string")
        
        # Validate boolean flags
        boolean_fields = ['enable_advanced_visuals', 'debug_mode', 'use_com_engine']
        for field in boolean_fields:
            if field in config:
                if not isinstance(config[field], bool):
                    raise ValidationError(f"{field} must be a boolean")
        
        return True
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate URL format.
        
        Args:
            url: URL to validate
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If URL is invalid
        """
        if not url:
            raise ValidationError("URL cannot be empty")
        
        if not isinstance(url, str):
            raise ValidationError("URL must be a string")
        
        try:
            result = urlparse(url)
            if not result.scheme or not result.netloc:
                raise ValidationError("URL must have scheme and netloc")
            
            if result.scheme not in ['http', 'https']:
                raise ValidationError("URL scheme must be http or https")
            
        except Exception as e:
            raise ValidationError(f"Invalid URL format: {str(e)}")
        
        return True
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email address format.
        
        Args:
            email: Email address to validate
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If email is invalid
        """
        if not email:
            raise ValidationError("Email cannot be empty")
        
        if not isinstance(email, str):
            raise ValidationError("Email must be a string")
        
        # Basic email regex pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            raise ValidationError("Invalid email format")
        
        return True
    
    @staticmethod
    def validate_color_hex(color: str) -> bool:
        """
        Validate hex color format.
        
        Args:
            color: Hex color string
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If color is invalid
        """
        if not color:
            raise ValidationError("Color cannot be empty")
        
        if not isinstance(color, str):
            raise ValidationError("Color must be a string")
        
        # Remove # if present
        if color.startswith('#'):
            color = color[1:]
        
        # Check if valid hex
        if not re.match(r'^[0-9A-Fa-f]{6}$', color):
            raise ValidationError("Invalid hex color format (expected: #RRGGBB)")
        
        return True
    
    @staticmethod
    def validate_numeric_range(value: Union[int, float], min_val: Union[int, float], 
                             max_val: Union[int, float], field_name: str = "value") -> bool:
        """
        Validate numeric value is within range.
        
        Args:
            value: Value to validate
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            field_name: Name of the field for error messages
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If value is out of range
        """
        if not isinstance(value, (int, float)):
            raise ValidationError(f"{field_name} must be a number")
        
        if value < min_val or value > max_val:
            raise ValidationError(f"{field_name} must be between {min_val} and {max_val}")
        
        return True
    
    @staticmethod
    def validate_string_length(text: str, min_length: int = 0, max_length: int = 1000, 
                             field_name: str = "text") -> bool:
        """
        Validate string length.
        
        Args:
            text: Text to validate
            min_length: Minimum length
            max_length: Maximum length
            field_name: Name of the field for error messages
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If length is invalid
        """
        if not isinstance(text, str):
            raise ValidationError(f"{field_name} must be a string")
        
        if len(text) < min_length:
            raise ValidationError(f"{field_name} must be at least {min_length} characters")
        
        if len(text) > max_length:
            raise ValidationError(f"{field_name} must be no more than {max_length} characters")
        
        return True
    
    @staticmethod
    def validate_list_items(items: List[Any], item_type: type, field_name: str = "items") -> bool:
        """
        Validate list items are of correct type.
        
        Args:
            items: List to validate
            item_type: Expected type of items
            field_name: Name of the field for error messages
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If items are invalid
        """
        if not isinstance(items, list):
            raise ValidationError(f"{field_name} must be a list")
        
        for i, item in enumerate(items):
            if not isinstance(item, item_type):
                raise ValidationError(f"{field_name}[{i}] must be of type {item_type.__name__}")
        
        return True


class DataValidator:
    """Validator for complex data structures."""
    
    @staticmethod
    def validate_chart_data(chart_data: Dict[str, Any]) -> bool:
        """
        Validate chart data structure.
        
        Args:
            chart_data: Chart data dictionary
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If chart data is invalid
        """
        if not isinstance(chart_data, dict):
            raise ValidationError("Chart data must be a dictionary")
        
        # Check required fields
        required_fields = ['type', 'data']
        for field in required_fields:
            if field not in chart_data:
                raise ValidationError(f"Chart data must contain '{field}' field")
        
        # Validate chart type
        valid_types = ['bar', 'line', 'pie', 'column', 'area', 'scatter']
        if chart_data['type'] not in valid_types:
            raise ValidationError(f"Chart type must be one of: {', '.join(valid_types)}")
        
        # Validate data
        data = chart_data['data']
        if not isinstance(data, dict):
            raise ValidationError("Chart data must be a dictionary")
        
        if not data:
            raise ValidationError("Chart data cannot be empty")
        
        # Validate data values
        for key, value in data.items():
            if not isinstance(key, str):
                raise ValidationError("Chart data keys must be strings")
            
            if not isinstance(value, (int, float)):
                raise ValidationError("Chart data values must be numbers")
        
        return True
    
    @staticmethod
    def validate_metrics_data(metrics_data: Dict[str, Any]) -> bool:
        """
        Validate metrics data structure.
        
        Args:
            metrics_data: Metrics data dictionary
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If metrics data is invalid
        """
        if not isinstance(metrics_data, dict):
            raise ValidationError("Metrics data must be a dictionary")
        
        if 'metrics' in metrics_data:
            metrics = metrics_data['metrics']
            if not isinstance(metrics, list):
                raise ValidationError("Metrics must be a list")
            
            for i, metric in enumerate(metrics):
                if not isinstance(metric, dict):
                    raise ValidationError(f"Metric {i} must be a dictionary")
                
                if 'label' not in metric:
                    raise ValidationError(f"Metric {i} must have a 'label' field")
                
                if 'value' not in metric:
                    raise ValidationError(f"Metric {i} must have a 'value' field")
                
                if not isinstance(metric['value'], (int, float, str)):
                    raise ValidationError(f"Metric {i} value must be a number or string")
        
        return True
    
    @staticmethod
    def validate_feature_data(feature_data: Dict[str, Any]) -> bool:
        """
        Validate feature data structure.
        
        Args:
            feature_data: Feature data dictionary
            
        Returns:
            bool: True if valid
            
        Raises:
            ValidationError: If feature data is invalid
        """
        if not isinstance(feature_data, dict):
            raise ValidationError("Feature data must be a dictionary")
        
        if 'features' in feature_data:
            features = feature_data['features']
            if not isinstance(features, list):
                raise ValidationError("Features must be a list")
            
            for i, feature in enumerate(features):
                if isinstance(feature, dict):
                    if 'title' not in feature:
                        raise ValidationError(f"Feature {i} must have a 'title' field")
                    
                    if not isinstance(feature['title'], str):
                        raise ValidationError(f"Feature {i} title must be a string")
                
                elif not isinstance(feature, str):
                    raise ValidationError(f"Feature {i} must be a string or dictionary")
        
        return True


# Convenience functions for common validations
def validate_input_data(data: Dict[str, Any], data_type: str) -> bool:
    """
    Validate input data based on type.
    
    Args:
        data: Data to validate
        data_type: Type of data ('slide', 'chart', 'metrics', 'features')
        
    Returns:
        bool: True if valid
        
    Raises:
        ValidationError: If data is invalid
    """
    validators = {
        'slide': InputValidator.validate_slide_data,
        'chart': DataValidator.validate_chart_data,
        'metrics': DataValidator.validate_metrics_data,
        'features': DataValidator.validate_feature_data,
    }
    
    if data_type not in validators:
        raise ValidationError(f"Unknown data type: {data_type}")
    
    return validators[data_type](data)


def validate_file_format(file_path: Union[str, Path], allowed_extensions: List[str]) -> bool:
    """
    Validate file format against allowed extensions.
    
    Args:
        file_path: Path to file
        allowed_extensions: List of allowed extensions (e.g., ['.zip', '.pptx'])
        
    Returns:
        bool: True if valid
        
    Raises:
        ValidationError: If file format is invalid
    """
    path = Path(file_path)
    
    if path.suffix.lower() not in [ext.lower() for ext in allowed_extensions]:
        raise ValidationError(f"File format not allowed. Allowed: {', '.join(allowed_extensions)}")
    
    return True


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file system operations.
    
    Args:
        filename: Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing whitespace and dots
    sanitized = sanitized.strip(' .')
    
    # Limit length
    if len(sanitized) > 255:
        name, ext = os.path.splitext(sanitized)
        sanitized = name[:255-len(ext)] + ext
    
    # Ensure it's not empty
    if not sanitized:
        sanitized = "untitled"
    
    return sanitized


def validate_and_sanitize_input(data: Any, validation_rules: Dict[str, Any]) -> Any:
    """
    Validate and sanitize input data according to rules.
    
    Args:
        data: Data to validate and sanitize
        validation_rules: Dictionary of validation rules
        
    Returns:
        Any: Sanitized data
        
    Raises:
        ValidationError: If validation fails
    """
    if 'type' in validation_rules:
        if not isinstance(data, validation_rules['type']):
            raise ValidationError(f"Data must be of type {validation_rules['type'].__name__}")
    
    if 'required' in validation_rules and validation_rules['required']:
        if data is None or (isinstance(data, str) and not data.strip()):
            raise ValidationError("Data is required")
    
    if isinstance(data, str):
        if 'max_length' in validation_rules:
            InputValidator.validate_string_length(data, 0, validation_rules['max_length'])
        
        if 'pattern' in validation_rules:
            if not re.match(validation_rules['pattern'], data):
                raise ValidationError("Data does not match required pattern")
        
        # Sanitize string
        data = data.strip()
    
    if isinstance(data, (int, float)):
        if 'min_value' in validation_rules and 'max_value' in validation_rules:
            InputValidator.validate_numeric_range(
                data, validation_rules['min_value'], validation_rules['max_value']
            )
    
    return data

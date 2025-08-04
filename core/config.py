"""
Core configuration management for the AI PowerPoint Framework.

This module handles environment variables, API keys, and global framework settings.
Extracted from the original smartArt.py monolithic file for better maintainability.
"""

import os
import tempfile
import importlib.util
from dataclasses import dataclass
from typing import Optional

# Load environment variables from .env file if dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv is optional - continue without it
    pass


@dataclass
class FrameworkConfig:
    """
    Central configuration class for the AI PowerPoint Framework.

    This class manages all configuration settings including API keys,
    file paths, processing options, and feature flags.

    Attributes:
        gemini_api_key (str): Google Gemini API key for AI analysis
        max_retries (int): Maximum number of retry attempts for API calls
        retry_delay (float): Base delay between retry attempts in seconds
        temp_dir (str): Directory for temporary files
        enable_com_powerpoint (bool): Whether to use COM-based PowerPoint
        enable_advanced_visuals (bool): Whether to create advanced visual elements
        max_slides (int): Maximum number of slides to generate
        max_points_per_slide (int): Maximum bullet points per slide
        debug_mode (bool): Enable debug logging and detailed error messages
    """

    # API Configuration
    gemini_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    max_retries: int = 3
    retry_delay: float = 1.0

    # File and Path Configuration
    temp_dir: Optional[str] = None
    output_dir: Optional[str] = None

    # PowerPoint Engine Configuration
    enable_com_powerpoint: bool = True
    enable_python_pptx_fallback: bool = True

    # Visual Features Configuration
    enable_advanced_visuals: bool = True
    enable_image_generation: bool = True
    enable_smartart: bool = True
    enable_custom_backgrounds: bool = True

    # Content Limits
    max_slides: int = 10
    max_points_per_slide: int = 6
    max_content_length: int = 50000  # Maximum characters to analyze

    # Processing Options
    debug_mode: bool = False
    enable_caching: bool = True
    parallel_processing: bool = False

    def __post_init__(self):
        """Initialize configuration with environment variables and defaults."""
        # Load API key from environment if not provided
        if self.gemini_api_key is None:
            self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        
        if self.openai_api_key is None:
            self.openai_api_key = os.getenv("OPENAI_API_KEY")

        # Set default directories if not provided
        if self.temp_dir is None:
            import tempfile
            self.temp_dir = tempfile.gettempdir()

        if self.output_dir is None:
            self.output_dir = self.temp_dir

        # Note: API key validation is now optional to allow testing without AI features

    @classmethod
    def from_env(cls) -> "FrameworkConfig":
        """
        Create configuration from environment variables.

        Returns:
            FrameworkConfig: Configuration instance with values from environment
        """
        return cls(
            gemini_api_key=os.getenv("GEMINI_API_KEY"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            max_retries=int(os.getenv("AI_PPT_MAX_RETRIES", "3")),
            retry_delay=float(os.getenv("AI_PPT_RETRY_DELAY", "1.0")),
            temp_dir=os.getenv("AI_PPT_TEMP_DIR") or tempfile.gettempdir(),
            output_dir=os.getenv("AI_PPT_OUTPUT_DIR") or tempfile.gettempdir(),
            enable_com_powerpoint=os.getenv("AI_PPT_ENABLE_COM", "true").lower()
            == "true",
            enable_advanced_visuals=os.getenv("AI_PPT_ADVANCED_VISUALS", "true").lower()
            == "true",
            max_slides=int(os.getenv("AI_PPT_MAX_SLIDES", "10")),
            max_points_per_slide=int(os.getenv("AI_PPT_MAX_POINTS", "6")),
            debug_mode=os.getenv("AI_PPT_DEBUG", "false").lower() == "true",
        )

    def validate(self) -> bool:
        """
        Validate the configuration settings.

        Returns:
            bool: True if configuration is valid

        Raises:
            ValueError: If configuration is invalid
        """
        # Note: API key is now optional to allow testing without AI features
        # A warning will be shown if missing, but it won't prevent operation
        
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")

        if self.retry_delay < 0:
            raise ValueError("retry_delay must be non-negative")

        if self.max_slides <= 0:
            raise ValueError("max_slides must be positive")

        if self.max_points_per_slide <= 0:
            raise ValueError("max_points_per_slide must be positive")

        return True

    def to_dict(self) -> dict:
        """
        Convert configuration to dictionary.

        Returns:
            dict: Configuration as dictionary (excluding sensitive data)
        """
        config_dict = {}
        for key, value in self.__dict__.items():
            # Mask sensitive information
            if "api_key" in key.lower() or "password" in key.lower():
                config_dict[key] = "***masked***" if value else None
            else:
                config_dict[key] = value
        return config_dict


# Global configuration instance (can be overridden)
_global_config: Optional[FrameworkConfig] = None


def get_config() -> FrameworkConfig:
    """
    Get the global framework configuration.

    Returns:
        FrameworkConfig: The global configuration instance
    """
    global _global_config
    if _global_config is None:
        _global_config = FrameworkConfig.from_env()
    return _global_config


def set_config(config: FrameworkConfig) -> None:
    """
    Set the global framework configuration.

    Args:
        config (FrameworkConfig): New configuration to use globally
    """
    global _global_config
    config.validate()
    _global_config = config


# Environment validation functions
def check_dependencies() -> dict:
    """
    Check if all required dependencies are available.

    Returns:
        dict: Status of each dependency
    """
    dependencies = {
        "streamlit": False,
        "google.genai": False,
        "win32com.client": False,
        "python-pptx": False,
        "dotenv": False,
    }

    # Check each dependency
    dependencies["streamlit"] = importlib.util.find_spec("streamlit") is not None
    dependencies["google.genai"] = importlib.util.find_spec("google.genai") is not None
    dependencies["win32com.client"] = importlib.util.find_spec("win32com.client") is not None
    dependencies["python-pptx"] = importlib.util.find_spec("pptx") is not None
    dependencies["dotenv"] = importlib.util.find_spec("dotenv") is not None

    return dependencies


def validate_environment() -> bool:
    """
    Validate that the environment is properly configured.

    Returns:
        bool: True if environment is valid

    Raises:
        RuntimeError: If environment is not properly configured
    """
    # Check dependencies
    deps = check_dependencies()

    missing_required = []
    if not deps["streamlit"]:
        missing_required.append("streamlit")

    if missing_required:
        raise RuntimeError(
            f"Missing required dependencies: {', '.join(missing_required)}. "
            f"Please install them with: pip install {' '.join(missing_required)}"
        )

    return True

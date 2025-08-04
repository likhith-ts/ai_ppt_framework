"""
Core module initialization for the AI PowerPoint Framework.

This module provides access to core configuration, constants, and exceptions.
"""

from .config import FrameworkConfig, get_config, set_config, validate_environment
from .constants import (
    SLIDE_WIDTH,
    SLIDE_HEIGHT,
    SPACING_UNIT,
    MARGIN_SMALL,
    MARGIN_MEDIUM,
    MARGIN_LARGE,
    CONTENT_WIDTH,
    CONTENT_HEIGHT,
    LayoutConstants,
    TypographyConstants,
    ComponentConstants,
)
from .exceptions import (
    FrameworkError,
    ConfigurationError,
    AIClientError,
    PresentationGenerationError,
    SlideBuilderError,
    DesignSystemError,
    FileHandlingError,
    ContentAnalysisError,
    ValidationError,
    DependencyError,
)

__all__ = [
    # Configuration
    "FrameworkConfig",
    "get_config",
    "set_config",
    "validate_environment",
    # Constants
    "SLIDE_WIDTH",
    "SLIDE_HEIGHT",
    "SPACING_UNIT",
    "MARGIN_SMALL",
    "MARGIN_MEDIUM",
    "MARGIN_LARGE",
    "CONTENT_WIDTH",
    "CONTENT_HEIGHT",
    "LayoutConstants",
    "TypographyConstants",
    "ComponentConstants",
    # Exceptions
    "FrameworkError",
    "ConfigurationError",
    "AIClientError",
    "PresentationGenerationError",
    "SlideBuilderError",
    "DesignSystemError",
    "FileHandlingError",
    "ContentAnalysisError",
    "ValidationError",
    "DependencyError",
]

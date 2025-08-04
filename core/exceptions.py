"""
Custom exceptions for the AI PowerPoint Framework.

This module defines all custom exceptions used throughout the framework,
providing clear error handling and debugging capabilities.
"""

from typing import Optional


class FrameworkError(Exception):
    """
    Base exception class for all AI PowerPoint Framework errors.

    This is the base class for all custom exceptions in the framework.
    It provides a foundation for error handling and can include additional
    context and debugging information.

    Attributes:
        message (str): The error message
        error_code (str): Optional error code for categorization
        context (dict): Additional context information
    """

    def __init__(self, message: str, error_code: Optional[str] = None, context: Optional[dict] = None):
        """
        Initialize the framework error.

        Args:
            message (str): Human-readable error message
            error_code (str, optional): Machine-readable error code
            context (dict, optional): Additional context information
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "FRAMEWORK_ERROR"
        self.context = context or {}

    def __str__(self) -> str:
        """Return a formatted error message."""
        if self.context:
            return f"[{self.error_code}] {self.message} | Context: {self.context}"
        return f"[{self.error_code}] {self.message}"


class ConfigurationError(FrameworkError):
    """
    Exception raised for configuration-related errors.

    This exception is raised when there are issues with the framework
    configuration, such as missing API keys, invalid settings, or
    environment setup problems.
    """

    def __init__(self, message: str, context: Optional[dict] = None):
        super().__init__(message, error_code="CONFIG_ERROR", context=context)


class AIClientError(FrameworkError):
    """
    Exception raised for AI client-related errors.

    This exception is raised when there are issues with AI service
    communication, such as API failures, authentication errors,
    or response parsing problems.
    """

    def __init__(self, message: str, context: Optional[dict] = None):
        super().__init__(message, error_code="AI_CLIENT_ERROR", context=context)


class PresentationGenerationError(FrameworkError):
    """
    Exception raised for presentation generation errors.

    This exception is raised when there are issues creating or
    saving PowerPoint presentations, such as COM errors, file
    system issues, or template problems.
    """

    def __init__(self, message: str, context: Optional[dict] = None):
        super().__init__(message, error_code="PRESENTATION_ERROR", context=context)


class SlideBuilderError(FrameworkError):
    """
    Exception raised for slide builder errors.

    This exception is raised when there are issues with specific
    slide builders, such as layout failures, content formatting
    problems, or visual element creation errors.
    """

    def __init__(self, message: str, slide_type: Optional[str] = None, context: Optional[dict] = None):
        context = context or {}
        if slide_type:
            context["slide_type"] = slide_type

        super().__init__(message, error_code="SLIDE_BUILDER_ERROR", context=context)


class DesignSystemError(FrameworkError):
    """
    Exception raised for design system errors.

    This exception is raised when there are issues with the design
    system components, such as color palette problems, typography
    errors, or layout calculation failures.
    """

    def __init__(self, message: str, component: Optional[str] = None, context: Optional[dict] = None):
        context = context or {}
        if component:
            context["component"] = component

        super().__init__(message, error_code="DESIGN_SYSTEM_ERROR", context=context)


class FileHandlingError(FrameworkError):
    """
    Exception raised for file handling errors.

    This exception is raised when there are issues with file
    operations, such as ZIP extraction failures, file reading
    errors, or permission problems.
    """

    def __init__(self, message: str, file_path: Optional[str] = None, context: Optional[dict] = None):
        context = context or {}
        if file_path:
            context["file_path"] = file_path

        super().__init__(message, error_code="FILE_HANDLING_ERROR", context=context)


class ContentAnalysisError(FrameworkError):
    """
    Exception raised for content analysis errors.

    This exception is raised when there are issues analyzing
    repository content, such as parsing failures, content
    validation errors, or structure detection problems.
    """

    def __init__(self, message: str, content_type: Optional[str] = None, context: Optional[dict] = None):
        context = context or {}
        if content_type:
            context["content_type"] = content_type

        super().__init__(message, error_code="CONTENT_ANALYSIS_ERROR", context=context)


class ValidationError(FrameworkError):
    """
    Exception raised for validation errors.

    This exception is raised when input validation fails,
    such as invalid parameters, malformed data, or constraint
    violations.
    """

    def __init__(
        self, message: str, field: Optional[str] = None, value: Optional[str] = None, context: Optional[dict] = None
    ):
        context = context or {}
        if field:
            context["field"] = field
        if value:
            context["value"] = str(value)

        super().__init__(message, error_code="VALIDATION_ERROR", context=context)


class DependencyError(FrameworkError):
    """
    Exception raised for dependency-related errors.

    This exception is raised when required dependencies are
    missing or incompatible, such as missing Python packages
    or incorrect versions.
    """

    def __init__(self, message: str, dependency: Optional[str] = None, context: Optional[dict] = None):
        context = context or {}
        if dependency:
            context["dependency"] = dependency

        super().__init__(message, error_code="DEPENDENCY_ERROR", context=context)


# Error context helpers
def create_error_context(**kwargs) -> dict:
    """
    Create an error context dictionary with common debugging information.

    Args:
        **kwargs: Additional context key-value pairs

    Returns:
        dict: Error context with timestamp and provided information
    """
    import time
    import traceback

    context = {"timestamp": time.time(), "traceback": traceback.format_exc(), **kwargs}

    return context


def handle_framework_error(error: Exception, operation: Optional[str] = None) -> FrameworkError:
    """
    Convert a generic exception to a FrameworkError with context.

    Args:
        error (Exception): The original exception
        operation (str, optional): Description of the operation that failed

    Returns:
        FrameworkError: Framework-specific error with context
    """
    context = create_error_context(
        original_error=str(error), error_type=type(error).__name__, operation=operation
    )

    # Try to preserve the original error type if it's already a FrameworkError
    if isinstance(error, FrameworkError):
        return error

    # Convert common exceptions to specific framework errors
    if isinstance(error, (FileNotFoundError, PermissionError, IOError)):
        return FileHandlingError(
            f"File operation failed: {str(error)}", context=context
        )

    if isinstance(error, (ValueError, TypeError)):
        return ValidationError(f"Validation failed: {str(error)}", context=context)

    if isinstance(error, ImportError):
        return DependencyError(f"Dependency error: {str(error)}", context=context)

    # Default to generic framework error
    return FrameworkError(f"Operation failed: {str(error)}", context=context)


# Exception hierarchy for easy catching
__all__ = [
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
    "create_error_context",
    "handle_framework_error",
]

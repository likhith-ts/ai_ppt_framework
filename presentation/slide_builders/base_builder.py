"""
Base slide builder for the AI PowerPoint Framework.

This module defines the abstract interface for all slide builders,
providing common functionality and ensuring consistent behavior.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any

from design.themes import DesignTheme
from design.color_system import DesignPalettes
from core.exceptions import SlideBuilderError


class BaseSlideBuilder(ABC):
    """
    Abstract base class for specialized slide builders.

    This class defines the interface that all slide builders must implement,
    providing common utilities and ensuring consistent slide creation.
    """

    def __init__(self, theme: DesignTheme = DesignTheme.CORPORATE_MODERN):
        """
        Initialize the slide builder.

        Args:
            theme: Design theme to apply to slides
        """
        self.theme = theme
        self.palette = DesignPalettes.get_palette(theme)
        self.slides_created = 0

    @abstractmethod
    def build_slide(self, slide_data: Dict[str, Any], presentation_engine: Any) -> bool:
        """
        Build a slide using the specified presentation engine.

        Args:
            slide_data: Dictionary containing slide content and metadata
            presentation_engine: Engine instance (COM or python-pptx)

        Returns:
            True if slide was created successfully

        Raises:
            SlideBuilderError: If slide creation fails
        """
        pass

    def validate_slide_data(self, slide_data: Dict[str, Any]) -> bool:
        """
        Validate that slide data contains required fields.

        Args:
            slide_data: Slide data to validate

        Returns:
            True if valid, False otherwise
        """
        required_fields = ["title", "points"]
        return all(field in slide_data for field in required_fields)

    def get_slide_title(self, slide_data: Dict[str, Any]) -> str:
        """Extract and clean slide title from slide data."""
        title = slide_data.get("title", "Untitled Slide")
        return self.clean_text(title)

    def get_slide_points(self, slide_data: Dict[str, Any]) -> List[str]:
        """Extract and clean slide points from slide data."""
        points = slide_data.get("points", [])
        return [self.clean_text(point) for point in points if point.strip()]

    def clean_text(self, text: str) -> str:
        """Clean and format text content."""
        if not text:
            return ""

        # Remove extra whitespace and clean formatting
        text = text.strip()
        text = " ".join(text.split())  # Normalize whitespace

        # Remove any markdown-style formatting
        text = text.replace("**", "").replace("*", "")
        text = text.replace("__", "").replace("_", "")

        return text

    def format_bullet_points(self, points: List[str]) -> str:
        """Format points as bullet list."""
        if not points:
            return ""

        formatted_points = []
        for point in points:
            clean_point = self.clean_text(point)
            if clean_point:
                # Ensure point doesn't already start with bullet
                if not clean_point.startswith("•") and not clean_point.startswith("-"):
                    clean_point = f"• {clean_point}"
                formatted_points.append(clean_point)

        return "\n".join(formatted_points)

    def get_font_settings(self, text_type: str = "body") -> Dict[str, Any]:
        """
        Get font settings for different text types.

        Args:
            text_type: Type of text ("title", "subtitle", "body", "caption")

        Returns:
            Dictionary with font settings
        """
        base_settings = {"font_name": "Segoe UI", "color": self.palette.text_primary}

        if text_type == "title":
            base_settings.update(
                {"size": 32, "bold": True, "color": self.palette.primary}
            )
        elif text_type == "subtitle":
            base_settings.update(
                {"size": 24, "bold": False, "color": self.palette.text_secondary}
            )
        elif text_type == "body":
            base_settings.update({"size": 18, "bold": False})
        elif text_type == "caption":
            base_settings.update(
                {"size": 14, "bold": False, "color": self.palette.text_secondary}
            )

        return base_settings

    def handle_builder_error(self, error: Exception, context: str) -> None:
        """
        Handle and wrap builder errors with context.

        Args:
            error: Original exception
            context: Context description

        Raises:
            SlideBuilderError: Wrapped error with context
        """
        raise SlideBuilderError(
            f"Failed to {context}: {str(error)}",
            slide_type=self.__class__.__name__,
            context={"original_error": str(error)},
        ) from error

    def get_slides_created_count(self) -> int:
        """Get the number of slides created by this builder."""
        return self.slides_created

    def reset_counter(self) -> None:
        """Reset the slides created counter."""
        self.slides_created = 0

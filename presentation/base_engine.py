"""
Base presentation engine for the AI PowerPoint Framework.

This module defines the abstract interface that all presentation engines must implement,
providing a consistent API for different PowerPoint generation backends.
"""

from abc import ABC, abstractmethod
from typing import List, Any, Optional
from pathlib import Path

from design.themes import DesignTheme
from core.exceptions import PresentationGenerationError as PresentationError


class SlideData:
    """Data structure for slide information."""

    def __init__(
        self,
        title: str,
        points: List[str],
        theme: DesignTheme = DesignTheme.CORPORATE_MODERN,
        slide_type: str = "content_slide",
        background_color: Optional[str] = None,
        title_color: Optional[str] = None,
        text_color: Optional[str] = None,
        primary_color: Optional[str] = None,
        accent_colors: Optional[List[str]] = None,
        background_image: Optional[str] = None,
        diagram_image: Optional[str] = None,
        feature_icons: Optional[List[str]] = None,
        custom_visuals: Optional[dict] = None,
    ):
        self.title = title
        self.points = points
        self.theme = theme
        self.slide_type = slide_type
        self.background_color = background_color
        self.title_color = title_color
        self.text_color = text_color
        self.primary_color = primary_color
        self.accent_colors = accent_colors or []
        self.background_image = background_image
        self.diagram_image = diagram_image
        self.feature_icons = feature_icons or []
        self.custom_visuals = custom_visuals or {}


class BasePresentationEngine(ABC):
    """
    Abstract base class for PowerPoint presentation engines.

    This class defines the interface that all presentation engines must implement,
    ensuring consistent behavior across different backends (COM, python-pptx, etc.).
    """

    def __init__(self, config: Optional[Any] = None):
        """
        Initialize the presentation engine.

        Args:
            config: Configuration object for the engine
        """
        self.config = config
        self.presentation = None
        self.slides_created = 0

    @abstractmethod
    def create_presentation(self, title: str = "AI Generated Presentation") -> None:
        """
        Create a new PowerPoint presentation.

        Args:
            title: Title for the presentation

        Raises:
            PresentationError: If presentation creation fails
        """
        pass

    @abstractmethod
    def add_slide(self, slide_data: SlideData) -> None:
        """
        Add a slide to the presentation.

        Args:
            slide_data: Slide data object containing title, points, and styling

        Raises:
            PresentationError: If slide creation fails
        """
        pass

    @abstractmethod
    def add_title_slide(
        self,
        title: str,
        subtitle: str = "",
        theme: DesignTheme = DesignTheme.CORPORATE_MODERN,
    ) -> None:
        """
        Add a title slide to the presentation.

        Args:
            title: Main title text
            subtitle: Subtitle text
            theme: Design theme to apply

        Raises:
            PresentationError: If title slide creation fails
        """
        pass

    @abstractmethod
    def save_presentation(self, filepath: Path) -> bool:
        """
        Save the presentation to a file.

        Args:
            filepath: Path where to save the presentation

        Returns:
            True if save was successful, False otherwise

        Raises:
            PresentationError: If save operation fails
        """
        pass

    @abstractmethod
    def close_presentation(self) -> None:
        """
        Close the presentation and clean up resources.

        Raises:
            PresentationError: If cleanup fails
        """
        pass

    def create_full_presentation(
        self,
        slides_data: List[SlideData],
        output_path: Path,
        presentation_title: str = "AI Generated Presentation",
    ) -> bool:
        """
        Create a complete presentation with multiple slides.

        Args:
            slides_data: List of slide data objects
            output_path: Path where to save the presentation
            presentation_title: Title for the presentation

        Returns:
            True if successful, False otherwise

        Raises:
            PresentationError: If presentation creation fails
        """
        try:
            self.create_presentation(presentation_title)

            for slide_data in slides_data:
                if slide_data.slide_type == "title_slide":
                    subtitle = slide_data.points[0] if slide_data.points else ""
                    self.add_title_slide(slide_data.title, subtitle, slide_data.theme)
                else:
                    self.add_slide(slide_data)

            success = self.save_presentation(output_path)
            self.close_presentation()

            return success

        except Exception as e:
            self.close_presentation()
            raise PresentationError(f"Failed to create presentation: {str(e)}") from e

    def get_slides_count(self) -> int:
        """Get the number of slides created."""
        return self.slides_created

    def is_available(self) -> bool:
        """
        Check if this engine is available on the current system.

        Returns:
            True if engine can be used, False otherwise
        """
        return True  # Override in subclasses for specific checks

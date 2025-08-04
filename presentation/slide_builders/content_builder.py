"""
Content slide builder for the AI PowerPoint Framework.

Specialized builder for general content slides with bullet points and formatted text.
"""

from typing import Dict, Any

from .base_builder import BaseSlideBuilder
from core.exceptions import SlideBuilderError


class ContentSlideBuilder(BaseSlideBuilder):
    """
    Builder for general content slides with bullet points.

    Features:
    - Professional bullet point formatting
    - Theme-based styling
    - Adaptive text sizing
    - Multi-engine support (COM/python-pptx)
    """

    def build_slide(self, slide_data: Dict[str, Any], presentation_engine: Any) -> bool:
        """Build a content slide with title and bullet points."""
        try:
            if not self.validate_slide_data(slide_data):
                raise SlideBuilderError("Invalid slide data for content slide")

            title = self.get_slide_title(slide_data)
            points = self.get_slide_points(slide_data)

            # Create slide data object for engine
            from base_engine import SlideData

            engine_slide_data = SlideData(
                title=title, points=points, theme=self.theme, slide_type="content_slide"
            )

            # Use the presentation engine to add the slide
            presentation_engine.add_slide(engine_slide_data)

            self.slides_created += 1
            return True

        except Exception as e:
            self.handle_builder_error(e, "build content slide")
            return False

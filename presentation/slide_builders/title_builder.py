"""
Title slide builder for creating impactful presentation opening slides.

This module provides specialized functionality for creating title slides
with professional layouts, typography, and visual elements.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from .base_builder import BaseSlideBuilder
from ...core.exceptions import SlideBuilderError
from ...design.color_system import ColorPalette
from ...design.themes import DesignTheme


@dataclass
class TitleSlideData:
    """Data structure for title slide content."""
    
    title: str
    subtitle: Optional[str] = None
    author: Optional[str] = None
    date: Optional[str] = None
    company: Optional[str] = None
    logo_path: Optional[str] = None
    additional_info: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.additional_info is None:
            self.additional_info = []


class TitleSlideBuilder(BaseSlideBuilder):
    """
    Builder for creating professional title slides.
    
    This builder creates impactful opening slides with proper typography,
    visual hierarchy, and branding elements.
    """
    
    def supports_slide_type(self, slide_type: str) -> bool:
        """Check if this builder supports the given slide type."""
        return slide_type.lower() in ['title', 'cover', 'intro', 'section']
    
    def build_slide(self, slide_data: Dict[str, Any], presentation_engine: Any) -> bool:
        """
        Build a title slide.
        
        Args:
            slide_data: Dictionary containing slide information
            presentation_engine: Engine instance (COM or python-pptx)
            
        Returns:
            bool: True if slide was created successfully
        """
        try:
            # Convert dict to TitleSlideData
            title_data = TitleSlideData(
                title=slide_data.get('title', 'Untitled'),
                subtitle=slide_data.get('subtitle'),
                author=slide_data.get('author'),
                date=slide_data.get('date'),
                company=slide_data.get('company'),
                logo_path=slide_data.get('logo_path'),
                additional_info=slide_data.get('additional_info', [])
            )
            
            # Use the presentation engine to create the slide
            slide = presentation_engine.add_slide(layout_name="title")
            
            # Add title
            title_shape = slide.shapes.title
            title_shape.text = title_data.title
            
            # Add subtitle if present
            if hasattr(slide, 'placeholders') and title_data.subtitle:
                try:
                    subtitle_shape = slide.placeholders[1]
                    subtitle_shape.text = title_data.subtitle
                except (IndexError, AttributeError):
                    # Fallback - add subtitle as text box
                    pass
            
            # Add author info if present
            if title_data.author:
                author_text = title_data.author
                if title_data.company:
                    author_text += f" | {title_data.company}"
                if title_data.date:
                    author_text += f" | {title_data.date}"
                
                # Try to add to footer or as text box
                try:
                    if hasattr(slide, 'placeholders') and len(slide.placeholders) > 2:
                        footer_shape = slide.placeholders[2]
                        footer_shape.text = author_text
                except (IndexError, AttributeError):
                    # Fallback - could add as text box
                    pass
            
            self.slides_created += 1
            return True
            
        except Exception as e:
            self.handle_builder_error(e, "create title slide")
            return False
    
    def build(self, slide_data: Dict[str, Any]) -> object:
        """
        Build a title slide (legacy interface).
        
        Args:
            slide_data: Dictionary containing slide information
            
        Returns:
            object: The slide data structure
        """
        return {
            'type': 'title',
            'content': slide_data,
            'title': slide_data.get('title', 'Untitled'),
            'subtitle': slide_data.get('subtitle'),
            'author': slide_data.get('author'),
            'date': slide_data.get('date'),
            'company': slide_data.get('company')
        }
    
    def create_cover_slide(
        self,
        title: str,
        subtitle: str,
        author: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a simple cover slide.
        
        Args:
            title: Main title
            subtitle: Subtitle text
            author: Author name
            **kwargs: Additional options
            
        Returns:
            dict: Slide data
        """
        return {
            'type': 'title',
            'title': title,
            'subtitle': subtitle,
            'author': author,
            **kwargs
        }
    
    def create_section_title(
        self,
        section_title: str,
        section_description: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a section title slide.
        
        Args:
            section_title: Section title
            section_description: Optional description
            **kwargs: Additional options
            
        Returns:
            dict: Slide data
        """
        return {
            'type': 'section',
            'title': section_title,
            'subtitle': section_description,
            **kwargs
        }
    
    def create_presentation_title(
        self,
        presentation_title: str,
        company_name: str,
        presenter_name: str,
        date: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a full presentation title slide.
        
        Args:
            presentation_title: Main presentation title
            company_name: Company or organization name
            presenter_name: Presenter's name
            date: Presentation date
            **kwargs: Additional options
            
        Returns:
            dict: Slide data
        """
        return {
            'type': 'presentation_title',
            'title': presentation_title,
            'company': company_name,
            'author': presenter_name,
            'date': date,
            **kwargs
        }
    
    def get_layout_suggestions(self, content_length: int) -> List[Dict[str, Any]]:
        """
        Get layout suggestions for title slides.
        
        Args:
            content_length: Length of content to display
            
        Returns:
            List of layout suggestions
        """
        suggestions = [
            {
                "name": "Classic Center",
                "description": "Traditional centered layout",
                "suitable_for": "Most presentations",
                "title_position": "center",
                "subtitle_position": "center_below",
                "author_position": "bottom_center",
            },
            {
                "name": "Modern Left",
                "description": "Contemporary left-aligned layout",
                "suitable_for": "Creative presentations",
                "title_position": "left_center",
                "subtitle_position": "left_below",
                "author_position": "bottom_left",
            },
            {
                "name": "Corporate Right",
                "description": "Professional right-aligned layout",
                "suitable_for": "Business presentations",
                "title_position": "right_center",
                "subtitle_position": "right_below",
                "author_position": "bottom_right",
            },
        ]
        
        return suggestions

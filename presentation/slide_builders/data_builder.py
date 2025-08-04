"""
Data visualization slide builder for creating charts and data-driven slides.

This module creates slides specifically for data visualizations,
integrating with the data analysis and chart generation components.
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

from presentation.slide_builders.base_builder import BaseSlideBuilder
from visual.layout_system import LayoutType, AlignmentType
from core.exceptions import SlideBuilderError


class DataSlideBuilder(BaseSlideBuilder):
    """
    Slide builder specialized for data visualization slides.
    
    Creates slides with charts, graphs, and data-driven content
    based on analysis results from the DataVisualizationAgent.
    """
    
    def __init__(self):
        """Initialize the data slide builder"""
        super().__init__()
        self.logger = logging.getLogger(__name__)
    
    def build_slide(self, slide_data: Dict[str, Any], presentation_engine: Any) -> bool:
        """
        Build a data slide using the specified presentation engine.
        
        Args:
            slide_data: Dictionary containing slide content and metadata
            presentation_engine: Engine instance (COM or python-pptx)
            
        Returns:
            True if slide was created successfully
        """
        try:
            slide_type = slide_data.get('slide_type', 'content')
            
            if slide_type == 'data_overview':
                return self._create_data_overview_slide(slide_data, presentation_engine)
            elif slide_type == 'chart':
                return self._create_chart_slide(slide_data, presentation_engine)
            elif slide_type == 'dashboard':
                return self._create_dashboard_slide(slide_data, presentation_engine)
            else:
                # Default content slide
                return self._create_content_slide(slide_data, presentation_engine)
                
        except Exception as e:
            self.logger.error(f"Failed to build data slide: {e}")
            raise SlideBuilderError(f"Data slide creation failed: {e}")
    
    def _create_data_overview_slide(self, slide_data: Dict[str, Any], 
                                   presentation_engine: Any) -> bool:
        """Create a data overview slide with dataset information"""
        try:
            # Use standard content layout
            layout_type = LayoutType.TITLE_CONTENT
            
            title = slide_data.get('title', 'Data Overview')
            
            # Build overview content
            overview = slide_data.get('data_overview', {})
            content_lines = [
                f"Dataset: {overview.get('name', 'Dataset')}",
                f"Records: {overview.get('rows', 0):,}",
                f"Columns: {overview.get('columns', 0)}",
                f"Numeric Columns: {overview.get('numeric_columns', 0)}",
                f"Categorical Columns: {overview.get('categorical_columns', 0)}"
            ]
            
            # Add key findings if available
            key_findings = slide_data.get('key_findings', [])
            if key_findings:
                content_lines.append("")
                content_lines.append("Key Findings:")
                for finding in key_findings[:3]:  # Top 3 findings
                    content_lines.append(f"• {finding}")
            
            # Create slide using engine
            slide_info = {
                'title': title,
                'points': content_lines,
                'layout_type': layout_type.value
            }
            
            return presentation_engine.create_content_slide(slide_info)
            
        except Exception as e:
            self.logger.error(f"Failed to create data overview slide: {e}")
            return False
    
    def _create_chart_slide(self, slide_data: Dict[str, Any], 
                           presentation_engine: Any) -> bool:
        """Create a slide with a data chart"""
        try:
            title = slide_data.get('title', 'Data Visualization')
            chart_config = slide_data.get('chart_data', {})
            
            # Create slide with chart placeholder for now
            # Full chart implementation would depend on the engine type
            slide_info = {
                'title': title,
                'points': [f"[Chart: {chart_config.get('type', 'Data Chart')}]"],
                'layout_type': LayoutType.TITLE_CONTENT.value
            }
            
            return presentation_engine.create_content_slide(slide_info)
            
        except Exception as e:
            self.logger.error(f"Failed to create chart slide: {e}")
            return False
    
    def _create_dashboard_slide(self, slide_data: Dict[str, Any], 
                               presentation_engine: Any) -> bool:
        """Create a dashboard slide with multiple charts"""
        try:
            title = slide_data.get('title', 'Data Dashboard')
            charts = slide_data.get('charts', [])
            
            # Create slide with dashboard placeholder
            chart_summaries = [f"Chart {i+1}: {chart.get('title', 'Chart')}" 
                             for i, chart in enumerate(charts)]
            
            slide_info = {
                'title': title,
                'points': chart_summaries,
                'layout_type': LayoutType.TITLE_CONTENT.value
            }
            
            return presentation_engine.create_content_slide(slide_info)
            
        except Exception as e:
            self.logger.error(f"Failed to create dashboard slide: {e}")
            return False
    
    def _create_content_slide(self, slide_data: Dict[str, Any], 
                             presentation_engine: Any) -> bool:
        """Create a standard content slide"""
        try:
            if not self.validate_slide_data(slide_data):
                return False
            
            title = self.get_slide_title(slide_data)
            points = self.get_slide_points(slide_data)
            
            slide_info = {
                'title': title,
                'points': points,
                'layout_type': LayoutType.TITLE_CONTENT.value
            }
            
            return presentation_engine.create_content_slide(slide_info)
            
        except Exception as e:
            self.logger.error(f"Failed to create content slide: {e}")
            return False

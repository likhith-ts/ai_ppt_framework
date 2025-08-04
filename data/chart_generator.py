"""
Chart generation module for creating professional data visualizations in PowerPoint.

This module creates native PowerPoint charts from data analysis results,
supporting various chart types and professional styling.
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import json

from data.data_analyzer import DataInsight, ChartType
from core.exceptions import FrameworkError


class ChartStyle(Enum):
    """Chart styling options"""
    PROFESSIONAL = "professional"
    MODERN = "modern"
    MINIMAL = "minimal"
    COLORFUL = "colorful"


class ChartGenerator:
    """
    Generates PowerPoint chart objects from data analysis results.
    """
    
    def __init__(self, style: ChartStyle = ChartStyle.PROFESSIONAL):
        """
        Initialize chart generator.
        
        Args:
            style: Default chart styling
        """
        self.style = style
        self.logger = logging.getLogger(__name__)
    
    def create_chart_from_insight(self, insight: DataInsight, 
                                 slide_width: float = 10, 
                                 slide_height: float = 7.5) -> Dict[str, Any]:
        """
        Create a chart configuration from a data insight.
        
        Args:
            insight: Data insight containing chart data and type
            slide_width: Slide width in inches
            slide_height: Slide height in inches
            
        Returns:
            Chart configuration dictionary
        """
        try:
            chart_config = {
                'type': insight.chart_type.value,
                'title': insight.title,
                'data': insight.data,
                'style': self.style.value,
                'position': self._calculate_chart_position(slide_width, slide_height),
                'size': self._calculate_chart_size(slide_width, slide_height),
                'formatting': self._get_chart_formatting(insight.chart_type)
            }
            
            # Add specific configurations based on chart type
            if insight.chart_type == ChartType.BAR_CHART:
                chart_config.update(self._configure_bar_chart(insight))
            elif insight.chart_type == ChartType.LINE_CHART:
                chart_config.update(self._configure_line_chart(insight))
            elif insight.chart_type == ChartType.PIE_CHART:
                chart_config.update(self._configure_pie_chart(insight))
            elif insight.chart_type == ChartType.SCATTER_PLOT:
                chart_config.update(self._configure_scatter_plot(insight))
            elif insight.chart_type == ChartType.HISTOGRAM:
                chart_config.update(self._configure_histogram(insight))
            elif insight.chart_type == ChartType.AREA_CHART:
                chart_config.update(self._configure_area_chart(insight))
            
            return chart_config
            
        except Exception as e:
            self.logger.error(f"Failed to create chart configuration: {e}")
            raise FrameworkError(f"Chart generation failed: {e}")
    
    def _calculate_chart_position(self, slide_width: float, 
                                 slide_height: float) -> Dict[str, float]:
        """Calculate optimal chart position on slide"""
        # Center the chart with some margin
        margin = 0.5
        chart_width = slide_width - (2 * margin)
        chart_height = slide_height * 0.6  # 60% of slide height
        
        return {
            'left': margin,
            'top': slide_height * 0.2,  # Start 20% down the slide
            'width': chart_width,
            'height': chart_height
        }
    
    def _calculate_chart_size(self, slide_width: float, 
                             slide_height: float) -> Dict[str, float]:
        """Calculate chart dimensions"""
        return {
            'width': slide_width * 0.8,
            'height': slide_height * 0.6
        }
    
    def _get_chart_formatting(self, chart_type: ChartType) -> Dict[str, Any]:
        """Get formatting configuration for chart type"""
        base_formatting = {
            'font_size': 12,
            'font_family': 'Calibri',
            'title_font_size': 16,
            'legend_position': 'bottom',
            'grid_lines': True,
            'data_labels': False
        }
        
        # Customize based on chart type
        if chart_type in [ChartType.PIE_CHART, ChartType.DONUT_CHART]:
            base_formatting.update({
                'data_labels': True,
                'legend_position': 'right',
                'grid_lines': False
            })
        elif chart_type == ChartType.SCATTER_PLOT:
            base_formatting.update({
                'trend_line': True,
                'data_labels': False
            })
        
        return base_formatting
    
    def _configure_bar_chart(self, insight: DataInsight) -> Dict[str, Any]:
        """Configure bar chart specific settings"""
        return {
            'chart_subtype': 'clustered',
            'categories': insight.data.get('labels', []),
            'series': [{
                'name': insight.title,
                'values': insight.data.get('values', [])
            }],
            'axis_labels': {
                'x_axis': 'Categories',
                'y_axis': 'Values'
            }
        }
    
    def _configure_line_chart(self, insight: DataInsight) -> Dict[str, Any]:
        """Configure line chart specific settings"""
        return {
            'chart_subtype': 'line_with_markers',
            'categories': insight.data.get('dates', insight.data.get('labels', [])),
            'series': [{
                'name': insight.title,
                'values': insight.data.get('values', [])
            }],
            'axis_labels': {
                'x_axis': 'Time' if 'dates' in insight.data else 'Categories',
                'y_axis': 'Values'
            },
            'smooth_lines': True
        }
    
    def _configure_pie_chart(self, insight: DataInsight) -> Dict[str, Any]:
        """Configure pie chart specific settings"""
        return {
            'chart_subtype': 'pie',
            'categories': insight.data.get('labels', []),
            'series': [{
                'name': insight.title,
                'values': insight.data.get('values', [])
            }],
            'explosion': 0.1,  # Slight separation of slices
            'show_percentages': True
        }
    
    def _configure_scatter_plot(self, insight: DataInsight) -> Dict[str, Any]:
        """Configure scatter plot specific settings"""
        return {
            'chart_subtype': 'scatter_with_markers',
            'x_values': insight.data.get('x_values', []),
            'y_values': insight.data.get('y_values', []),
            'series': [{
                'name': insight.title,
                'x_values': insight.data.get('x_values', []),
                'y_values': insight.data.get('y_values', [])
            }],
            'axis_labels': {
                'x_axis': 'X Values',
                'y_axis': 'Y Values'
            },
            'trend_line': insight.data.get('correlation', 0) != 0
        }
    
    def _configure_histogram(self, insight: DataInsight) -> Dict[str, Any]:
        """Configure histogram specific settings"""
        values = insight.data.get('values', [])
        
        # Create bins for histogram
        if values:
            min_val = min(values)
            max_val = max(values)
            num_bins = min(10, len(set(values)))  # Max 10 bins
            bin_width = (max_val - min_val) / num_bins
            
            bins = []
            bin_counts = []
            for i in range(num_bins):
                bin_start = min_val + (i * bin_width)
                bin_end = min_val + ((i + 1) * bin_width)
                count = sum(1 for v in values if bin_start <= v < bin_end)
                bins.append(f"{bin_start:.1f}-{bin_end:.1f}")
                bin_counts.append(count)
        else:
            bins = []
            bin_counts = []
        
        return {
            'chart_subtype': 'column',
            'categories': bins,
            'series': [{
                'name': 'Frequency',
                'values': bin_counts
            }],
            'axis_labels': {
                'x_axis': 'Value Ranges',
                'y_axis': 'Frequency'
            }
        }
    
    def _configure_area_chart(self, insight: DataInsight) -> Dict[str, Any]:
        """Configure area chart specific settings"""
        return {
            'chart_subtype': 'area',
            'categories': insight.data.get('dates', insight.data.get('labels', [])),
            'series': [{
                'name': insight.title,
                'values': insight.data.get('values', [])
            }],
            'axis_labels': {
                'x_axis': 'Time' if 'dates' in insight.data else 'Categories',
                'y_axis': 'Values'
            },
            'transparency': 0.3
        }
    
    def create_dashboard_layout(self, insights: List[DataInsight], 
                               slide_width: float = 10, 
                               slide_height: float = 7.5) -> List[Dict[str, Any]]:
        """
        Create a dashboard layout with multiple charts.
        
        Args:
            insights: List of data insights
            slide_width: Slide width in inches
            slide_height: Slide height in inches
            
        Returns:
            List of chart configurations for dashboard
        """
        dashboard_charts = []
        
        # Determine layout based on number of charts
        num_charts = len(insights)
        if num_charts <= 2:
            # Side by side
            chart_width = (slide_width - 1.5) / 2
            chart_height = slide_height * 0.6
            
            for i, insight in enumerate(insights):
                chart_config = self.create_chart_from_insight(insight, slide_width, slide_height)
                chart_config['position'] = {
                    'left': 0.5 + (i * (chart_width + 0.5)),
                    'top': slide_height * 0.2,
                    'width': chart_width,
                    'height': chart_height
                }
                dashboard_charts.append(chart_config)
        
        elif num_charts <= 4:
            # 2x2 grid
            chart_width = (slide_width - 1.5) / 2
            chart_height = (slide_height * 0.8) / 2
            
            for i, insight in enumerate(insights):
                row = i // 2
                col = i % 2
                
                chart_config = self.create_chart_from_insight(insight, slide_width, slide_height)
                chart_config['position'] = {
                    'left': 0.5 + (col * (chart_width + 0.5)),
                    'top': 0.5 + (row * (chart_height + 0.5)),
                    'width': chart_width,
                    'height': chart_height
                }
                dashboard_charts.append(chart_config)
        
        else:
            # More than 4 charts - create multiple slides
            # For now, just take the top 4 most significant
            sorted_insights = sorted(insights, key=lambda x: x.significance, reverse=True)[:4]
            return self.create_dashboard_layout(sorted_insights, slide_width, slide_height)
        
        return dashboard_charts
    
    def get_color_scheme(self, theme: str = "professional") -> List[str]:
        """
        Get color scheme for charts based on theme.
        
        Args:
            theme: Color theme name
            
        Returns:
            List of hex color codes
        """
        color_schemes = {
            "professional": [
                "#1f4e79", "#2e75b6", "#70ad47", "#ffc000", 
                "#c55a11", "#7030a0", "#44546a", "#264478"
            ],
            "modern": [
                "#0078d4", "#00bcf2", "#40e0d0", "#90ee90",
                "#ffb347", "#ffa07a", "#dda0dd", "#b0c4de"
            ],
            "minimal": [
                "#2d3748", "#4a5568", "#718096", "#a0aec0",
                "#cbd5e0", "#e2e8f0", "#edf2f7", "#f7fafc"
            ],
            "colorful": [
                "#e53e3e", "#dd6b20", "#d69e2e", "#38a169",
                "#3182ce", "#553c9a", "#805ad5", "#d53f8c"
            ]
        }
        
        return color_schemes.get(theme, color_schemes["professional"])

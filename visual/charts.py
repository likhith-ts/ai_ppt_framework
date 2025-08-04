"""
Chart and graph generation for presentations.

This module provides intelligent chart generation capabilities,
creating appropriate visualizations based on data structure and content.
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass
import json

from core.exceptions import FrameworkError
from design.color_system import ColorPalette


class ChartType(Enum):
    """Chart types supported by the framework."""
    
    BAR = "bar"
    COLUMN = "column"
    LINE = "line"
    PIE = "pie"
    DOUGHNUT = "doughnut"
    SCATTER = "scatter"
    AREA = "area"
    RADAR = "radar"
    BUBBLE = "bubble"
    COMBO = "combo"
    HISTOGRAM = "histogram"
    WATERFALL = "waterfall"
    GANTT = "gantt"
    TREEMAP = "treemap"
    HEATMAP = "heatmap"


class ChartStyle(Enum):
    """Chart styling options."""
    
    MINIMAL = "minimal"
    CORPORATE = "corporate"
    MODERN = "modern"
    COLORFUL = "colorful"
    MONOCHROME = "monochrome"
    GRADIENT = "gradient"


@dataclass
class ChartData:
    """Represents chart data structure."""
    
    labels: List[str]
    datasets: List[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class ChartConfig:
    """Configuration for chart generation."""
    
    chart_type: ChartType
    title: str
    style: ChartStyle = ChartStyle.MODERN
    color_palette: Optional[ColorPalette] = None
    show_legend: bool = True
    show_grid: bool = True
    show_labels: bool = True
    animate: bool = True
    responsive: bool = True
    custom_options: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.custom_options is None:
            self.custom_options = {}


@dataclass
class GeneratedChart:
    """Represents a generated chart."""
    
    config: ChartConfig
    data: ChartData
    chart_definition: Dict[str, Any]
    powerpoint_data: Dict[str, Any]
    description: str
    preview_html: Optional[str] = None


class ChartGenerator:
    """
    Generator for creating presentation charts and graphs.
    
    This class provides intelligent chart generation based on
    data structure, content type, and visual requirements.
    """
    
    def __init__(self, default_style: ChartStyle = ChartStyle.MODERN):
        """
        Initialize the chart generator.
        
        Args:
            default_style: Default chart style to use
        """
        self.default_style = default_style
        self._chart_templates = self._init_chart_templates()
        self._color_schemes = self._init_color_schemes()
    
    def analyze_data_structure(self, data: Union[Dict, List, str]) -> ChartType:
        """
        Analyze data structure and recommend appropriate chart type.
        
        Args:
            data: Data to analyze
            
        Returns:
            ChartType: Recommended chart type
        """
        if isinstance(data, dict):
            return self._analyze_dict_data(data)
        elif isinstance(data, list):
            return self._analyze_list_data(data)
        elif isinstance(data, str):
            return self._analyze_text_data(data)
        else:
            return ChartType.BAR  # Default fallback
    
    def create_chart(
        self,
        data: Union[Dict, List, str],
        title: str,
        chart_type: Optional[ChartType] = None,
        style: Optional[ChartStyle] = None,
        color_palette: Optional[ColorPalette] = None,
        **kwargs
    ) -> GeneratedChart:
        """
        Create a chart from data.
        
        Args:
            data: Data to visualize
            title: Chart title
            chart_type: Override automatic type detection
            style: Chart styling
            color_palette: Color palette for the chart
            **kwargs: Additional chart options
            
        Returns:
            GeneratedChart: Generated chart
        """
        if chart_type is None:
            chart_type = self.analyze_data_structure(data)
        
        config = ChartConfig(
            chart_type=chart_type,
            title=title,
            style=style or self.default_style,
            color_palette=color_palette,
            **kwargs
        )
        
        chart_data = self._prepare_chart_data(data, chart_type)
        chart_definition = self._create_chart_definition(config, chart_data)
        powerpoint_data = self._create_powerpoint_data(config, chart_data)
        
        return GeneratedChart(
            config=config,
            data=chart_data,
            chart_definition=chart_definition,
            powerpoint_data=powerpoint_data,
            description=f"{chart_type.value.title()} chart showing {title}",
            preview_html=self._generate_preview_html(config, chart_data),
        )
    
    def create_comparison_chart(
        self,
        categories: List[str],
        values: List[Union[int, float]],
        title: str,
        chart_type: ChartType = ChartType.COLUMN,
        **kwargs
    ) -> GeneratedChart:
        """
        Create a comparison chart.
        
        Args:
            categories: Category labels
            values: Values for each category
            title: Chart title
            chart_type: Type of chart to create
            **kwargs: Additional options
            
        Returns:
            GeneratedChart: Generated chart
        """
        data = {
            "labels": categories,
            "datasets": [{"label": "Values", "data": values}]
        }
        
        return self.create_chart(data, title, chart_type, **kwargs)
    
    def create_trend_chart(
        self,
        time_labels: List[str],
        values: List[Union[int, float]],
        title: str,
        chart_type: ChartType = ChartType.LINE,
        **kwargs
    ) -> GeneratedChart:
        """
        Create a trend chart.
        
        Args:
            time_labels: Time period labels
            values: Values for each time period
            title: Chart title
            chart_type: Type of chart to create
            **kwargs: Additional options
            
        Returns:
            GeneratedChart: Generated chart
        """
        data = {
            "labels": time_labels,
            "datasets": [{"label": "Trend", "data": values}]
        }
        
        return self.create_chart(data, title, chart_type, **kwargs)
    
    def create_distribution_chart(
        self,
        labels: List[str],
        values: List[Union[int, float]],
        title: str,
        chart_type: ChartType = ChartType.PIE,
        **kwargs
    ) -> GeneratedChart:
        """
        Create a distribution chart.
        
        Args:
            labels: Distribution labels
            values: Values for each segment
            title: Chart title
            chart_type: Type of chart to create
            **kwargs: Additional options
            
        Returns:
            GeneratedChart: Generated chart
        """
        data = {
            "labels": labels,
            "datasets": [{"label": "Distribution", "data": values}]
        }
        
        return self.create_chart(data, title, chart_type, **kwargs)
    
    def create_multi_series_chart(
        self,
        categories: List[str],
        series_data: Dict[str, List[Union[int, float]]],
        title: str,
        chart_type: ChartType = ChartType.COLUMN,
        **kwargs
    ) -> GeneratedChart:
        """
        Create a multi-series chart.
        
        Args:
            categories: Category labels
            series_data: Dictionary of series name to values
            title: Chart title
            chart_type: Type of chart to create
            **kwargs: Additional options
            
        Returns:
            GeneratedChart: Generated chart
        """
        datasets = []
        for series_name, values in series_data.items():
            datasets.append({
                "label": series_name,
                "data": values
            })
        
        data = {
            "labels": categories,
            "datasets": datasets
        }
        
        return self.create_chart(data, title, chart_type, **kwargs)
    
    def _analyze_dict_data(self, data: Dict) -> ChartType:
        """Analyze dictionary data structure."""
        if "labels" in data and "datasets" in data:
            # Already structured chart data
            return ChartType.COLUMN
        
        # Simple key-value pairs
        if all(isinstance(v, (int, float)) for v in data.values()):
            if len(data) <= 10:
                return ChartType.PIE
            else:
                return ChartType.COLUMN
        
        # Multi-level data
        if any(isinstance(v, (list, dict)) for v in data.values()):
            return ChartType.COLUMN
        
        return ChartType.BAR
    
    def _analyze_list_data(self, data: List) -> ChartType:
        """Analyze list data structure."""
        if not data:
            return ChartType.BAR
        
        # List of numbers
        if all(isinstance(item, (int, float)) for item in data):
            return ChartType.LINE
        
        # List of dictionaries
        if all(isinstance(item, dict) for item in data):
            return ChartType.COLUMN
        
        # Mixed data
        return ChartType.BAR
    
    def _analyze_text_data(self, data: str) -> ChartType:
        """Analyze text data for chart recommendations."""
        data_lower = data.lower()
        
        # Look for trend keywords
        trend_keywords = ["over time", "trend", "growth", "decline", "change"]
        if any(keyword in data_lower for keyword in trend_keywords):
            return ChartType.LINE
        
        # Look for comparison keywords
        comparison_keywords = ["compare", "versus", "vs", "difference"]
        if any(keyword in data_lower for keyword in comparison_keywords):
            return ChartType.COLUMN
        
        # Look for distribution keywords
        distribution_keywords = ["percentage", "share", "portion", "part of"]
        if any(keyword in data_lower for keyword in distribution_keywords):
            return ChartType.PIE
        
        return ChartType.BAR
    
    def _prepare_chart_data(self, data: Union[Dict, List, str], chart_type: ChartType) -> ChartData:
        """Prepare data for chart generation."""
        if isinstance(data, dict):
            if "labels" in data and "datasets" in data:
                # Already structured
                return ChartData(
                    labels=data["labels"],
                    datasets=data["datasets"]
                )
            else:
                # Convert dict to chart data
                return ChartData(
                    labels=list(data.keys()),
                    datasets=[{
                        "label": "Values",
                        "data": list(data.values())
                    }]
                )
        elif isinstance(data, list):
            if all(isinstance(item, (int, float)) for item in data):
                return ChartData(
                    labels=[f"Item {i+1}" for i in range(len(data))],
                    datasets=[{
                        "label": "Values",
                        "data": data
                    }]
                )
            else:
                return ChartData(
                    labels=[str(item) for item in data],
                    datasets=[{
                        "label": "Count",
                        "data": [1] * len(data)
                    }]
                )
        else:
            # String data - create simple chart
            return ChartData(
                labels=["Data"],
                datasets=[{
                    "label": "Value",
                    "data": [1]
                }]
            )
    
    def _create_chart_definition(self, config: ChartConfig, data: ChartData) -> Dict[str, Any]:
        """Create chart definition for web frameworks."""
        chart_def = {
            "type": config.chart_type.value,
            "data": {
                "labels": data.labels,
                "datasets": self._style_datasets(data.datasets, config)
            },
            "options": {
                "responsive": config.responsive,
                "plugins": {
                    "title": {
                        "display": bool(config.title),
                        "text": config.title
                    },
                    "legend": {
                        "display": config.show_legend
                    }
                },
                "scales": self._get_scale_options(config),
                "animation": {
                    "duration": 1000 if config.animate else 0
                }
            }
        }
        
        # Add custom options
        if config.custom_options:
            chart_def["options"].update(config.custom_options)
        
        return chart_def
    
    def _create_powerpoint_data(self, config: ChartConfig, data: ChartData) -> Dict[str, Any]:
        """Create PowerPoint-compatible chart data."""
        return {
            "chart_type": config.chart_type.value,
            "title": config.title,
            "categories": data.labels,
            "series": [
                {
                    "name": dataset.get("label", "Series"),
                    "values": dataset["data"]
                }
                for dataset in data.datasets
            ],
            "style": config.style.value,
            "show_legend": config.show_legend,
            "show_grid": config.show_grid,
            "colors": self._get_chart_colors(config),
        }
    
    def _style_datasets(self, datasets: List[Dict[str, Any]], config: ChartConfig) -> List[Dict[str, Any]]:
        """Apply styling to chart datasets."""
        styled_datasets = []
        colors = self._get_chart_colors(config)
        
        for i, dataset in enumerate(datasets):
            styled_dataset = dataset.copy()
            
            # Apply colors
            if config.chart_type in [ChartType.PIE, ChartType.DOUGHNUT]:
                styled_dataset["backgroundColor"] = colors
            else:
                color_index = i % len(colors)
                styled_dataset["backgroundColor"] = colors[color_index]
                styled_dataset["borderColor"] = colors[color_index]
            
            # Apply style-specific options
            if config.style == ChartStyle.MINIMAL:
                styled_dataset["borderWidth"] = 1
            elif config.style == ChartStyle.CORPORATE:
                styled_dataset["borderWidth"] = 2
            elif config.style == ChartStyle.MODERN:
                styled_dataset["borderWidth"] = 0
                styled_dataset["borderRadius"] = 4
            
            styled_datasets.append(styled_dataset)
        
        return styled_datasets
    
    def _get_scale_options(self, config: ChartConfig) -> Dict[str, Any]:
        """Get scale options for chart."""
        if config.chart_type in [ChartType.PIE, ChartType.DOUGHNUT]:
            return {}
        
        return {
            "x": {
                "grid": {
                    "display": config.show_grid
                }
            },
            "y": {
                "grid": {
                    "display": config.show_grid
                }
            }
        }
    
    def _get_chart_colors(self, config: ChartConfig) -> List[str]:
        """Get color scheme for chart."""
        if config.color_palette:
            # Convert RGB integers to hex strings
            return [
                f"#{config.color_palette.primary:06x}",
                f"#{config.color_palette.secondary:06x}",
                f"#{config.color_palette.accent:06x}",
                f"#{config.color_palette.text_primary:06x}",
            ]
        
        return self._color_schemes.get(config.style, self._color_schemes[ChartStyle.MODERN])
    
    def _generate_preview_html(self, config: ChartConfig, data: ChartData) -> str:
        """Generate HTML preview of the chart."""
        chart_def = self._create_chart_definition(config, data)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Chart Preview</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <div style="width: 400px; height: 300px;">
                <canvas id="chartPreview"></canvas>
            </div>
            <script>
                const ctx = document.getElementById('chartPreview').getContext('2d');
                const chart = new Chart(ctx, {json.dumps(chart_def)});
            </script>
        </body>
        </html>
        """
        
        return html
    
    def _init_chart_templates(self) -> Dict[ChartType, Dict[str, Any]]:
        """Initialize chart template library."""
        return {
            ChartType.BAR: {
                "default_options": {
                    "indexAxis": "y",
                    "responsive": True,
                }
            },
            ChartType.COLUMN: {
                "default_options": {
                    "responsive": True,
                }
            },
            ChartType.LINE: {
                "default_options": {
                    "responsive": True,
                    "tension": 0.4,
                }
            },
            ChartType.PIE: {
                "default_options": {
                    "responsive": True,
                }
            },
            ChartType.DOUGHNUT: {
                "default_options": {
                    "responsive": True,
                    "cutout": "60%",
                }
            },
        }
    
    def _init_color_schemes(self) -> Dict[ChartStyle, List[str]]:
        """Initialize color scheme library."""
        return {
            ChartStyle.MINIMAL: [
                "#6c757d", "#adb5bd", "#dee2e6", "#f8f9fa"
            ],
            ChartStyle.CORPORATE: [
                "#0d6efd", "#6610f2", "#6f42c1", "#d63384"
            ],
            ChartStyle.MODERN: [
                "#20c997", "#fd7e14", "#dc3545", "#6f42c1"
            ],
            ChartStyle.COLORFUL: [
                "#ff6b6b", "#4ecdc4", "#45b7d1", "#f9ca24",
                "#f0932b", "#eb4d4b", "#6ab04c", "#30336b"
            ],
            ChartStyle.MONOCHROME: [
                "#343a40", "#495057", "#6c757d", "#adb5bd"
            ],
            ChartStyle.GRADIENT: [
                "#667eea", "#764ba2", "#f093fb", "#f5576c"
            ],
        }
    
    def export_chart_config(self, chart: GeneratedChart) -> Dict[str, Any]:
        """
        Export chart configuration for external use.
        
        Args:
            chart: Generated chart to export
            
        Returns:
            dict: Chart configuration data
        """
        return {
            "chart_definition": chart.chart_definition,
            "powerpoint_data": chart.powerpoint_data,
            "config": {
                "chart_type": chart.config.chart_type.value,
                "title": chart.config.title,
                "style": chart.config.style.value,
                "show_legend": chart.config.show_legend,
                "show_grid": chart.config.show_grid,
                "animate": chart.config.animate,
            },
            "data": {
                "labels": chart.data.labels,
                "datasets": chart.data.datasets,
            },
        }

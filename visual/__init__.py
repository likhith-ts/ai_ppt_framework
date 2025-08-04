"""
Visual elements module for the AI PowerPoint Framework.

This module provides visual enhancement capabilities including SmartArt generation,
background styling, and chart creation for presentations.
"""

from .smartart_engine import SmartArtEngine, SmartArtType
from .backgrounds import BackgroundGenerator, BackgroundStyle
from .charts import ChartGenerator, ChartType

__all__ = [
    "SmartArtEngine",
    "SmartArtType", 
    "BackgroundGenerator",
    "BackgroundStyle",
    "ChartGenerator",
    "ChartType",
]

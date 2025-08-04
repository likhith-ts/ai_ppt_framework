"""
Data integration module for the AI PowerPoint Framework.

This module provides data source integrations for creating data-driven presentations.
"""

from .google_sheets import GoogleSheetsClient
from .data_analyzer import DataAnalyzer
from .chart_generator import ChartGenerator

__all__ = [
    'GoogleSheetsClient',
    'DataAnalyzer', 
    'ChartGenerator'
]

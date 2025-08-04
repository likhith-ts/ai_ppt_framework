"""
UI module for the AI PowerPoint Framework.

This module provides the web-based user interface components and the main
Streamlit application for generating presentations.
"""

from .streamlit_app import run_streamlit_app
from .components import (
    UIComponents,
    FormComponents,
    DialogComponents,
    apply_custom_css,
    get_theme_colors
)

__all__ = [
    'run_streamlit_app',
    'UIComponents',
    'FormComponents', 
    'DialogComponents',
    'apply_custom_css',
    'get_theme_colors'
]

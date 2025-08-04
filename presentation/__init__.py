"""
Presentation module initialization for the AI PowerPoint Framework.

This module provides presentation engines, slide builders, and formatting utilities
for generating professional PowerPoint presentations.
"""

from .factory import PresentationFactory
from .base_engine import BasePresentationEngine
from .com_engine import COMPresentationEngine
from .pptx_engine import PPTXPresentationEngine

__all__ = [
    "PresentationFactory",
    "BasePresentationEngine",
    "COMPresentationEngine",
    "PPTXPresentationEngine",
]

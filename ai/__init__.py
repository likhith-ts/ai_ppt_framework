"""
AI integration module initialization for the AI PowerPoint Framework.

This module provides access to AI client, content analyzer, and prompt templates.
"""

from .gemini_client import GeminiClient
from .content_analyzer import ContentAnalyzer
from .prompt_templates import PromptTemplates

__all__ = ["GeminiClient", "ContentAnalyzer", "PromptTemplates"]

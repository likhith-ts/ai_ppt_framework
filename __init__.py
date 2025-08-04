"""
AI PowerPoint Framework - Professional presentation generation with AI.

This framework provides advanced PowerPoint presentation generation capabilities
using AI analysis, professional design systems, and cross-platform compatibility.

Key Features:
- AI-powered content analysis and generation
- Professional design themes and color systems
- Cross-platform presentation engines (COM/python-pptx)
- Modular, extensible architecture
- Comprehensive error handling and logging

Quick Start:
    ```python
    from ai_ppt_framework import AIPresenterFramework

    # Simple usage
    framework = AIPresenterFramework()
    ppt_path = framework.create_from_zip("repository.zip")

    # Advanced usage with custom configuration
    from ai_ppt_framework.core.config import Config
    from ai_ppt_framework.design.themes import DesignTheme

    config = Config(default_theme=DesignTheme.TECH_INNOVATION)
    framework = AIPresenterFramework(config)
    ppt_path = framework.create_from_zip("repo.zip", "analysis.pptx")
    ```

Architecture:
    - core: Configuration, constants, exceptions
    - design: Themes, colors, typography, layouts
    - ai: Gemini client, content analysis, prompt templates
    - presentation: Engines, factories, slide builders
    - visual: SmartArt, backgrounds, charts
    - utils: File handling, parsing, validation
    - ui: Streamlit interface components
"""

from .framework import AIPresenterFramework

__version__ = "1.0.0"
__author__ = "AI PowerPoint Framework Team"

__all__ = ["AIPresenterFramework"]

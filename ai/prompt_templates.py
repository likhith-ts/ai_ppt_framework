"""
Prompt templates for AI content generation.

This module contains sophisticated prompt templates for generating high-quality
presentation content using AI models like Gemini. Templates are designed for
different presentation types and use advanced prompting techniques.
"""

from typing import Dict, List, Optional
from enum import Enum

from design.themes import DesignTheme


class SlideType(Enum):
    """Types of slides for different presentation purposes."""

    TITLE_SLIDE = "title_slide"
    ARCHITECTURE_SLIDE = "architecture_slide"
    FEATURES_SLIDE = "features_slide"
    METRICS_SLIDE = "metrics_slide"
    ROADMAP_SLIDE = "roadmap_slide"
    CONTENT_SLIDE = "content_slide"


class PromptTemplates:
    """
    Advanced prompt templates for AI-powered presentation generation.

    Features:
    - Executive-grade presentation prompts
    - Context-aware content generation
    - Multiple slide type support
    - Technology-specific adaptations
    - Fallback content strategies
    """

    @staticmethod
    def get_repository_analysis_prompt(
        content: str, max_content_length: int = 15000
    ) -> str:
        """
        Generate comprehensive repository analysis prompt for Gemini AI.

        Args:
            content: Repository content to analyze
            max_content_length: Maximum content length to include in prompt

        Returns:
            Detailed analysis prompt for AI generation
        """
        truncated_content = (
            content[:max_content_length]
            if len(content) > max_content_length
            else content
        )

        return f"""
As a world-class presentation designer and software architect from top tech companies (Google, Microsoft, Adobe), analyze this GitHub repository and create an extraordinary multi-slide presentation that would impress executives and technical leaders.

CRITICAL: You MUST provide EXACTLY this format with detailed, specific content for each point. Do not use placeholder text like [Technology stack overview] - provide ACTUAL analysis.

Create exactly 5 slides with this EXACT structure:

SLIDE 1 - PROJECT OVERVIEW:
TITLE: [Create a compelling 4-6 word title based on the actual project]
THEME_SUGGESTION: tech_innovation
SLIDE_TYPE: title_slide
MAIN_POINTS:
- [Identify the specific technology stack used - languages, frameworks, libraries]
- [Describe the primary purpose and functionality of this application]
- [List 2-3 key features that make this project valuable]
- [Assess the project scope - simple tool, complex application, enterprise system]
- [Evaluate development maturity - prototype, MVP, production-ready, enterprise-grade]

SLIDE 2 - TECHNICAL ARCHITECTURE:
TITLE: [Create architecture-focused title like "Python-Streamlit Architecture" or "Full-Stack Technical Design"]
THEME_SUGGESTION: corporate_modern
SLIDE_TYPE: architecture_slide
MAIN_POINTS:
- [Identify core technologies: programming languages, web frameworks, databases]
- [Describe data storage and persistence: files, databases, cloud storage]
- [List API integrations and external services used]
- [Identify development tools: package managers, build tools, testing frameworks]
- [Describe deployment strategy: local, cloud, containerized, serverless]

SLIDE 3 - KEY FEATURES & CAPABILITIES:
TITLE: [Create feature-focused title like "Core Capabilities" or "Feature Showcase"]
THEME_SUGGESTION: creative_gradient
SLIDE_TYPE: features_slide
MAIN_POINTS:
- [Primary user-facing features that solve real problems]
- [Advanced or unique functionality that sets this apart]
- [Performance characteristics: speed, scalability, efficiency]
- [Security measures and data protection features]
- [Scalability features and growth potential]

SLIDE 4 - CODE QUALITY & ENGINEERING:
TITLE: [Create quality-focused title like "Engineering Excellence" or "Code Quality Standards"]
THEME_SUGGESTION: minimalist_luxury
SLIDE_TYPE: metrics_slide
MAIN_POINTS:
- [Code organization: file structure, modularity, separation of concerns]
- [Testing approach: unit tests, integration tests, quality assurance]
- [Documentation quality: README, code comments, API docs]
- [Development best practices: version control, code style, conventions]
- [Maintainability factors: code clarity, extensibility, technical debt]

SLIDE 5 - BUSINESS IMPACT & ROADMAP:
TITLE: [Create business-focused title like "Strategic Value" or "Business Impact"]
THEME_SUGGESTION: corporate_modern
SLIDE_TYPE: roadmap_slide
MAIN_POINTS:
- [Business value proposition: what problem does this solve]
- [Market opportunities: target users, potential market size]
- [Technical advantages: competitive benefits, innovation aspects]
- [Growth potential: scalability, expansion opportunities]
- [Future enhancement opportunities: roadmap, next features]

ANALYSIS GUIDELINES:
1. Extract ACTUAL technology stack from file extensions, imports, and dependencies
2. Identify REAL architectural patterns from folder structure and code organization
3. Assess ACTUAL code quality from file organization, naming conventions, and structure
4. Determine REAL project maturity from completeness, testing, documentation
5. Focus on CONCRETE business and technical value, not generic statements
6. Each bullet point should be 8-15 words, specific and actionable
7. Use technical terms appropriately but keep executive-friendly language
8. Base ALL analysis on the actual code and files provided

Repository Content to Analyze:
{truncated_content}

REMEMBER: Provide SPECIFIC, DETAILED content based on the actual repository, not generic placeholder text!
"""

    @staticmethod
    def get_content_slide_prompt(
        title: str, context: str, theme: DesignTheme = DesignTheme.CORPORATE_MODERN
    ) -> str:
        """
        Generate prompt for a single content slide.

        Args:
            title: Slide title
            context: Context information for content generation
            theme: Design theme for the slide

        Returns:
            Focused content generation prompt
        """
        return f"""
Create professional presentation content for a slide titled "{title}".

Context: {context}

Requirements:
- Generate 4-6 compelling bullet points
- Each point should be 8-15 words
- Focus on actionable insights and specific value
- Use professional, executive-friendly language
- Align with {theme.value} design aesthetic
- Ensure content is specific and concrete, not generic

Format your response exactly as:
TITLE: {title}
THEME_SUGGESTION: {theme.value}
SLIDE_TYPE: content_slide
MAIN_POINTS:
- [First specific, actionable point]
- [Second specific, actionable point]
- [Third specific, actionable point]
- [Fourth specific, actionable point]
- [Optional fifth point if relevant]
"""

    @staticmethod
    def get_fallback_content_template(
        project_type: str,
        tech_stack: List[str],
        complexity: str,
        maturity: str,
        file_count: int,
    ) -> str:
        """
        Generate professional fallback content when AI is unavailable.

        Args:
            project_type: Type of project (e.g., "AI-Powered Web Application")
            tech_stack: List of primary technologies
            complexity: Project complexity level
            maturity: Project maturity level
            file_count: Number of files in project

        Returns:
            Professional presentation content
        """
        primary_stack = ", ".join(tech_stack[:3]) if tech_stack else "Multi-technology"

        return f"""
SLIDE 1 - PROJECT OVERVIEW:
TITLE: {primary_stack} {project_type}
THEME_SUGGESTION: tech_innovation
SLIDE_TYPE: title_slide
MAIN_POINTS:
- Built with {primary_stack} technology stack for modern development
- {project_type} with {complexity.lower()} architecture and design
- {file_count} files analyzed showing comprehensive codebase structure
- {maturity} application with professional development practices
- Scalable solution designed for growth and enterprise deployment

SLIDE 2 - TECHNICAL ARCHITECTURE:
TITLE: Technology Stack & Architecture
THEME_SUGGESTION: corporate_modern
SLIDE_TYPE: architecture_slide
MAIN_POINTS:
- Core stack: {primary_stack} with modern development frameworks
- Modular architecture ensuring separation of concerns and maintainability
- Professional project structure following industry best practices
- Comprehensive dependency management and configuration setup
- {maturity} development environment with deployment readiness

SLIDE 3 - KEY FEATURES & CAPABILITIES:
TITLE: Core Features & Functionality
THEME_SUGGESTION: creative_gradient
SLIDE_TYPE: features_slide
MAIN_POINTS:
- Well-architected components delivering robust user functionality
- {complexity} feature implementation with modern UX/UI patterns
- Performance-optimized design ensuring scalable user experience
- Secure and reliable codebase with proper error handling
- Extensible architecture supporting future feature enhancements

SLIDE 4 - CODE QUALITY & ENGINEERING:
TITLE: Engineering Excellence Standards
THEME_SUGGESTION: minimalist_luxury
SLIDE_TYPE: metrics_slide
MAIN_POINTS:
- Clean code organization with {file_count} well-structured files
- Professional naming conventions and documentation standards
- Version control ready with proper Git configuration
- {maturity} codebase with comprehensive error handling
- Enterprise-ready deployment configuration and setup

SLIDE 5 - BUSINESS IMPACT & ROADMAP:
TITLE: Strategic Value & Market Potential
THEME_SUGGESTION: corporate_modern
SLIDE_TYPE: roadmap_slide
MAIN_POINTS:
- High business value solving real-world problems efficiently
- {complexity} solution targeting professional and enterprise markets
- Modern {primary_stack} technology ensuring long-term viability
- Scalable architecture supporting rapid business growth
- Strategic technical foundation for future product development
"""

    @staticmethod
    def get_custom_prompt_template(
        slide_count: int = 5,
        focus_areas: Optional[List[str]] = None,
        target_audience: str = "executives and technical leaders",
    ) -> str:
        """
        Generate a customizable prompt template.

        Args:
            slide_count: Number of slides to generate
            focus_areas: Specific areas to focus on (e.g., ["security", "scalability"])
            target_audience: Target presentation audience

        Returns:
            Customized prompt template
        """
        focus_instruction = ""
        if focus_areas:
            focus_instruction = f"\nSpecial focus areas: {', '.join(focus_areas)}"

        return f"""
As a world-class presentation expert, create a compelling {slide_count}-slide presentation analyzing this repository for {target_audience}.
{focus_instruction}

Ensure each slide:
- Has a compelling, specific title based on actual analysis
- Contains 4-6 bullet points of 8-15 words each
- Provides concrete insights, not generic statements
- Uses professional language appropriate for {target_audience}
- Aligns with modern presentation design principles

Follow the exact format:
SLIDE [number] - [CATEGORY]:
TITLE: [Specific title based on analysis]
THEME_SUGGESTION: [appropriate_theme]
SLIDE_TYPE: [slide_type]
MAIN_POINTS:
- [Specific, actionable point]
- [Specific, actionable point]
- [Specific, actionable point]
- [Specific, actionable point]
- [Optional fifth point]

Analyze the provided repository content and deliver insights that would impress {target_audience}.
"""

    @classmethod
    def get_theme_suggestions(cls) -> Dict[SlideType, DesignTheme]:
        """Get recommended themes for different slide types."""
        return {
            SlideType.TITLE_SLIDE: DesignTheme.TECH_INNOVATION,
            SlideType.ARCHITECTURE_SLIDE: DesignTheme.CORPORATE_MODERN,
            SlideType.FEATURES_SLIDE: DesignTheme.CREATIVE_GRADIENT,
            SlideType.METRICS_SLIDE: DesignTheme.MINIMALIST_LUXURY,
            SlideType.ROADMAP_SLIDE: DesignTheme.CORPORATE_MODERN,
            SlideType.CONTENT_SLIDE: DesignTheme.CORPORATE_MODERN,
        }

    @classmethod
    def validate_ai_response(cls, response: str) -> bool:
        """
        Validate that AI response follows expected format.

        Args:
            response: AI-generated response to validate

        Returns:
            True if response format is valid
        """
        required_patterns = [
            "SLIDE",
            "TITLE:",
            "THEME_SUGGESTION:",
            "SLIDE_TYPE:",
            "MAIN_POINTS:",
        ]

        return all(pattern in response for pattern in required_patterns)

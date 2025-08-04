"""
Design themes for the AI PowerPoint Framework.

This module defines professional design themes inspired by top creative agencies,
providing a structured approach to visual consistency across presentations.
"""

from enum import Enum
from typing import Dict, Any, List, Optional


class DesignTheme(Enum):
    """
    Professional design themes inspired by top creative agencies.

    Each theme represents a complete visual identity including colors,
    typography, spacing, and overall aesthetic approach.
    """

    CORPORATE_MODERN = "corporate_modern"
    CREATIVE_GRADIENT = "creative_gradient"
    MINIMALIST_LUXURY = "minimalist_luxury"
    TECH_INNOVATION = "tech_innovation"
    ADOBE_INSPIRED = "adobe_inspired"
    BEHANCE_STYLE = "behance_style"


class ThemeProperties:
    """
    Container class for theme-specific properties and metadata.

    This class provides additional information about each theme,
    including descriptions, use cases, and target audiences.
    """

    # Theme metadata and descriptions
    METADATA = {
        DesignTheme.CORPORATE_MODERN: {
            "name": "Corporate Modern",
            "description": "Professional and trustworthy design for business presentations",
            "primary_colors": ["Deep Navy", "Slate Gray", "Vibrant Blue"],
            "mood": "Professional, Trustworthy, Clean",
            "use_cases": [
                "Business meetings",
                "Executive presentations",
                "Financial reports",
            ],
            "target_audience": "Executives, Corporate teams, Professional services",
        },
        DesignTheme.CREATIVE_GRADIENT: {
            "name": "Creative Gradient",
            "description": "Bold and vibrant design for creative and marketing presentations",
            "primary_colors": ["Coral Red", "Teal", "Golden Yellow"],
            "mood": "Creative, Energetic, Bold",
            "use_cases": [
                "Marketing campaigns",
                "Creative pitches",
                "Product launches",
            ],
            "target_audience": "Creative teams, Marketing professionals, Startups",
        },
        DesignTheme.MINIMALIST_LUXURY: {
            "name": "Minimalist Luxury",
            "description": "Elegant and sophisticated design with minimal elements",
            "primary_colors": ["Almost Black", "Pure White", "Gold Accent"],
            "mood": "Elegant, Sophisticated, Premium",
            "use_cases": ["Luxury brands", "High-end services", "Premium products"],
            "target_audience": "Luxury brands, High-end clients, Premium services",
        },
        DesignTheme.TECH_INNOVATION: {
            "name": "Tech Innovation",
            "description": "Modern and futuristic design for technology presentations",
            "primary_colors": ["Deep Blue", "Cyan", "Space Dark"],
            "mood": "Innovative, Futuristic, Technical",
            "use_cases": ["Tech demos", "Product launches", "Developer presentations"],
            "target_audience": "Tech companies, Developers, Innovation teams",
        },
        DesignTheme.ADOBE_INSPIRED: {
            "name": "Adobe Inspired",
            "description": "Creative agency-style design with artistic flair",
            "primary_colors": ["Adobe Red", "Creative Purple", "Design Orange"],
            "mood": "Artistic, Creative, Inspiring",
            "use_cases": [
                "Design portfolios",
                "Creative showcases",
                "Agency presentations",
            ],
            "target_audience": "Designers, Creative agencies, Artists",
        },
        DesignTheme.BEHANCE_STYLE: {
            "name": "Behance Style",
            "description": "Portfolio-grade design for showcasing creative work",
            "primary_colors": ["Portfolio Blue", "Showcase Gray", "Creative White"],
            "mood": "Portfolio-ready, Professional creative, Showcase-worthy",
            "use_cases": [
                "Portfolio presentations",
                "Creative showcases",
                "Design reviews",
            ],
            "target_audience": "Creative professionals, Portfolio reviews, Design teams",
        },
    }

    @classmethod
    def get_theme_info(cls, theme: DesignTheme) -> Dict[str, Any]:
        """
        Get comprehensive information about a specific theme.

        Args:
            theme (DesignTheme): The theme to get information for

        Returns:
            Dict[str, Any]: Complete theme information including metadata
        """
        return cls.METADATA.get(theme, {})

    @classmethod
    def get_theme_description(cls, theme: DesignTheme) -> str:
        """
        Get a brief description of the theme.

        Args:
            theme (DesignTheme): The theme to describe

        Returns:
            str: Theme description
        """
        return cls.METADATA.get(theme, {}).get(
            "description", "Professional design theme"
        )

    @classmethod
    def get_recommended_themes_for_content(cls, content_type: str) -> list[DesignTheme]:
        """
        Get recommended themes based on content type.

        Args:
            content_type (str): Type of content (e.g., "business", "creative", "tech")

        Returns:
            list[DesignTheme]: List of recommended themes
        """
        recommendations = {
            "business": [DesignTheme.CORPORATE_MODERN, DesignTheme.MINIMALIST_LUXURY],
            "creative": [
                DesignTheme.CREATIVE_GRADIENT,
                DesignTheme.ADOBE_INSPIRED,
                DesignTheme.BEHANCE_STYLE,
            ],
            "technology": [DesignTheme.TECH_INNOVATION, DesignTheme.CORPORATE_MODERN],
            "startup": [DesignTheme.CREATIVE_GRADIENT, DesignTheme.TECH_INNOVATION],
            "luxury": [DesignTheme.MINIMALIST_LUXURY, DesignTheme.CORPORATE_MODERN],
            "portfolio": [DesignTheme.BEHANCE_STYLE, DesignTheme.ADOBE_INSPIRED],
            "default": [DesignTheme.CORPORATE_MODERN, DesignTheme.CREATIVE_GRADIENT],
        }

        return recommendations.get(content_type.lower(), recommendations["default"])


class ThemeSelector:
    """
    Intelligent theme selection based on content analysis.

    This class provides algorithms for automatically selecting the most
    appropriate theme based on content type, target audience, and context.
    """

    @staticmethod
    def select_theme_by_keywords(content: str) -> DesignTheme:
        """
        Select a theme based on keywords found in the content.

        Args:
            content (str): Content to analyze for theme selection

        Returns:
            DesignTheme: Most appropriate theme based on content analysis
        """
        content_lower = content.lower()

        # Define keyword mappings for each theme
        theme_keywords = {
            DesignTheme.TECH_INNOVATION: [
                "technology",
                "tech",
                "innovation",
                "ai",
                "machine learning",
                "data",
                "api",
                "software",
                "development",
                "programming",
                "algorithm",
                "digital",
                "automation",
                "cloud",
                "scalable",
            ],
            DesignTheme.CORPORATE_MODERN: [
                "business",
                "corporate",
                "professional",
                "enterprise",
                "executive",
                "strategy",
                "management",
                "finance",
                "investment",
                "corporate",
                "quarterly",
                "annual",
                "board",
                "stakeholder",
                "revenue",
            ],
            DesignTheme.CREATIVE_GRADIENT: [
                "creative",
                "design",
                "marketing",
                "brand",
                "campaign",
                "visual",
                "artistic",
                "innovative",
                "colorful",
                "bold",
                "engaging",
                "dynamic",
                "vibrant",
                "modern",
                "trendy",
            ],
            DesignTheme.MINIMALIST_LUXURY: [
                "luxury",
                "premium",
                "elegant",
                "sophisticated",
                "high-end",
                "exclusive",
                "refined",
                "quality",
                "excellence",
                "prestigious",
                "minimalist",
                "clean",
                "simple",
                "pure",
                "classic",
            ],
            DesignTheme.ADOBE_INSPIRED: [
                "portfolio",
                "showcase",
                "creative work",
                "design portfolio",
                "artistic",
                "visual arts",
                "graphic design",
                "creative agency",
                "branding",
                "identity",
                "creative process",
                "inspiration",
            ],
            DesignTheme.BEHANCE_STYLE: [
                "portfolio",
                "creative showcase",
                "design work",
                "creative professional",
                "artistic portfolio",
                "design portfolio",
                "creative collection",
                "visual portfolio",
                "design showcase",
                "creative display",
            ],
        }

        # Score each theme based on keyword matches
        theme_scores = {}
        for theme, keywords in theme_keywords.items():
            score = sum(1 for keyword in keywords if keyword in content_lower)
            theme_scores[theme] = score

        # Return the theme with the highest score, default to CORPORATE_MODERN
        if not theme_scores or max(theme_scores.values()) == 0:
            return DesignTheme.CORPORATE_MODERN

        return max(theme_scores.items(), key=lambda x: x[1])[0]

    @staticmethod
    def select_theme_by_file_types(file_extensions: List[str]) -> DesignTheme:
        """
        Select a theme based on the types of files in the repository.

        Args:
            file_extensions (list[str]): List of file extensions found

        Returns:
            DesignTheme: Most appropriate theme based on file types
        """
        extensions_lower = [ext.lower() for ext in file_extensions]

        # Programming languages and tech indicators
        if any(
            ext in extensions_lower
            for ext in [".py", ".js", ".ts", ".java", ".cpp", ".go", ".rs"]
        ):
            return DesignTheme.TECH_INNOVATION

        # Web development
        if any(
            ext in extensions_lower
            for ext in [".html", ".css", ".scss", ".jsx", ".vue"]
        ):
            return DesignTheme.CREATIVE_GRADIENT

        # Design files
        if any(
            ext in extensions_lower for ext in [".psd", ".ai", ".sketch", ".fig", ".xd"]
        ):
            return DesignTheme.ADOBE_INSPIRED

        # Documentation heavy (business/corporate)
        if any(
            ext in extensions_lower for ext in [".md", ".doc", ".docx", ".pdf", ".txt"]
        ):
            return DesignTheme.CORPORATE_MODERN

        # Default fallback
        return DesignTheme.CORPORATE_MODERN

    @staticmethod
    def select_theme_smart(
        content: str, file_extensions: Optional[List[str]] = None
    ) -> DesignTheme:
        """
        Intelligent theme selection combining multiple factors.

        Args:
            content (str): Repository content to analyze
            file_extensions (list[str], optional): File extensions found in repository

        Returns:
            DesignTheme: Best matching theme based on comprehensive analysis
        """
        # Get theme suggestions from different methods
        content_theme = ThemeSelector.select_theme_by_keywords(content)

        file_theme = DesignTheme.CORPORATE_MODERN
        if file_extensions:
            file_theme = ThemeSelector.select_theme_by_file_types(file_extensions)

        # If both methods agree, use that theme
        if content_theme == file_theme:
            return content_theme

        # For tech content with design files, prefer creative themes
        if content_theme == DesignTheme.TECH_INNOVATION and file_theme in [
            DesignTheme.CREATIVE_GRADIENT,
            DesignTheme.ADOBE_INSPIRED,
        ]:
            return file_theme

        # Default to content-based selection as it's more comprehensive
        return content_theme


# Export all theme-related classes and enums
__all__ = ["DesignTheme", "ThemeProperties", "ThemeSelector"]

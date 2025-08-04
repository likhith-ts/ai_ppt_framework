"""
Professional color system for the AI PowerPoint Framework.

This module provides industry-grade color palettes with psychological impact,
color theory utilities, and harmonious color generation for presentations.
"""

import colorsys
from dataclasses import dataclass
from typing import List, Dict, Tuple
from .themes import DesignTheme


@dataclass
class ColorPalette:
    """
    Industry-grade color palette with psychological impact.

    This class represents a complete color scheme for presentations,
    including primary colors, text colors, status colors, and gradients.
    All colors are stored as RGB integers for compatibility with PowerPoint.

    Attributes:
        primary (int): Main brand/theme color
        secondary (int): Supporting color
        accent (int): Highlight/call-to-action color
        background (int): Main background color
        text_primary (int): Primary text color
        text_secondary (int): Secondary/muted text color
        success (int): Success state color (green)
        warning (int): Warning state color (orange/yellow)
        gradient_start (int): Starting color for gradients
        gradient_end (int): Ending color for gradients
    """

    primary: int
    secondary: int
    accent: int
    background: int
    text_primary: int
    text_secondary: int
    success: int
    warning: int
    gradient_start: int
    gradient_end: int

    @classmethod
    def get_harmony_colors(
        cls, base_color: int, harmony_type: str = "complementary"
    ) -> List[int]:
        """
        Generate harmonious colors using color theory.

        This method uses mathematical color relationships to create
        visually pleasing color combinations from a single base color.

        Args:
            base_color (int): Base color as RGB integer (0xRRGGBB)
            harmony_type (str): Type of harmony ("complementary", "triadic", "analogous")

        Returns:
            List[int]: List of harmonious colors as RGB integers
        """
        # Convert RGB integer to individual components
        r = (base_color >> 16) & 255
        g = (base_color >> 8) & 255
        b = base_color & 255

        # Convert to HSV for color theory calculations
        h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)

        colors = []

        if harmony_type == "complementary":
            # Original color + opposite on color wheel
            colors.append(base_color)
            comp_h = (h + 0.5) % 1.0
            comp_rgb = colorsys.hsv_to_rgb(comp_h, s, v)
            comp_color = (
                int(comp_rgb[0] * 255) << 16
                | int(comp_rgb[1] * 255) << 8
                | int(comp_rgb[2] * 255)
            )
            colors.append(comp_color)

        elif harmony_type == "triadic":
            # Three colors equally spaced on color wheel
            for i in range(3):
                new_h = (h + i * 0.333) % 1.0
                rgb = colorsys.hsv_to_rgb(new_h, s, v)
                color = (
                    int(rgb[0] * 255) << 16 | int(rgb[1] * 255) << 8 | int(rgb[2] * 255)
                )
                colors.append(color)

        elif harmony_type == "analogous":
            # Colors adjacent on the color wheel (±30 degrees)
            for i in range(-1, 2):
                new_h = (h + i * 0.083) % 1.0  # 30 degrees = 1/12 of circle
                rgb = colorsys.hsv_to_rgb(new_h, s, v)
                color = (
                    int(rgb[0] * 255) << 16 | int(rgb[1] * 255) << 8 | int(rgb[2] * 255)
                )
                colors.append(color)

        return colors

    def get_tints(self, color: int, steps: int = 5) -> List[int]:
        """
        Generate tints (lighter versions) of a color.

        Args:
            color (int): Base color as RGB integer
            steps (int): Number of tint variations to generate

        Returns:
            List[int]: List of tints from darkest to lightest
        """
        r = (color >> 16) & 255
        g = (color >> 8) & 255
        b = color & 255

        tints = []
        for i in range(steps):
            # Linear interpolation towards white
            factor = i / (steps - 1)
            tint_r = int(r + (255 - r) * factor)
            tint_g = int(g + (255 - g) * factor)
            tint_b = int(b + (255 - b) * factor)

            tint = (tint_r << 16) | (tint_g << 8) | tint_b
            tints.append(tint)

        return tints

    def get_shades(self, color: int, steps: int = 5) -> List[int]:
        """
        Generate shades (darker versions) of a color.

        Args:
            color (int): Base color as RGB integer
            steps (int): Number of shade variations to generate

        Returns:
            List[int]: List of shades from lightest to darkest
        """
        r = (color >> 16) & 255
        g = (color >> 8) & 255
        b = color & 255

        shades = []
        for i in range(steps):
            # Linear interpolation towards black
            factor = 1 - (i / (steps - 1))
            shade_r = int(r * factor)
            shade_g = int(g * factor)
            shade_b = int(b * factor)

            shade = (shade_r << 16) | (shade_g << 8) | shade_b
            shades.append(shade)

        return shades

    def get_contrast_ratio(self, color1: int, color2: int) -> float:
        """
        Calculate contrast ratio between two colors (WCAG standard).

        Args:
            color1 (int): First color as RGB integer
            color2 (int): Second color as RGB integer

        Returns:
            float: Contrast ratio (1.0 to 21.0)
        """

        def get_luminance(color: int) -> float:
            r = ((color >> 16) & 255) / 255.0
            g = ((color >> 8) & 255) / 255.0
            b = (color & 255) / 255.0

            # Convert to linear RGB
            def to_linear(c):
                return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

            r_lin = to_linear(r)
            g_lin = to_linear(g)
            b_lin = to_linear(b)

            # Calculate relative luminance
            return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin

        lum1 = get_luminance(color1)
        lum2 = get_luminance(color2)

        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)

        return (lighter + 0.05) / (darker + 0.05)


class DesignPalettes:
    """
    Collection of industry-inspired color palettes.

    This class provides pre-defined color palettes for each design theme,
    carefully crafted for professional presentations and optimal readability.
    """

    # Corporate Modern - Professional blues and grays
    CORPORATE_MODERN = ColorPalette(
        primary=0x2C3E50,  # Deep navy blue
        secondary=0x34495E,  # Slate gray
        accent=0x3498DB,  # Vibrant blue
        background=0xF8F9FA,  # Off white
        text_primary=0x2C3E50,  # Dark navy for text
        text_secondary=0x7F8C8D,  # Medium gray for secondary text
        success=0x27AE60,  # Professional green
        warning=0xF39C12,  # Professional orange
        gradient_start=0x667EEA,  # Gradient blue start
        gradient_end=0x764BA2,  # Gradient purple end
    )

    # Creative Gradient - Bold and vibrant colors
    CREATIVE_GRADIENT = ColorPalette(
        primary=0xFF6B6B,  # Coral red
        secondary=0x4ECDC4,  # Turquoise teal
        accent=0xFFE66D,  # Golden yellow
        background=0x1A1A2E,  # Dark navy background
        text_primary=0xFFFFFF,  # White text
        text_secondary=0xE0E0E0,  # Light gray text
        success=0x95E1D3,  # Mint green
        warning=0xFFA07A,  # Light salmon
        gradient_start=0xFF6B6B,  # Coral gradient start
        gradient_end=0x4ECDC4,  # Teal gradient end
    )

    # Minimalist Luxury - Elegant blacks, whites, and gold
    MINIMALIST_LUXURY = ColorPalette(
        primary=0x1C1C1C,  # Almost black
        secondary=0xF5F5F5,  # Light gray
        accent=0xC9B037,  # Elegant gold
        background=0xFFFFFF,  # Pure white
        text_primary=0x1C1C1C,  # Almost black text
        text_secondary=0x666666,  # Medium gray text
        success=0x28A745,  # Clean green
        warning=0xFFC107,  # Gold warning
        gradient_start=0xC9B037,  # Gold gradient start
        gradient_end=0xFFF8DC,  # Cornsilk gradient end
    )

    # Tech Innovation - Futuristic blues and cyans
    TECH_INNOVATION = ColorPalette(
        primary=0x0D47A1,  # Deep tech blue
        secondary=0x1565C0,  # Medium blue
        accent=0x00E5FF,  # Electric cyan
        background=0x0A0E27,  # Dark space background
        text_primary=0xFFFFFF,  # White text
        text_secondary=0xB0BEC5,  # Light blue-gray text
        success=0x00C853,  # Tech green
        warning=0xFF9800,  # Tech orange
        gradient_start=0x0D47A1,  # Deep blue gradient start
        gradient_end=0x00E5FF,  # Cyan gradient end
    )

    # Adobe Inspired - Creative agency colors
    ADOBE_INSPIRED = ColorPalette(
        primary=0xFF0000,  # Adobe red
        secondary=0x9900FF,  # Creative purple
        accent=0xFF6600,  # Design orange
        background=0xF6F6F6,  # Light creative background
        text_primary=0x2D2D2D,  # Dark charcoal text
        text_secondary=0x666666,  # Medium gray text
        success=0x00CC66,  # Creative green
        warning=0xFFCC00,  # Creative yellow
        gradient_start=0xFF0000,  # Red gradient start
        gradient_end=0x9900FF,  # Purple gradient end
    )

    # Behance Style - Portfolio-grade colors
    BEHANCE_STYLE = ColorPalette(
        primary=0x053EFF,  # Behance blue
        secondary=0x4A90E2,  # Portfolio blue
        accent=0x1769FF,  # Showcase blue
        background=0xFAFAFA,  # Portfolio background
        text_primary=0x191919,  # Portfolio text
        text_secondary=0x696969,  # Secondary portfolio text
        success=0x7ED321,  # Portfolio green
        warning=0xF5A623,  # Portfolio orange
        gradient_start=0x053EFF,  # Behance blue gradient start
        gradient_end=0x4A90E2,  # Light blue gradient end
    )

    @classmethod
    def get_palette(cls, theme: DesignTheme) -> ColorPalette:
        """
        Get the color palette for a specific design theme.

        Args:
            theme (DesignTheme): The design theme to get colors for

        Returns:
            ColorPalette: Complete color palette for the theme
        """
        palette_map = {
            DesignTheme.CORPORATE_MODERN: cls.CORPORATE_MODERN,
            DesignTheme.CREATIVE_GRADIENT: cls.CREATIVE_GRADIENT,
            DesignTheme.MINIMALIST_LUXURY: cls.MINIMALIST_LUXURY,
            DesignTheme.TECH_INNOVATION: cls.TECH_INNOVATION,
            DesignTheme.ADOBE_INSPIRED: cls.ADOBE_INSPIRED,
            DesignTheme.BEHANCE_STYLE: cls.BEHANCE_STYLE,
        }

        return palette_map.get(theme, cls.CORPORATE_MODERN)

    @classmethod
    def get_all_palettes(cls) -> Dict[DesignTheme, ColorPalette]:
        """
        Get all available color palettes.

        Returns:
            Dict[DesignTheme, ColorPalette]: Dictionary mapping themes to palettes
        """
        return {
            DesignTheme.CORPORATE_MODERN: cls.CORPORATE_MODERN,
            DesignTheme.CREATIVE_GRADIENT: cls.CREATIVE_GRADIENT,
            DesignTheme.MINIMALIST_LUXURY: cls.MINIMALIST_LUXURY,
            DesignTheme.TECH_INNOVATION: cls.TECH_INNOVATION,
            DesignTheme.ADOBE_INSPIRED: cls.ADOBE_INSPIRED,
            DesignTheme.BEHANCE_STYLE: cls.BEHANCE_STYLE,
        }


class ColorUtilities:
    """
    Utility functions for color manipulation and analysis.

    This class provides helper functions for common color operations
    used throughout the framework.
    """

    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """Convert RGB values to hex string."""
        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex string to RGB tuple."""
        hex_color = hex_color.lstrip("#")
        rgb_values = [int(hex_color[i : i + 2], 16) for i in (0, 2, 4)]
        return (rgb_values[0], rgb_values[1], rgb_values[2])

    @staticmethod
    def int_to_rgb(color_int: int) -> Tuple[int, int, int]:
        """Convert RGB integer to RGB tuple."""
        r = (color_int >> 16) & 255
        g = (color_int >> 8) & 255
        b = color_int & 255
        return (r, g, b)

    @staticmethod
    def rgb_to_int(r: int, g: int, b: int) -> int:
        """Convert RGB tuple to RGB integer."""
        return (r << 16) | (g << 8) | b

    @staticmethod
    def is_dark_color(color: int, threshold: float = 0.5) -> bool:
        """
        Determine if a color is dark (for choosing text color).

        Args:
            color (int): Color as RGB integer
            threshold (float): Threshold for darkness (0.0-1.0)

        Returns:
            bool: True if color is dark
        """
        r, g, b = ColorUtilities.int_to_rgb(color)

        # Calculate perceived brightness using standard formula
        brightness = (r * 0.299 + g * 0.587 + b * 0.114) / 255.0

        return brightness < threshold

    @staticmethod
    def get_readable_text_color(background_color: int) -> int:
        """
        Get the best text color (black or white) for a background.

        Args:
            background_color (int): Background color as RGB integer

        Returns:
            int: Either black (0x000000) or white (0xFFFFFF)
        """
        return 0xFFFFFF if ColorUtilities.is_dark_color(background_color) else 0x000000


# Export all color-related classes
__all__ = ["ColorPalette", "DesignPalettes", "ColorUtilities"]

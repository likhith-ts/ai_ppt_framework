"""
Design constants and measurements for the AI PowerPoint Framework.

This module contains all the design constants, measurements, and layout specifications
extracted from the original smartArt.py file. It follows professional design principles
based on an 8-point grid system for pixel-perfect alignment.
"""

# PowerPoint slide dimensions (in points)
# Standard 16:9 aspect ratio for modern presentations
SLIDE_WIDTH = 960  # Standard 16:9 slide width in points
SLIDE_HEIGHT = 540  # Standard 16:9 slide height in points

# Professional spacing system based on 8-point grid
# This ensures consistent visual rhythm and professional appearance
SPACING_UNIT = 8  # Base unit for all spacing calculations

# Margin definitions using the 8-point grid system
MARGIN_SMALL = SPACING_UNIT * 3  # 24pt - For tight layouts
MARGIN_MEDIUM = SPACING_UNIT * 5  # 40pt - Standard margin
MARGIN_LARGE = SPACING_UNIT * 8  # 64pt - For spacious layouts

# Layout spacing
GUTTER = SPACING_UNIT * 2  # 16pt - Space between elements
COMPONENT_SPACING = SPACING_UNIT * 4  # 32pt - Space between major components

# Content area calculations
# These define the safe content area within slides, accounting for margins
CONTENT_WIDTH = SLIDE_WIDTH - (2 * MARGIN_LARGE)  # 832pt
CONTENT_HEIGHT = SLIDE_HEIGHT - (2 * MARGIN_LARGE) - 80  # 396pt (minus title area)

# Title and content positioning
TITLE_HEIGHT = 80  # Standard height for slide titles
TITLE_Y_POSITION = MARGIN_LARGE  # Top margin for titles
CONTENT_Y_POSITION = (
    TITLE_Y_POSITION + TITLE_HEIGHT + COMPONENT_SPACING
)  # Content starts below title

# Typography scale based on modular scale
# Font sizes follow a mathematical progression for visual hierarchy
FONT_SIZE_GIANT = 48  # For major headlines
FONT_SIZE_LARGE = 36  # For slide titles
FONT_SIZE_TITLE = 32  # For section titles
FONT_SIZE_SUBTITLE = 24  # For subtitles
FONT_SIZE_BODY = 18  # For body text
FONT_SIZE_CAPTION = 14  # For captions and notes
FONT_SIZE_SMALL = 12  # For fine print

# Line height multipliers for optimal readability
LINE_HEIGHT_TIGHT = 1.1  # For headlines
LINE_HEIGHT_NORMAL = 1.4  # For body text
LINE_HEIGHT_LOOSE = 1.6  # For better readability

# Standard element dimensions
BUTTON_HEIGHT = 40  # Standard button height
INPUT_HEIGHT = 36  # Standard input field height
CARD_MIN_HEIGHT = 120  # Minimum height for cards
CARD_MAX_HEIGHT = 200  # Maximum height for cards

# Grid system for layouts
GRID_COLUMNS = 12  # Number of columns in the grid system
GRID_GUTTER = GUTTER  # Space between grid columns

# Animation and transition timings (in milliseconds)
ANIMATION_FAST = 150  # Quick transitions
ANIMATION_NORMAL = 300  # Standard transitions
ANIMATION_SLOW = 500  # Slower, more dramatic transitions

# Z-index layers for element stacking
Z_INDEX_BACKGROUND = 0  # Background elements
Z_INDEX_CONTENT = 10  # Main content
Z_INDEX_OVERLAY = 20  # Overlays and modals
Z_INDEX_TOOLTIP = 30  # Tooltips and popovers

# Border radius values for consistent rounded corners
BORDER_RADIUS_SMALL = 4  # Subtle rounding
BORDER_RADIUS_MEDIUM = 8  # Standard rounding
BORDER_RADIUS_LARGE = 16  # More pronounced rounding
BORDER_RADIUS_CIRCLE = 50  # For circular elements (percentage)

# Shadow definitions for depth
SHADOW_SUBTLE = "0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)"
SHADOW_NORMAL = "0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23)"
SHADOW_HEAVY = "0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23)"

# Breakpoints for responsive design (if needed)
BREAKPOINT_MOBILE = 480
BREAKPOINT_TABLET = 768
BREAKPOINT_DESKTOP = 1024
BREAKPOINT_LARGE = 1440

# Supported themes for presentations
SUPPORTED_THEMES = {
    "corporate_modern": "Corporate Modern",
    "academic_formal": "Academic Formal",
    "creative_vibrant": "Creative Vibrant",
    "minimal_clean": "Minimal Clean",
    "tech_startup": "Tech Startup",
    "consulting_professional": "Consulting Professional",
}

# Default theme
DEFAULT_THEME = "corporate_modern"

# File format constants
SUPPORTED_UPLOAD_FORMATS = [".zip"]
SUPPORTED_OUTPUT_FORMATS = [".pptx"]
MAX_UPLOAD_SIZE_MB = 100

# API configuration
DEFAULT_MAX_SLIDES = 10
DEFAULT_MAX_POINTS_PER_SLIDE = 6
DEFAULT_TIMEOUT_SECONDS = 300


class LayoutConstants:
    """
    Container class for layout-specific constants.

    This class organizes layout constants into logical groups for
    better organization and easier maintenance.
    """

    # Slide layout constants
    SLIDE = {
        "width": SLIDE_WIDTH,
        "height": SLIDE_HEIGHT,
        "aspect_ratio": SLIDE_WIDTH / SLIDE_HEIGHT,
    }

    # Margin constants
    MARGINS = {"small": MARGIN_SMALL, "medium": MARGIN_MEDIUM, "large": MARGIN_LARGE}

    # Spacing constants
    SPACING = {"unit": SPACING_UNIT, "gutter": GUTTER, "component": COMPONENT_SPACING}

    # Content area constants
    CONTENT = {
        "width": CONTENT_WIDTH,
        "height": CONTENT_HEIGHT,
        "x_position": MARGIN_LARGE,
        "y_position": CONTENT_Y_POSITION,
    }

    # Title area constants
    TITLE = {
        "height": TITLE_HEIGHT,
        "y_position": TITLE_Y_POSITION,
        "width": CONTENT_WIDTH,
        "x_position": MARGIN_LARGE,
    }


class TypographyConstants:
    """
    Container class for typography-specific constants.

    This class provides a structured way to access font sizes,
    line heights, and other typography-related values.
    """

    # Font size scale
    SIZES = {
        "giant": FONT_SIZE_GIANT,
        "large": FONT_SIZE_LARGE,
        "title": FONT_SIZE_TITLE,
        "subtitle": FONT_SIZE_SUBTITLE,
        "body": FONT_SIZE_BODY,
        "caption": FONT_SIZE_CAPTION,
        "small": FONT_SIZE_SMALL,
    }

    # Line height multipliers
    LINE_HEIGHTS = {
        "tight": LINE_HEIGHT_TIGHT,
        "normal": LINE_HEIGHT_NORMAL,
        "loose": LINE_HEIGHT_LOOSE,
    }

    # Font families (PowerPoint compatible)
    FAMILIES = {
        "primary": "Calibri",  # Modern, professional
        "secondary": "Arial",  # Classic, readable
        "monospace": "Consolas",  # For code
        "serif": "Times New Roman",  # For formal documents
    }


class ComponentConstants:
    """
    Container class for component-specific constants.

    This class defines standard dimensions and properties
    for common UI components.
    """

    # Button constants
    BUTTON = {
        "height": BUTTON_HEIGHT,
        "padding_x": SPACING_UNIT * 3,
        "padding_y": SPACING_UNIT * 1.5,
        "border_radius": BORDER_RADIUS_MEDIUM,
    }

    # Card constants
    CARD = {
        "min_height": CARD_MIN_HEIGHT,
        "max_height": CARD_MAX_HEIGHT,
        "padding": SPACING_UNIT * 3,
        "border_radius": BORDER_RADIUS_LARGE,
    }

    # Input field constants
    INPUT = {
        "height": INPUT_HEIGHT,
        "padding_x": SPACING_UNIT * 2,
        "border_radius": BORDER_RADIUS_SMALL,
    }


def get_responsive_font_size(base_size: int, scale_factor: float = 1.0) -> int:
    """
    Calculate responsive font size based on base size and scale factor.

    Args:
        base_size (int): Base font size in points
        scale_factor (float): Scaling factor (1.0 = no change)

    Returns:
        int: Scaled font size in points
    """
    return max(8, int(base_size * scale_factor))  # Minimum 8pt font


def get_grid_width(columns: int, total_columns: int = GRID_COLUMNS) -> int:
    """
    Calculate width for a grid column span.

    Args:
        columns (int): Number of columns to span
        total_columns (int): Total columns in grid (default: 12)

    Returns:
        int: Width in points for the specified column span
    """
    column_width = (CONTENT_WIDTH - (GUTTER * (total_columns - 1))) / total_columns
    return int((column_width * columns) + (GUTTER * (columns - 1)))


def get_vertical_rhythm(lines: int) -> int:
    """
    Calculate vertical spacing based on line height rhythm.

    Args:
        lines (int): Number of line heights

    Returns:
        int: Vertical spacing in points
    """
    base_line_height = FONT_SIZE_BODY * LINE_HEIGHT_NORMAL
    return int(base_line_height * lines)

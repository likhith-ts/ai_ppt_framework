"""
Background generation and styling for presentations.

This module provides intelligent background generation capabilities,
creating appropriate backgrounds based on content and design themes.
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import random

from core.exceptions import FrameworkError
from design.color_system import ColorPalette
from design.themes import DesignTheme


class BackgroundStyle(Enum):
    """Background styles supported by the framework."""
    
    SOLID = "solid"
    GRADIENT = "gradient"
    PATTERN = "pattern"
    TEXTURE = "texture"
    IMAGE = "image"
    GEOMETRIC = "geometric"
    ABSTRACT = "abstract"
    PROFESSIONAL = "professional"


class GradientDirection(Enum):
    """Gradient direction options."""
    
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    DIAGONAL_UP = "diagonal_up"
    DIAGONAL_DOWN = "diagonal_down"
    RADIAL = "radial"


@dataclass
class BackgroundConfig:
    """Configuration for background generation."""
    
    style: BackgroundStyle
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    opacity: float = 1.0
    gradient_direction: Optional[GradientDirection] = None
    pattern_type: Optional[str] = None
    texture_intensity: float = 0.5
    geometric_complexity: int = 3
    custom_properties: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.custom_properties is None:
            self.custom_properties = {}


@dataclass
class GeneratedBackground:
    """Represents a generated background."""
    
    config: BackgroundConfig
    css_properties: Dict[str, str]
    powerpoint_properties: Dict[str, Any]
    description: str
    preview_data: Optional[Dict[str, Any]] = None


class BackgroundGenerator:
    """
    Generator for creating presentation backgrounds.
    
    This class provides intelligent background generation based on
    content themes, design requirements, and aesthetic preferences.
    """
    
    def __init__(self, design_theme: Optional[DesignTheme] = None):
        """
        Initialize the background generator.
        
        Args:
            design_theme: Design theme for background styling
        """
        self.design_theme = design_theme
        self._pattern_library = self._init_pattern_library()
        self._texture_library = self._init_texture_library()
        self._geometric_library = self._init_geometric_library()
    
    def generate_background(
        self,
        content_type: str,
        color_palette: Optional[ColorPalette] = None,
        style: Optional[BackgroundStyle] = None,
        custom_config: Optional[BackgroundConfig] = None,
    ) -> GeneratedBackground:
        """
        Generate a background based on content and requirements.
        
        Args:
            content_type: Type of content (e.g., "technical", "business", "creative")
            color_palette: Color palette to use
            style: Override background style
            custom_config: Custom background configuration
            
        Returns:
            GeneratedBackground: Generated background
        """
        if custom_config:
            config = custom_config
        else:
            config = self._create_config_for_content(content_type, color_palette, style)
        
        return self._generate_from_config(config)
    
    def generate_theme_background(
        self,
        theme: DesignTheme,
        slide_type: str = "content",
        variation: int = 0,
    ) -> GeneratedBackground:
        """
        Generate a background based on a design theme.
        
        Args:
            theme: Design theme to use
            slide_type: Type of slide (title, content, section, etc.)
            variation: Style variation (0-2)
            
        Returns:
            GeneratedBackground: Generated background
        """
        config = self._create_theme_config(theme, slide_type, variation)
        return self._generate_from_config(config)
    
    def create_gradient_background(
        self,
        colors: List[str],
        direction: GradientDirection = GradientDirection.DIAGONAL_DOWN,
        opacity: float = 1.0,
    ) -> GeneratedBackground:
        """
        Create a gradient background with specified colors.
        
        Args:
            colors: List of colors for the gradient
            direction: Gradient direction
            opacity: Background opacity
            
        Returns:
            GeneratedBackground: Generated gradient background
        """
        config = BackgroundConfig(
            style=BackgroundStyle.GRADIENT,
            primary_color=colors[0] if colors else "#ffffff",
            secondary_color=colors[1] if len(colors) > 1 else colors[0],
            opacity=opacity,
            gradient_direction=direction,
        )
        
        return self._generate_from_config(config)
    
    def create_pattern_background(
        self,
        pattern_type: str,
        base_color: str,
        accent_color: str,
        intensity: float = 0.3,
    ) -> GeneratedBackground:
        """
        Create a pattern background.
        
        Args:
            pattern_type: Type of pattern
            base_color: Base color
            accent_color: Accent color
            intensity: Pattern intensity
            
        Returns:
            GeneratedBackground: Generated pattern background
        """
        config = BackgroundConfig(
            style=BackgroundStyle.PATTERN,
            primary_color=base_color,
            secondary_color=accent_color,
            pattern_type=pattern_type,
            opacity=intensity,
        )
        
        return self._generate_from_config(config)
    
    def _create_config_for_content(
        self,
        content_type: str,
        color_palette: Optional[ColorPalette],
        style: Optional[BackgroundStyle],
    ) -> BackgroundConfig:
        """Create background configuration based on content type."""
        content_type_lower = content_type.lower()
        
        # Determine style based on content type
        if style is None:
            if "technical" in content_type_lower or "code" in content_type_lower:
                style = BackgroundStyle.GEOMETRIC
            elif "business" in content_type_lower or "corporate" in content_type_lower:
                style = BackgroundStyle.PROFESSIONAL
            elif "creative" in content_type_lower or "design" in content_type_lower:
                style = BackgroundStyle.ABSTRACT
            else:
                style = BackgroundStyle.GRADIENT
        
        # Get colors from palette
        primary_color = "#ffffff"
        secondary_color = "#f0f0f0"
        
        if color_palette:
            primary_color = color_palette.background
            secondary_color = color_palette.secondary
        
        return BackgroundConfig(
            style=style,
            primary_color=primary_color,
            secondary_color=secondary_color,
            opacity=0.95,
            gradient_direction=GradientDirection.DIAGONAL_DOWN,
        )
    
    def _create_theme_config(
        self,
        theme: DesignTheme,
        slide_type: str,
        variation: int,
    ) -> BackgroundConfig:
        """Create background configuration based on design theme."""
        theme_configs = {
            DesignTheme.CORPORATE_MODERN: {
                "style": BackgroundStyle.PROFESSIONAL,
                "gradient_direction": GradientDirection.DIAGONAL_DOWN,
                "opacity": 1.0,
            },
            DesignTheme.CREATIVE_GRADIENT: {
                "style": BackgroundStyle.GRADIENT,
                "gradient_direction": GradientDirection.VERTICAL,
                "opacity": 0.98,
            },
            DesignTheme.MINIMALIST_LUXURY: {
                "style": BackgroundStyle.GRADIENT,
                "gradient_direction": GradientDirection.VERTICAL,
                "opacity": 0.98,
            },
            DesignTheme.TECH_INNOVATION: {
                "style": BackgroundStyle.GEOMETRIC,
                "geometric_complexity": 4,
                "opacity": 0.9,
            },
            DesignTheme.ADOBE_INSPIRED: {
                "style": BackgroundStyle.ABSTRACT,
                "opacity": 0.85,
            },
            DesignTheme.BEHANCE_STYLE: {
                "style": BackgroundStyle.ABSTRACT,
                "opacity": 0.85,
            },
        }
        
        base_config = theme_configs.get(theme, {})
        
        return BackgroundConfig(
            style=base_config.get("style", BackgroundStyle.GRADIENT),
            primary_color="#ffffff",
            secondary_color="#f8f9fa",
            opacity=base_config.get("opacity", 0.95),
            gradient_direction=base_config.get("gradient_direction", GradientDirection.DIAGONAL_DOWN),
            geometric_complexity=base_config.get("geometric_complexity", 3),
        )
    
    def _generate_from_config(self, config: BackgroundConfig) -> GeneratedBackground:
        """Generate background from configuration."""
        generators = {
            BackgroundStyle.SOLID: self._generate_solid,
            BackgroundStyle.GRADIENT: self._generate_gradient,
            BackgroundStyle.PATTERN: self._generate_pattern,
            BackgroundStyle.TEXTURE: self._generate_texture,
            BackgroundStyle.GEOMETRIC: self._generate_geometric,
            BackgroundStyle.ABSTRACT: self._generate_abstract,
            BackgroundStyle.PROFESSIONAL: self._generate_professional,
        }
        
        generator = generators.get(config.style, self._generate_solid)
        return generator(config)
    
    def _generate_solid(self, config: BackgroundConfig) -> GeneratedBackground:
        """Generate solid background."""
        css_properties = {
            "background-color": config.primary_color or "#ffffff",
            "opacity": str(config.opacity),
        }
        
        powerpoint_properties = {
            "fill_type": "solid",
            "color": config.primary_color or "#ffffff",
            "opacity": config.opacity,
        }
        
        return GeneratedBackground(
            config=config,
            css_properties=css_properties,
            powerpoint_properties=powerpoint_properties,
            description=f"Solid background in {config.primary_color}",
        )
    
    def _generate_gradient(self, config: BackgroundConfig) -> GeneratedBackground:
        """Generate gradient background."""
        direction_map = {
            GradientDirection.HORIZONTAL: "to right",
            GradientDirection.VERTICAL: "to bottom",
            GradientDirection.DIAGONAL_UP: "to top right",
            GradientDirection.DIAGONAL_DOWN: "to bottom right",
            GradientDirection.RADIAL: "radial-gradient",
        }
        
        direction = direction_map.get(
            config.gradient_direction or GradientDirection.DIAGONAL_DOWN, 
            "to bottom right"
        )
        
        primary = config.primary_color or "#ffffff"
        secondary = config.secondary_color or "#f0f0f0"
        
        gradient_dir = config.gradient_direction or GradientDirection.DIAGONAL_DOWN
        if gradient_dir == GradientDirection.RADIAL:
            gradient = f"radial-gradient(circle, {primary}, {secondary})"
        else:
            gradient = f"linear-gradient({direction}, {primary}, {secondary})"
        
        css_properties = {
            "background": gradient,
            "opacity": str(config.opacity),
        }
        
        powerpoint_properties = {
            "fill_type": "gradient",
            "gradient_type": gradient_dir.value,
            "color1": primary,
            "color2": secondary,
            "opacity": config.opacity,
        }
        
        return GeneratedBackground(
            config=config,
            css_properties=css_properties,
            powerpoint_properties=powerpoint_properties,
            description=f"Gradient background from {primary} to {secondary}",
        )
    
    def _generate_pattern(self, config: BackgroundConfig) -> GeneratedBackground:
        """Generate pattern background."""
        pattern_type = config.pattern_type or "dots"
        pattern_data = self._pattern_library.get(pattern_type, {})
        
        css_properties = {
            "background-color": config.primary_color or "#ffffff",
            "background-image": pattern_data.get("css_pattern", ""),
            "opacity": str(config.opacity),
        }
        
        powerpoint_properties = {
            "fill_type": "pattern",
            "pattern_type": pattern_type,
            "foreground_color": config.secondary_color or "#000000",
            "background_color": config.primary_color or "#ffffff",
            "opacity": config.opacity,
        }
        
        return GeneratedBackground(
            config=config,
            css_properties=css_properties,
            powerpoint_properties=powerpoint_properties,
            description=f"Pattern background with {pattern_type} pattern",
        )
    
    def _generate_texture(self, config: BackgroundConfig) -> GeneratedBackground:
        """Generate texture background."""
        texture_data = self._texture_library.get("paper", {})
        
        css_properties = {
            "background-color": config.primary_color or "#ffffff",
            "background-image": texture_data.get("css_texture", ""),
            "opacity": str(config.opacity),
        }
        
        powerpoint_properties = {
            "fill_type": "texture",
            "texture_type": "paper",
            "color": config.primary_color or "#ffffff",
            "opacity": config.opacity,
        }
        
        return GeneratedBackground(
            config=config,
            css_properties=css_properties,
            powerpoint_properties=powerpoint_properties,
            description="Textured background with paper texture",
        )
    
    def _generate_geometric(self, config: BackgroundConfig) -> GeneratedBackground:
        """Generate geometric background."""
        complexity = config.geometric_complexity
        geometric_data = self._geometric_library.get(f"complexity_{complexity}", {})
        
        css_properties = {
            "background-color": config.primary_color or "#ffffff",
            "background-image": geometric_data.get("css_pattern", ""),
            "opacity": str(config.opacity),
        }
        
        powerpoint_properties = {
            "fill_type": "geometric",
            "pattern_complexity": complexity,
            "primary_color": config.primary_color or "#ffffff",
            "accent_color": config.secondary_color or "#000000",
            "opacity": config.opacity,
        }
        
        return GeneratedBackground(
            config=config,
            css_properties=css_properties,
            powerpoint_properties=powerpoint_properties,
            description=f"Geometric background with complexity level {complexity}",
        )
    
    def _generate_abstract(self, config: BackgroundConfig) -> GeneratedBackground:
        """Generate abstract background."""
        # Create abstract pattern with random elements
        css_properties = {
            "background": f"linear-gradient(45deg, {config.primary_color or '#ffffff'}, {config.secondary_color or '#f0f0f0'})",
            "opacity": str(config.opacity),
        }
        
        powerpoint_properties = {
            "fill_type": "abstract",
            "style": "modern",
            "primary_color": config.primary_color or "#ffffff",
            "secondary_color": config.secondary_color or "#f0f0f0",
            "opacity": config.opacity,
        }
        
        return GeneratedBackground(
            config=config,
            css_properties=css_properties,
            powerpoint_properties=powerpoint_properties,
            description="Abstract artistic background",
        )
    
    def _generate_professional(self, config: BackgroundConfig) -> GeneratedBackground:
        """Generate professional background."""
        # Create clean, professional look
        css_properties = {
            "background": f"linear-gradient(to bottom, {config.primary_color or '#ffffff'}, {config.secondary_color or '#f8f9fa'})",
            "opacity": str(config.opacity),
        }
        
        powerpoint_properties = {
            "fill_type": "gradient",
            "gradient_type": "vertical",
            "color1": config.primary_color or "#ffffff",
            "color2": config.secondary_color or "#f8f9fa",
            "opacity": config.opacity,
        }
        
        return GeneratedBackground(
            config=config,
            css_properties=css_properties,
            powerpoint_properties=powerpoint_properties,
            description="Professional business background",
        )
    
    def _init_pattern_library(self) -> Dict[str, Dict[str, str]]:
        """Initialize pattern library."""
        return {
            "dots": {
                "css_pattern": "radial-gradient(circle, rgba(0,0,0,0.1) 1px, transparent 1px)",
                "description": "Polka dot pattern",
            },
            "lines": {
                "css_pattern": "linear-gradient(90deg, rgba(0,0,0,0.1) 1px, transparent 1px)",
                "description": "Vertical lines pattern",
            },
            "grid": {
                "css_pattern": "linear-gradient(rgba(0,0,0,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(0,0,0,0.1) 1px, transparent 1px)",
                "description": "Grid pattern",
            },
            "diagonal": {
                "css_pattern": "linear-gradient(45deg, rgba(0,0,0,0.1) 1px, transparent 1px)",
                "description": "Diagonal lines pattern",
            },
        }
    
    def _init_texture_library(self) -> Dict[str, Dict[str, str]]:
        """Initialize texture library."""
        return {
            "paper": {
                "css_texture": "url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGcgZmlsbD0ibm9uZSIgZmlsbC1ydWxlPSJldmVub2RkIj4KPGcgZmlsbD0iIzAwMDAwMCIgZmlsbC1vcGFjaXR5PSIwLjAzIj4KPHBhdGggZD0iTTM2IDM0djE2aDIwVjMwSDM2djRaTTAgMTRoMjBWMEgwdjE0em0yMCAwaDIwVjBIMjB2MTR6bTIwIDIwaDIwVjE0SDQwdjIwem0yMCAyMGgxNnYtMjBINjB2MjB6bTAgMjBoMTZ2LTIwSDYwdjIwem0yMC0yMGgxNlYxNEg4MHYyMHpNMCAwdjIwaDIwVjBIMHoiLz4KPC9nPgo8L2c+Cjwvc3ZnPgo=')",
                "description": "Paper texture",
            },
            "fabric": {
                "css_texture": "url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGcgZmlsbD0ibm9uZSIgZmlsbC1ydWxlPSJldmVub2RkIj4KPGcgZmlsbD0iIzAwMDAwMCIgZmlsbC1vcGFjaXR5PSIwLjAyIj4KPHBhdGggZD0iTTIwIDIwaDIwdjIwSDIwVjIwem0yMC0yMGgyMHYyMEg0MFYwem0wIDIwaDIwdjIwSDQwVjIwem0tMjAtMjBoMjB2MjBIMjBWMHoiLz4KPC9nPgo8L2c+Cjwvc3ZnPgo=')",
                "description": "Fabric texture",
            },
        }
    
    def _init_geometric_library(self) -> Dict[str, Dict[str, str]]:
        """Initialize geometric pattern library."""
        return {
            "complexity_1": {
                "css_pattern": "polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%)",
                "description": "Simple geometric shapes",
            },
            "complexity_2": {
                "css_pattern": "polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%)",
                "description": "Medium complexity geometric shapes",
            },
            "complexity_3": {
                "css_pattern": "polygon(50% 0%, 80% 10%, 100% 35%, 100% 70%, 80% 90%, 50% 100%, 20% 90%, 0% 70%, 0% 35%, 20% 10%)",
                "description": "High complexity geometric shapes",
            },
        }
    
    def get_background_suggestions(
        self,
        content_type: str,
        color_palette: Optional[ColorPalette] = None,
        count: int = 3,
    ) -> List[GeneratedBackground]:
        """
        Get multiple background suggestions for content.
        
        Args:
            content_type: Type of content
            color_palette: Color palette to use
            count: Number of suggestions to generate
            
        Returns:
            List[GeneratedBackground]: List of background suggestions
        """
        suggestions = []
        styles = list(BackgroundStyle)
        
        for i in range(min(count, len(styles))):
            style = styles[i % len(styles)]
            background = self.generate_background(
                content_type=content_type,
                color_palette=color_palette,
                style=style,
            )
            suggestions.append(background)
        
        return suggestions

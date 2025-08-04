"""
Enhanced visual engine with AI-generated imagery and advanced themes.

This module provides sophisticated visual enhancements including
AI-generated backgrounds, diagrams, and custom themes.
"""

from typing import Optional, List, Dict, Any
from pathlib import Path
import random

from .smartart_engine import SmartArtEngine
from ai.dalle3_client import DallE3Client
from core.config import FrameworkConfig
from design.themes import DesignTheme


class EnhancedVisualEngine:
    """
    Enhanced visual engine with AI-powered imagery and theming.
    
    Features:
    - AI-generated backgrounds and visuals
    - Dynamic theme generation
    - SmartArt integration
    - Custom color schemes
    - Context-aware visual elements
    """
    
    def __init__(self, config: Optional[FrameworkConfig] = None):
        """
        Initialize the enhanced visual engine.
        
        Args:
            config: Framework configuration
        """
        self.config = config or FrameworkConfig()
        self.smartart_engine = SmartArtEngine(None)  # SmartArt engine doesn't need config
        
        # Initialize DALL-E client if OpenAI API key is available
        self.dalle_client = None
        if self.config.openai_api_key:
            try:
                self.dalle_client = DallE3Client(config)
            except Exception as e:
                print(f"Warning: Could not initialize DALL-E client: {e}")
    
    def generate_theme_package(
        self,
        project_type: str,
        tech_stack: List[str],
        complexity: str,
        custom_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a complete theme package for the presentation.
        
        Args:
            project_type: Type of project
            tech_stack: List of technologies used
            complexity: Project complexity level
            custom_prompt: User's custom theme prompt
            
        Returns:
            Complete theme package with colors, backgrounds, and style
        """
        theme_package = {
            "primary_color": self._generate_primary_color(tech_stack),
            "accent_colors": self._generate_accent_colors(project_type),
            "background_style": self._determine_background_style(complexity),
            "typography": self._select_typography(project_type),
            "visual_style": self._determine_visual_style(custom_prompt or project_type)
        }
        
        # Generate AI backgrounds if DALL-E is available
        if self.dalle_client and self.config.enable_image_generation:
            theme_package["ai_backgrounds"] = self._generate_ai_backgrounds(
                project_type, tech_stack, theme_package["primary_color"]
            )
        
        return theme_package
    
    def create_architecture_visual(
        self,
        tech_stack: List[str],
        components: List[str],
        slide_theme: DesignTheme
    ) -> Optional[str]:
        """
        Create an architecture visualization.
        
        Args:
            tech_stack: List of technologies
            components: List of system components
            slide_theme: Theme for the slide
            
        Returns:
            Path to generated architecture visual
        """
        if self.dalle_client:
            return self.dalle_client.generate_architecture_diagram(
                tech_stack, components, self._theme_to_style(slide_theme)
            )
        else:
            # Fallback to simple text-based diagram
            return None  # Will be handled by presentation engine
    
    def create_roadmap_visual(
        self,
        milestones: List[str],
        timeline: str,
        slide_theme: DesignTheme
    ) -> Optional[str]:
        """
        Create a roadmap visualization.
        
        Args:
            milestones: List of milestones
            timeline: Timeline context
            slide_theme: Theme for the slide
            
        Returns:
            Path to generated roadmap visual
        """
        if self.dalle_client:
            return self.dalle_client.generate_roadmap_visual(
                milestones, timeline, self._theme_to_style(slide_theme)
            )
        else:
            # Fallback to simple text-based roadmap
            return None  # Will be handled by presentation engine
    
    def create_metrics_visual(
        self,
        metrics: Dict[str, Any],
        chart_type: str,
        slide_theme: DesignTheme
    ) -> Optional[str]:
        """
        Create a metrics visualization.
        
        Args:
            metrics: Metrics data
            chart_type: Type of chart
            slide_theme: Theme for the slide
            
        Returns:
            Path to generated metrics visual
        """
        if self.dalle_client:
            return self.dalle_client.generate_metrics_chart(
                metrics, chart_type, self._theme_to_style(slide_theme)
            )
        else:
            # Fallback to simple text-based metrics
            return None  # Will be handled by presentation engine
    
    def create_feature_icons(
        self,
        features: List[str],
        slide_theme: DesignTheme
    ) -> List[str]:
        """
        Create feature icons.
        
        Args:
            features: List of features
            slide_theme: Theme for the slide
            
        Returns:
            List of paths to generated feature icons
        """
        if self.dalle_client:
            return self.dalle_client.generate_feature_icons(
                features, self._theme_to_style(slide_theme)
            )
        else:
            # Fallback to simple text-based icons
            return []  # Will be handled by presentation engine
    
    def _generate_primary_color(self, tech_stack: List[str]) -> str:
        """Generate primary color based on technology stack."""
        # Tech-specific color mappings
        tech_colors = {
            "Python": "#3776AB",
            "JavaScript": "#F7DF1E",
            "TypeScript": "#007ACC",
            "React": "#61DAFB",
            "Vue": "#4FC08D",
            "Angular": "#DD0031",
            "Node.js": "#339933",
            "Django": "#092E20",
            "Flask": "#000000",
            "FastAPI": "#009688",
            "Docker": "#2496ED",
            "AWS": "#FF9900",
            "Azure": "#0078D4",
            "GCP": "#4285F4",
            "AI": "#8E44AD",
            "ML": "#E74C3C",
            "Data": "#2ECC71",
            "Web": "#3498DB",
            "Mobile": "#E67E22",
            "Desktop": "#9B59B6"
        }
        
        # Find matching colors
        for tech in tech_stack:
            if tech in tech_colors:
                return tech_colors[tech]
        
        # Default professional colors
        defaults = ["#2C3E50", "#34495E", "#7F8C8D", "#95A5A6", "#BDC3C7"]
        return random.choice(defaults)
    
    def _generate_accent_colors(self, project_type: str) -> List[str]:
        """Generate accent colors based on project type."""
        accent_schemes = {
            "AI": ["#8E44AD", "#9B59B6", "#AF7AC5"],
            "Web": ["#3498DB", "#5DADE2", "#85C1E9"],
            "Mobile": ["#E67E22", "#F39C12", "#F8C471"],
            "Data": ["#2ECC71", "#58D68D", "#82E0AA"],
            "Enterprise": ["#34495E", "#5D6D7E", "#85929E"],
            "Startup": ["#E74C3C", "#EC7063", "#F1948A"]
        }
        
        for key in accent_schemes:
            if key.lower() in project_type.lower():
                return accent_schemes[key]
        
        return ["#3498DB", "#E74C3C", "#2ECC71"]  # Default
    
    def _determine_background_style(self, complexity: str) -> str:
        """Determine background style based on complexity."""
        if complexity.lower() in ["simple", "basic"]:
            return "clean_minimal"
        elif complexity.lower() in ["complex", "advanced"]:
            return "sophisticated_gradient"
        else:
            return "professional_subtle"
    
    def _select_typography(self, project_type: str) -> Dict[str, str]:
        """Select typography based on project type."""
        typography_schemes = {
            "AI": {"heading": "Segoe UI", "body": "Calibri", "accent": "Consolas"},
            "Web": {"heading": "Arial", "body": "Segoe UI", "accent": "Courier New"},
            "Enterprise": {"heading": "Times New Roman", "body": "Arial", "accent": "Georgia"},
            "Startup": {"heading": "Helvetica", "body": "Open Sans", "accent": "Roboto"}
        }
        
        for key in typography_schemes:
            if key.lower() in project_type.lower():
                return typography_schemes[key]
        
        return {"heading": "Calibri", "body": "Arial", "accent": "Segoe UI"}
    
    def _determine_visual_style(self, context: str) -> str:
        """Determine visual style based on context."""
        if "modern" in context.lower() or "tech" in context.lower():
            return "modern_tech"
        elif "corporate" in context.lower() or "business" in context.lower():
            return "corporate_professional"
        elif "creative" in context.lower() or "design" in context.lower():
            return "creative_dynamic"
        else:
            return "balanced_professional"
    
    def _generate_ai_backgrounds(
        self,
        project_type: str,
        tech_stack: List[str],
        primary_color: str
    ) -> List[str]:
        """Generate AI backgrounds for different slide types."""
        backgrounds = []
        
        if self.dalle_client:
            # Generate different backgrounds for different slide types
            slide_types = [
                ("title", "corporate_modern"),
                ("content", "professional_subtle"),
                ("architecture", "tech_focused"),
                ("metrics", "data_visualization")
            ]
            
            for slide_type, style in slide_types:
                bg_path = self.dalle_client.generate_background(
                    f"{project_type} {slide_type}",
                    project_type,
                    primary_color,
                    style
                )
                if bg_path:
                    backgrounds.append(bg_path)
        
        return backgrounds
    
    def _theme_to_style(self, theme: DesignTheme) -> str:
        """Convert DesignTheme to style string."""
        style_mapping = {
            DesignTheme.CORPORATE_MODERN: "corporate_modern",
            DesignTheme.TECH_INNOVATION: "tech_innovation",
            DesignTheme.CREATIVE_GRADIENT: "creative_gradient",
            DesignTheme.MINIMALIST_LUXURY: "minimalist_luxury"
        }
        
        return style_mapping.get(theme, "professional")
    
    def cleanup(self):
        """Clean up temporary resources."""
        if self.dalle_client:
            self.dalle_client.cleanup_images()

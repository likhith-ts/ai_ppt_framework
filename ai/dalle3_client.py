"""
OpenAI DALL-E 3 client for AI PowerPoint Framework.

This module provides integration with OpenAI's DALL-E 3 for generating
custom images, backgrounds, and visual elements for presentations.
"""

import os
import requests
import base64
from typing import Optional, Dict, Any, List
from pathlib import Path
import tempfile

from core.config import FrameworkConfig
from core.exceptions import AIClientError


class DallE3Client:
    """
    OpenAI DALL-E 3 client for generating presentation visuals.
    
    Features:
    - Custom background generation
    - Icon and diagram creation
    - Theme-based visual elements
    - Architecture diagrams
    - Infographic elements
    """
    
    def __init__(self, config: Optional[FrameworkConfig] = None):
        """
        Initialize the DALL-E 3 client.
        
        Args:
            config: Configuration instance
        """
        self.config = config or FrameworkConfig()
        self.api_key = self.config.openai_api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1"
        
        if not self.api_key:
            raise AIClientError("OpenAI API key not configured")
    
    def generate_background(
        self,
        theme: str,
        project_type: str,
        color_scheme: str = "professional",
        style: str = "minimalist"
    ) -> Optional[str]:
        """
        Generate a custom background for the presentation.
        
        Args:
            theme: Main theme of the presentation
            project_type: Type of project (e.g., "AI Web Application")
            color_scheme: Color scheme preference
            style: Visual style preference
            
        Returns:
            Path to generated background image
        """
        prompt = f"""
        Create a professional presentation background for a {project_type} project.
        Style: {style}, modern, clean, corporate
        Color scheme: {color_scheme} colors with subtle gradients
        Theme: {theme}
        
        Requirements:
        - Subtle geometric patterns or tech-inspired elements
        - Not distracting from text content
        - Professional business presentation style
        - Resolution suitable for PowerPoint backgrounds
        - Minimal visual noise, emphasis on elegance
        """
        
        return self._generate_image(prompt, "background")
    
    def generate_architecture_diagram(
        self,
        tech_stack: List[str],
        components: List[str],
        style: str = "modern"
    ) -> Optional[str]:
        """
        Generate an architecture diagram.
        
        Args:
            tech_stack: List of technologies used
            components: List of system components
            style: Visual style for the diagram
            
        Returns:
            Path to generated diagram image
        """
        tech_list = ", ".join(tech_stack[:5])  # Limit to 5 main technologies
        components_list = ", ".join(components[:8])  # Limit to 8 components
        
        prompt = f"""
        Create a professional system architecture diagram showing:
        Technologies: {tech_list}
        Components: {components_list}
        
        Style: {style}, clean, minimal, tech-focused
        Format: Boxes, arrows, clear labels
        Color scheme: Professional blues and grays
        Layout: Hierarchical or layered architecture view
        
        Requirements:
        - Clear component relationships
        - Professional technical diagram style
        - Suitable for business presentations
        - Clean typography and spacing
        """
        
        return self._generate_image(prompt, "architecture")
    
    def generate_roadmap_visual(
        self,
        milestones: List[str],
        timeline: str = "future",
        style: str = "timeline"
    ) -> Optional[str]:
        """
        Generate a roadmap visualization.
        
        Args:
            milestones: List of roadmap milestones
            timeline: Timeline context
            style: Visual style for the roadmap
            
        Returns:
            Path to generated roadmap image
        """
        milestones_text = ", ".join(milestones[:6])  # Limit to 6 milestones
        
        prompt = f"""
        Create a professional project roadmap visualization showing:
        Milestones: {milestones_text}
        Timeline: {timeline} development phases
        
        Style: {style}, modern, professional
        Format: Timeline with clear phases and milestones
        Color scheme: Progressive colors from current to future
        Layout: Horizontal timeline or vertical progression
        
        Requirements:
        - Clear milestone markers
        - Professional business style
        - Suitable for executive presentations
        - Clean and organized layout
        """
        
        return self._generate_image(prompt, "roadmap")
    
    def generate_metrics_chart(
        self,
        metrics: Dict[str, Any],
        chart_type: str = "mixed",
        style: str = "corporate"
    ) -> Optional[str]:
        """
        Generate a metrics visualization.
        
        Args:
            metrics: Dictionary of metrics to visualize
            chart_type: Type of chart (bar, pie, mixed)
            style: Visual style for the chart
            
        Returns:
            Path to generated chart image
        """
        metrics_summary = ", ".join([f"{k}: {v}" for k, v in list(metrics.items())[:5]])
        
        prompt = f"""
        Create a professional metrics dashboard showing:
        Data: {metrics_summary}
        Chart type: {chart_type} charts and visualizations
        
        Style: {style}, clean, data-focused
        Format: Professional dashboard with multiple metrics
        Color scheme: Corporate colors with data visualization best practices
        Layout: Grid or organized dashboard layout
        
        Requirements:
        - Clear data representation
        - Professional business intelligence style
        - Suitable for executive dashboards
        - Clean typography and clear labels
        """
        
        return self._generate_image(prompt, "metrics")
    
    def generate_feature_icons(
        self,
        features: List[str],
        style: str = "modern",
        color_scheme: str = "monochrome"
    ) -> List[str]:
        """
        Generate icons for features.
        
        Args:
            features: List of features to create icons for
            style: Visual style for icons
            color_scheme: Color scheme for icons
            
        Returns:
            List of paths to generated icon images
        """
        icons = []
        
        for feature in features[:4]:  # Limit to 4 features
            prompt = f"""
            Create a professional icon representing: {feature}
            
            Style: {style}, minimalist, tech-focused
            Color scheme: {color_scheme} with professional accent colors
            Format: Clean icon design suitable for presentations
            Background: Transparent or subtle
            
            Requirements:
            - Simple, recognizable symbol
            - Professional business style
            - Scalable icon design
            - Clear visual metaphor for the feature
            """
            
            icon_path = self._generate_image(prompt, f"icon_{feature.replace(' ', '_').lower()}")
            if icon_path:
                icons.append(icon_path)
        
        return icons
    
    def _generate_image(self, prompt: str, category: str) -> Optional[str]:
        """
        Generate an image using DALL-E 3.
        
        Args:
            prompt: Image generation prompt
            category: Category for file naming
            
        Returns:
            Path to generated image file
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "dall-e-3",
                "prompt": prompt,
                "n": 1,
                "size": "1024x1024",
                "quality": "standard",
                "style": "natural"
            }
            
            response = requests.post(
                f"{self.base_url}/images/generations",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                image_url = result["data"][0]["url"]
                
                # Download the image
                img_response = requests.get(image_url, timeout=30)
                if img_response.status_code == 200:
                    # Save to temporary file
                    temp_dir = Path(tempfile.gettempdir()) / "ai_ppt_images"
                    temp_dir.mkdir(exist_ok=True)
                    
                    image_path = temp_dir / f"{category}_{hash(prompt) % 10000}.png"
                    image_path.write_bytes(img_response.content)
                    
                    return str(image_path)
            
            return None
            
        except Exception as e:
            print(f"Error generating image: {e}")
            return None
    
    def cleanup_images(self):
        """Clean up temporary images."""
        temp_dir = Path(tempfile.gettempdir()) / "ai_ppt_images"
        if temp_dir.exists():
            for file in temp_dir.glob("*.png"):
                try:
                    file.unlink()
                except:
                    pass

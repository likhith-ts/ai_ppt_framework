"""
Enhanced Layout and Positioning System for AI PowerPoint Framework.

This module addresses the critical visual quality issues identified:
1. Layout & Alignment Problems
2. Background Image Issues  
3. Image Positioning & Z-Index
4. Content Overflow & Text Issues

The system provides precise positioning, proper alignment, and professional layouts.
"""

from typing import Tuple, Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import tempfile
from pathlib import Path

# Standard slide dimensions (16:9 aspect ratio)
SLIDE_WIDTH = 13.33  # inches  
SLIDE_HEIGHT = 7.5   # inches
SLIDE_WIDTH_PX = 1920  # pixels
SLIDE_HEIGHT_PX = 1080  # pixels

# Safe zones and margins
MARGIN_TOP = 0.5     # inches
MARGIN_BOTTOM = 0.5  # inches  
MARGIN_LEFT = 0.5    # inches
MARGIN_RIGHT = 0.5   # inches


class LayoutType(Enum):
    """Standard slide layout types"""
    TITLE_SLIDE = "title_slide"
    TITLE_CONTENT = "title_content"
    TWO_COLUMN = "two_column"
    IMAGE_TEXT = "image_text"
    CONTENT_ONLY = "content_only"
    DIAGRAM_FOCUS = "diagram_focus"
    FULL_IMAGE = "full_image"


class AlignmentType(Enum):
    """Element alignment options"""
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    JUSTIFY = "justify"
    TOP = "top"
    MIDDLE = "middle"
    BOTTOM = "bottom"


@dataclass
class Position:
    """Precise positioning for slide elements"""
    x: float  # inches from left
    y: float  # inches from top
    width: float  # inches
    height: float  # inches
    z_index: int = 0  # layering order


@dataclass
class LayoutRegion:
    """Defines a region within a slide layout"""
    name: str
    position: Position
    alignment: AlignmentType
    max_text_length: Optional[int] = None
    font_size_range: Tuple[int, int] = (12, 24)


class LayoutEngine:
    """
    Professional layout engine for consistent, aligned slide designs.
    
    Features:
    - Grid-based positioning system
    - Safe zones and margin enforcement
    - Dynamic element sizing
    - Z-index management
    - Text overflow prevention
    """
    
    def __init__(self):
        self.layouts = self._initialize_layouts()
        
    def _initialize_layouts(self) -> Dict[LayoutType, List[LayoutRegion]]:
        """Initialize standard layout templates"""
        layouts = {}
        
        # Title Slide Layout
        layouts[LayoutType.TITLE_SLIDE] = [
            LayoutRegion(
                name="title",
                position=Position(
                    x=MARGIN_LEFT,
                    y=2.0,
                    width=SLIDE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT,
                    height=1.5,
                    z_index=10
                ),
                alignment=AlignmentType.CENTER,
                font_size_range=(36, 48)
            ),
            LayoutRegion(
                name="subtitle", 
                position=Position(
                    x=MARGIN_LEFT,
                    y=4.0,
                    width=SLIDE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT,
                    height=1.0,
                    z_index=10
                ),
                alignment=AlignmentType.CENTER,
                font_size_range=(18, 24)
            )
        ]
        
        # Title + Content Layout
        layouts[LayoutType.TITLE_CONTENT] = [
            LayoutRegion(
                name="title",
                position=Position(
                    x=MARGIN_LEFT,
                    y=MARGIN_TOP,
                    width=SLIDE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT,
                    height=1.0,
                    z_index=10
                ),
                alignment=AlignmentType.LEFT,
                font_size_range=(24, 32)
            ),
            LayoutRegion(
                name="content",
                position=Position(
                    x=MARGIN_LEFT,
                    y=MARGIN_TOP + 1.2,
                    width=SLIDE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT,
                    height=SLIDE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM - 1.2,
                    z_index=5
                ),
                alignment=AlignmentType.LEFT,
                max_text_length=500,  # Prevent overflow
                font_size_range=(14, 18)
            )
        ]
        
        # Two Column Layout
        layouts[LayoutType.TWO_COLUMN] = [
            LayoutRegion(
                name="title",
                position=Position(
                    x=MARGIN_LEFT,
                    y=MARGIN_TOP,
                    width=SLIDE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT,
                    height=1.0,
                    z_index=10
                ),
                alignment=AlignmentType.LEFT,
                font_size_range=(24, 32)
            ),
            LayoutRegion(
                name="left_content",
                position=Position(
                    x=MARGIN_LEFT,
                    y=MARGIN_TOP + 1.2,
                    width=(SLIDE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT - 0.2) / 2,
                    height=SLIDE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM - 1.2,
                    z_index=5
                ),
                alignment=AlignmentType.LEFT,
                max_text_length=250,
                font_size_range=(12, 16)
            ),
            LayoutRegion(
                name="right_content",
                position=Position(
                    x=MARGIN_LEFT + (SLIDE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT) / 2 + 0.1,
                    y=MARGIN_TOP + 1.2,
                    width=(SLIDE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT - 0.2) / 2,
                    height=SLIDE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM - 1.2,
                    z_index=5
                ),
                alignment=AlignmentType.LEFT,
                max_text_length=250,
                font_size_range=(12, 16)
            )
        ]
        
        # Image + Text Layout
        layouts[LayoutType.IMAGE_TEXT] = [
            LayoutRegion(
                name="title",
                position=Position(
                    x=MARGIN_LEFT,
                    y=MARGIN_TOP,
                    width=SLIDE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT,
                    height=1.0,
                    z_index=10
                ),
                alignment=AlignmentType.LEFT,
                font_size_range=(24, 32)
            ),
            LayoutRegion(
                name="image",
                position=Position(
                    x=MARGIN_LEFT,
                    y=MARGIN_TOP + 1.2,
                    width=(SLIDE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT) * 0.6,
                    height=SLIDE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM - 1.2,
                    z_index=3
                ),
                alignment=AlignmentType.CENTER
            ),
            LayoutRegion(
                name="text_content",
                position=Position(
                    x=MARGIN_LEFT + (SLIDE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT) * 0.65,
                    y=MARGIN_TOP + 1.2,
                    width=(SLIDE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT) * 0.35 - 0.1,
                    height=SLIDE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM - 1.2,
                    z_index=5
                ),
                alignment=AlignmentType.LEFT,
                max_text_length=300,
                font_size_range=(12, 16)
            )
        ]
        
        # Diagram Focus Layout
        layouts[LayoutType.DIAGRAM_FOCUS] = [
            LayoutRegion(
                name="title",
                position=Position(
                    x=MARGIN_LEFT,
                    y=MARGIN_TOP,
                    width=SLIDE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT,
                    height=0.8,
                    z_index=10
                ),
                alignment=AlignmentType.CENTER,
                font_size_range=(20, 28)
            ),
            LayoutRegion(
                name="diagram",
                position=Position(
                    x=MARGIN_LEFT + 1.0,
                    y=MARGIN_TOP + 1.0,
                    width=SLIDE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT - 2.0,
                    height=SLIDE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM - 2.0,
                    z_index=3
                ),
                alignment=AlignmentType.CENTER
            ),
            LayoutRegion(
                name="caption",
                position=Position(
                    x=MARGIN_LEFT,
                    y=SLIDE_HEIGHT - MARGIN_BOTTOM - 0.6,
                    width=SLIDE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT,
                    height=0.5,
                    z_index=5
                ),
                alignment=AlignmentType.CENTER,
                max_text_length=100,
                font_size_range=(10, 14)
            )
        ]
        
        return layouts
    
    def get_layout(self, layout_type: LayoutType) -> List[LayoutRegion]:
        """Get layout regions for specified layout type"""
        return self.layouts.get(layout_type, self.layouts[LayoutType.TITLE_CONTENT])
    
    def calculate_optimal_layout(self, content_type: str, has_image: bool = False, 
                               has_diagram: bool = False) -> LayoutType:
        """
        Automatically select optimal layout based on content characteristics
        
        Args:
            content_type: Type of slide content
            has_image: Whether slide includes images
            has_diagram: Whether slide includes diagrams
            
        Returns:
            Optimal layout type for the content
        """
        if content_type == "title_slide":
            return LayoutType.TITLE_SLIDE
        elif has_diagram:
            return LayoutType.DIAGRAM_FOCUS
        elif has_image:
            return LayoutType.IMAGE_TEXT
        elif content_type in ["features", "comparison"]:
            return LayoutType.TWO_COLUMN
        else:
            return LayoutType.TITLE_CONTENT
    
    def validate_text_length(self, text: str, region: LayoutRegion) -> Tuple[str, bool]:
        """
        Validate and truncate text to prevent overflow
        
        Args:
            text: Text content to validate
            region: Layout region for the text
            
        Returns:
            Tuple of (processed_text, was_truncated)
        """
        if region.max_text_length is None:
            return text, False
            
        if len(text) <= region.max_text_length:
            return text, False
            
        # Smart truncation - try to break at sentence or word boundaries
        if len(text) > region.max_text_length:
            truncated = text[:region.max_text_length - 3]
            
            # Try to break at sentence boundary
            last_period = truncated.rfind('.')
            if last_period > region.max_text_length * 0.7:
                return truncated[:last_period + 1], True
            
            # Try to break at word boundary
            last_space = truncated.rfind(' ')
            if last_space > region.max_text_length * 0.8:
                return truncated[:last_space] + "...", True
            
            return truncated + "...", True
        
        return text, False
    
    def optimize_bullet_points(self, points: List[str], max_points: int = 4) -> List[str]:
        """
        Optimize bullet points for better readability
        
        Args:
            points: List of bullet points
            max_points: Maximum number of points to keep
            
        Returns:
            Optimized list of bullet points
        """
        if len(points) <= max_points:
            return points
        
        # Prioritize shorter, more impactful points
        scored_points = []
        for point in points:
            # Score based on length (shorter is better) and content quality
            length_score = max(0, 100 - len(point))  # Prefer shorter points
            keyword_score = 0
            
            # Boost points with important keywords
            important_keywords = ['key', 'important', 'critical', 'main', 'primary']
            for keyword in important_keywords:
                if keyword in point.lower():
                    keyword_score += 10
            
            total_score = length_score + keyword_score
            scored_points.append((point, total_score))
        
        # Sort by score and take top points
        scored_points.sort(key=lambda x: x[1], reverse=True)
        return [point for point, score in scored_points[:max_points]]
    
    def calculate_font_size(self, text: str, region: LayoutRegion) -> int:
        """
        Calculate optimal font size based on text length and region size
        
        Args:
            text: Text content
            region: Layout region
            
        Returns:
            Optimal font size
        """
        min_size, max_size = region.font_size_range
        
        # Base size on text length
        if len(text) < 50:
            return max_size
        elif len(text) < 150:
            return int(min_size + (max_size - min_size) * 0.7)
        elif len(text) < 300:
            return int(min_size + (max_size - min_size) * 0.4)
        else:
            return min_size


class BackgroundManager:
    """
    Manages slide backgrounds to ensure proper coverage and professional appearance.
    
    Addresses the issue where backgrounds appear as overlaid images instead of true backgrounds.
    """
    
    def __init__(self):
        self.temp_dir = Path(tempfile.gettempdir()) / "ai_ppt_backgrounds"
        self.temp_dir.mkdir(exist_ok=True)
    
    def prepare_background_image(self, image_path: str, slide_width: int = SLIDE_WIDTH_PX, 
                                slide_height: int = SLIDE_HEIGHT_PX) -> str:
        """
        Prepare and resize background image to properly cover slide
        
        Args:
            image_path: Path to original image
            slide_width: Target slide width in pixels
            slide_height: Target slide height in pixels
            
        Returns:
            Path to processed background image
        """
        try:
            from PIL import Image
            
            # Open and process image
            img = Image.open(image_path)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Calculate aspect ratios
            img_ratio = img.width / img.height
            slide_ratio = slide_width / slide_height
            
            if img_ratio > slide_ratio:
                # Image is wider - scale by height and crop width
                new_height = slide_height
                new_width = int(new_height * img_ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Center crop
                left = (new_width - slide_width) // 2
                img = img.crop((left, 0, left + slide_width, slide_height))
            else:
                # Image is taller - scale by width and crop height
                new_width = slide_width
                new_height = int(new_width / img_ratio)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Center crop
                top = (new_height - slide_height) // 2
                img = img.crop((0, top, slide_width, top + slide_height))
            
            # Ensure exact dimensions
            img = img.resize((slide_width, slide_height), Image.Resampling.LANCZOS)
            
            # Save processed image
            output_path = self.temp_dir / f"bg_{Path(image_path).stem}_processed.png"
            img.save(output_path, "PNG", quality=95)
            
            return str(output_path)
            
        except Exception as e:
            print(f"Warning: Could not process background image: {e}")
            return image_path
    
    def create_gradient_background(self, color1: str, color2: str, 
                                 slide_width: int = SLIDE_WIDTH_PX,
                                 slide_height: int = SLIDE_HEIGHT_PX) -> str:
        """
        Create a gradient background image
        
        Args:
            color1: Start color (hex format)
            color2: End color (hex format)
            slide_width: Width in pixels
            slide_height: Height in pixels
            
        Returns:
            Path to generated gradient background
        """
        try:
            from PIL import Image, ImageDraw
            
            # Create gradient
            img = Image.new('RGB', (slide_width, slide_height))
            draw = ImageDraw.Draw(img)
            
            # Convert hex colors to RGB
            def hex_to_rgb(hex_color):
                hex_color = hex_color.lstrip('#')
                return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            
            rgb1 = hex_to_rgb(color1)
            rgb2 = hex_to_rgb(color2)
            
            # Create vertical gradient
            for y in range(slide_height):
                ratio = y / slide_height
                r = int(rgb1[0] * (1 - ratio) + rgb2[0] * ratio)
                g = int(rgb1[1] * (1 - ratio) + rgb2[1] * ratio)
                b = int(rgb1[2] * (1 - ratio) + rgb2[2] * ratio)
                
                draw.line([(0, y), (slide_width, y)], fill=(r, g, b))
            
            # Save gradient
            output_path = self.temp_dir / f"gradient_{color1[1:]}_{color2[1:]}.png"
            img.save(output_path, "PNG")
            
            return str(output_path)
            
        except Exception as e:
            print(f"Warning: Could not create gradient background: {e}")
            return ""


# Global instances
layout_engine = LayoutEngine()
background_manager = BackgroundManager()

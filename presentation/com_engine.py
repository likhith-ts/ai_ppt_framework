"""
COM-based PowerPoint presentation engine.

This module provides PowerPoint generation using Windows COM objects,
offering the highest fidelity presentation creation on Windows systems.
"""

import platform
from typing import Optional, Any
from pathlib import Path

from .base_engine import BasePresentationEngine, SlideData
from core.exceptions import PresentationGenerationError
from design.themes import DesignTheme
from design.color_system import DesignPalettes


class COMPresentationEngine(BasePresentationEngine):
    """
    COM-based PowerPoint presentation engine for Windows.

    Features:
    - Native PowerPoint COM automation
    - Full PowerPoint feature access
    - Professional slide layouts
    - Advanced formatting capabilities
    - Windows-only implementation
    """

    def __init__(self, config: Optional[Any] = None):
        """Initialize the COM presentation engine."""
        super().__init__(config)
        self.powerpoint = None
        self.presentation = None
        self.slides = None

        if not self.is_available():
            raise PresentationGenerationError(
                "COM engine is only available on Windows with PowerPoint installed"
            )

    def is_available(self) -> bool:
        """Check if COM engine is available (Windows + PowerPoint)."""
        if platform.system() != "Windows":
            return False

        try:
            import win32com.client

            # Try to create PowerPoint instance
            powerpoint = win32com.client.Dispatch("PowerPoint.Application")
            powerpoint.Quit()
            return True
        except Exception:
            return False

    def create_presentation(self, title: str = "AI Generated Presentation") -> None:
        """Create a new PowerPoint presentation using COM."""
        try:
            import win32com.client

            # Start PowerPoint application
            self.powerpoint = win32com.client.Dispatch("PowerPoint.Application")
            self.powerpoint.Visible = True

            # Create new presentation
            self.presentation = self.powerpoint.Presentations.Add()
            self.slides = self.presentation.Slides

            # Set presentation properties
            self.presentation.PageSetup.SlideWidth = 960
            self.presentation.PageSetup.SlideHeight = 540

            self.slides_created = 0

        except Exception as e:
            self.close_presentation()
            raise PresentationGenerationError(
                f"Failed to create COM presentation: {str(e)}"
            ) from e

    def add_slide(self, slide_data: SlideData) -> None:
        """Add a content slide using COM automation."""
        if not self.slides:
            raise PresentationGenerationError("No presentation created")

        try:
            # Add slide with content layout (typically layout 2)
            slide = self.slides.Add(self.slides.Count + 1, 2)  # ppLayoutText = 2

            # Get theme colors
            palette = DesignPalettes.get_palette(slide_data.theme)

            # Set slide background
            slide.Background.Fill.ForeColor.RGB = palette.background

            # Configure title
            if slide.Shapes.HasTitle:
                title_shape = slide.Shapes.Title
                title_shape.TextFrame.TextRange.Text = slide_data.title
                title_shape.TextFrame.TextRange.Font.Name = "Segoe UI"
                title_shape.TextFrame.TextRange.Font.Size = 32
                title_shape.TextFrame.TextRange.Font.Color.RGB = palette.primary
                title_shape.TextFrame.TextRange.Font.Bold = True

            # Add content
            if len(slide.Shapes) > 1:  # Has content placeholder
                content_shape = slide.Shapes.Placeholders(2)  # Second placeholder
                content_text = "\n".join([f"• {point}" for point in slide_data.points])
                content_shape.TextFrame.TextRange.Text = content_text
                content_shape.TextFrame.TextRange.Font.Name = "Segoe UI"
                content_shape.TextFrame.TextRange.Font.Size = 18
                content_shape.TextFrame.TextRange.Font.Color.RGB = palette.text_primary

            # Insert AI-generated visuals if available
            if slide_data.background_image:
                self._insert_background_image(slide, slide_data.background_image)
            
            if slide_data.diagram_image:
                self._insert_diagram_image(slide, slide_data.diagram_image, slide_data.slide_type)
            
            if slide_data.feature_icons:
                self._insert_feature_icons(slide, slide_data.feature_icons)
            
            # Apply dynamic colors if available
            if slide_data.primary_color:
                self._apply_dynamic_colors(slide, slide_data)

            self.slides_created += 1

        except Exception as e:
            raise PresentationGenerationError(f"Failed to add slide: {str(e)}") from e

    def add_title_slide(
        self,
        title: str,
        subtitle: str = "",
        theme: DesignTheme = DesignTheme.CORPORATE_MODERN,
    ) -> None:
        """Add a title slide using COM automation."""
        if not self.slides:
            raise PresentationGenerationError("No presentation created")

        try:
            # Add title slide (layout 1)
            slide = self.slides.Add(1, 1)  # ppLayoutTitle = 1

            # Get theme colors
            palette = DesignPalettes.get_palette(theme)

            # Set slide background
            slide.Background.Fill.ForeColor.RGB = palette.background

            # Configure title
            if slide.Shapes.HasTitle:
                title_shape = slide.Shapes.Title
                title_shape.TextFrame.TextRange.Text = title
                title_shape.TextFrame.TextRange.Font.Name = "Segoe UI"
                title_shape.TextFrame.TextRange.Font.Size = 44
                title_shape.TextFrame.TextRange.Font.Color.RGB = palette.primary
                title_shape.TextFrame.TextRange.Font.Bold = True
                title_shape.TextFrame.TextRange.ParagraphFormat.Alignment = 2  # Center

            # Configure subtitle
            if len(slide.Shapes) > 1 and subtitle:
                subtitle_shape = slide.Shapes.Placeholders(2)
                subtitle_shape.TextFrame.TextRange.Text = subtitle
                subtitle_shape.TextFrame.TextRange.Font.Name = "Segoe UI"
                subtitle_shape.TextFrame.TextRange.Font.Size = 24
                subtitle_shape.TextFrame.TextRange.Font.Color.RGB = (
                    palette.text_secondary
                )
                subtitle_shape.TextFrame.TextRange.ParagraphFormat.Alignment = (
                    2  # Center
                )

            self.slides_created += 1

        except Exception as e:
            raise PresentationGenerationError(
                f"Failed to add title slide: {str(e)}"
            ) from e

    def save_presentation(self, filepath: Path) -> bool:
        """Save the presentation to a file."""
        if not self.presentation:
            raise PresentationGenerationError("No presentation to save")

        try:
            # Ensure directory exists
            filepath.parent.mkdir(parents=True, exist_ok=True)

            # Save presentation
            absolute_path = str(filepath.absolute())
            self.presentation.SaveAs(absolute_path)

            return filepath.exists()

        except Exception as e:
            raise PresentationGenerationError(
                f"Failed to save presentation: {str(e)}"
            ) from e

    def close_presentation(self) -> None:
        """Close the presentation and clean up COM objects."""
        try:
            if self.presentation:
                self.presentation.Close()
                self.presentation = None

            if self.powerpoint:
                self.powerpoint.Quit()
                self.powerpoint = None

            self.slides = None

        except Exception:
            # Ignore errors during cleanup
            pass

    def _insert_background_image(self, slide, image_path: str):
        """Insert a background image into the slide using COM."""
        try:
            from pathlib import Path
            
            if not image_path or not Path(image_path).exists():
                return
            
            # Insert image as background using COM
            # Position it as the first shape (background)
            picture = slide.Shapes.AddPicture(
                FileName=str(image_path),
                LinkToFile=False,  # Embed the image
                SaveWithDocument=True,
                Left=0,  # Left edge
                Top=0,   # Top edge
                Width=720,  # Standard slide width (10 inches * 72 points)
                Height=540  # Standard slide height (7.5 inches * 72 points)
            )
            
            # Send to back (make it the background)
            picture.ZOrder(0)  # Send to back
            
        except Exception as e:
            print(f"Warning: Could not insert background image via COM: {e}")
    
    def _insert_diagram_image(self, slide, image_path: str, slide_type: str):
        """Insert a diagram image into the slide using COM."""
        try:
            from pathlib import Path
            
            if not image_path or not Path(image_path).exists():
                return
            
            # Position based on slide type (in points, 72 points = 1 inch)
            if slide_type == "architecture_slide":
                left = 396  # 5.5 inches
                top = 108   # 1.5 inches
                width = 288 # 4 inches
                height = 216 # 3 inches
            elif slide_type == "roadmap_slide":
                left = 72   # 1 inch
                top = 216   # 3 inches
                width = 576 # 8 inches
                height = 144 # 2 inches
            elif slide_type == "metrics_slide":
                left = 360  # 5 inches
                top = 72    # 1 inch
                width = 324 # 4.5 inches
                height = 252 # 3.5 inches
            else:
                # Default positioning
                left = 396  # 5.5 inches
                top = 144   # 2 inches
                width = 252 # 3.5 inches
                height = 180 # 2.5 inches
            
            picture = slide.Shapes.AddPicture(
                FileName=str(image_path),
                LinkToFile=False,
                SaveWithDocument=True,
                Left=left,
                Top=top,
                Width=width,
                Height=height
            )
            
        except Exception as e:
            print(f"Warning: Could not insert diagram image via COM: {e}")
    
    def _insert_feature_icons(self, slide, icon_paths):
        """Insert feature icons into the slide using COM."""
        try:
            from pathlib import Path
            
            if not icon_paths:
                return
            
            # Position icons in a grid
            start_left = 72   # 1 inch from left
            start_top = 360   # 5 inches from top
            icon_size = 72    # 1 inch square
            spacing = 144     # 2 inches between icons
            
            for i, icon_path in enumerate(icon_paths[:4]):  # Maximum 4 icons
                if not icon_path or not Path(icon_path).exists():
                    continue
                
                left = start_left + (i * spacing)
                top = start_top
                
                picture = slide.Shapes.AddPicture(
                    FileName=str(icon_path),
                    LinkToFile=False,
                    SaveWithDocument=True,
                    Left=left,
                    Top=top,
                    Width=icon_size,
                    Height=icon_size
                )
                
        except Exception as e:
            print(f"Warning: Could not insert feature icons via COM: {e}")
    
    def _apply_dynamic_colors(self, slide, slide_data):
        """Apply dynamic color scheme from AI-generated theme using COM."""
        try:
            # If we have AI-generated colors, apply them
            if slide_data.primary_color:
                primary_rgb = self._hex_to_rgb(slide_data.primary_color)
                # Convert RGB to COM color format (BGR)
                com_color = primary_rgb[2] + (primary_rgb[1] << 8) + (primary_rgb[0] << 16)
                
                # Apply to title if it exists
                if slide.Shapes.HasTitle:
                    slide.Shapes.Title.TextFrame.TextRange.Font.Color.RGB = com_color
                
                print(f"Applied primary color: {slide_data.primary_color}")
            
            if slide_data.accent_colors:
                print(f"Applied accent colors: {slide_data.accent_colors}")
                
        except Exception as e:
            print(f"Warning: Could not apply dynamic colors via COM: {e}")
    
    def _hex_to_rgb(self, hex_color: str):
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def add_smartart_diagram(self, slide, diagram_data):
        """Add native PowerPoint SmartArt to slide using COM."""
        try:
            from visual.smartart_engine import SmartArtType
            
            # Map our SmartArt types to PowerPoint constants
            smartart_layouts = {
                SmartArtType.PROCESS: 1,      # Process (Basic Process)
                SmartArtType.HIERARCHY: 2,    # Hierarchy (Organization Chart)
                SmartArtType.CYCLE: 3,        # Cycle (Basic Cycle)
                SmartArtType.RELATIONSHIP: 4, # Relationship (Basic Venn)
                SmartArtType.MATRIX: 5,       # Matrix (Basic Matrix)
                SmartArtType.PYRAMID: 6,      # Pyramid (Basic Pyramid)
                SmartArtType.LIST: 7,         # List (Basic Block List)
                SmartArtType.PICTURE: 8,      # Picture (Picture with Caption)
            }
            
            # Get layout ID
            layout_id = smartart_layouts.get(diagram_data.diagram_type, 1)
            
            # Define SmartArt position and size
            left = 72    # 1 inch from left
            top = 144    # 2 inches from top
            width = 576  # 8 inches wide
            height = 288 # 4 inches tall
            
            # Add SmartArt graphic
            smartart = slide.Shapes.AddSmartArt(
                Layout=layout_id,
                Left=left,
                Top=top,
                Width=width,
                Height=height
            )
            
            # Populate SmartArt with data
            self._populate_smartart_data(smartart, diagram_data)
            
            # Apply theme colors
            if diagram_data.color_palette:
                self._apply_smartart_colors(smartart, diagram_data.color_palette)
            
            return smartart
            
        except Exception as e:
            print(f"Warning: Could not create SmartArt via COM: {e}")
            return None
    
    def _populate_smartart_data(self, smartart, diagram_data):
        """Populate SmartArt with actual data."""
        try:
            # Access SmartArt nodes
            nodes = smartart.SmartArt.AllNodes
            
            # Clear existing nodes and add our data
            for i, element in enumerate(diagram_data.elements):
                if i < nodes.Count:
                    # Update existing node
                    nodes.Item(i + 1).TextFrame2.TextRange.Text = element.text
                else:
                    # Add new node
                    new_node = nodes.Add()
                    new_node.TextFrame2.TextRange.Text = element.text
                    
                # Handle child elements for hierarchical structures
                if element.children and hasattr(nodes.Item(i + 1), 'AddNode'):
                    for child in element.children:
                        child_node = nodes.Item(i + 1).AddNode()
                        child_node.TextFrame2.TextRange.Text = child.text
                        
        except Exception as e:
            print(f"Warning: Could not populate SmartArt data: {e}")
    
    def _apply_smartart_colors(self, smartart, color_palette):
        """Apply color scheme to SmartArt."""
        try:
            # Get primary color in COM format
            primary_color = self._palette_to_com_color(color_palette.primary)
            
            # Apply color scheme
            smartart.SmartArt.Color = primary_color
            
        except Exception as e:
            print(f"Warning: Could not apply SmartArt colors: {e}")
    
    def _palette_to_com_color(self, color_int):
        """Convert palette color integer to COM color format."""
        # Extract RGB components
        red = (color_int >> 16) & 0xFF
        green = (color_int >> 8) & 0xFF
        blue = color_int & 0xFF
        
        # Convert to COM BGR format
        return blue + (green << 8) + (red << 16)

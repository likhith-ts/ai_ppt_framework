"""
Architecture diagram builder for creating system architecture slides.

This module provides specialized functionality for creating architecture diagrams
with components, connections, and system relationships.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from .base_builder import BaseSlideBuilder
from ...core.exceptions import SlideBuilderError
from ...visual.smartart_engine import SmartArtEngine, SmartArtType


@dataclass
class ArchitectureComponent:
    """Represents a component in the architecture."""
    
    name: str
    type: str  # e.g., "database", "service", "ui", "api"
    description: Optional[str] = None
    connections: Optional[List[str]] = None  # List of connected component names
    position: Optional[Dict[str, float]] = None  # x, y coordinates
    
    def __post_init__(self):
        if self.connections is None:
            self.connections = []


@dataclass
class ArchitectureData:
    """Data structure for architecture slide content."""
    
    title: str
    components: List[ArchitectureComponent]
    architecture_type: str = "system"  # system, microservices, layered, etc.
    description: Optional[str] = None
    layers: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.layers is None:
            self.layers = []


class ArchitectureSlideBuilder(BaseSlideBuilder):
    """
    Builder for creating architecture diagram slides.
    
    This builder creates technical architecture diagrams with components,
    connections, and system relationships.
    """
    
    def __init__(self):
        """Initialize the architecture slide builder."""
        super().__init__()
        self.smartart_engine = SmartArtEngine()
    
    def supports_slide_type(self, slide_type: str) -> bool:
        """Check if this builder supports the given slide type."""
        return slide_type.lower() in [
            'architecture', 'system', 'diagram', 'components',
            'microservices', 'infrastructure', 'deployment'
        ]
    
    def build_slide(self, slide_data: Dict[str, Any], presentation_engine: Any) -> bool:
        """
        Build an architecture slide.
        
        Args:
            slide_data: Dictionary containing slide information
            presentation_engine: Engine instance (COM or python-pptx)
            
        Returns:
            bool: True if slide was created successfully
        """
        try:
            # Parse architecture data
            arch_data = self._parse_architecture_data(slide_data)
            
            # Create slide
            slide = presentation_engine.add_slide(layout_name="blank")
            
            # Add title
            self._add_title(slide, arch_data.title)
            
            # Add description if present
            if arch_data.description:
                self._add_description(slide, arch_data.description)
            
            # Create architecture diagram
            self._create_architecture_diagram(slide, arch_data, presentation_engine)
            
            # Add legend if needed
            self._add_legend(slide, arch_data)
            
            self.slides_created += 1
            return True
            
        except Exception as e:
            self.handle_builder_error(e, "create architecture slide")
            return False
    
    def build(self, slide_data: Dict[str, Any]) -> object:
        """
        Build an architecture slide (legacy interface).
        
        Args:
            slide_data: Dictionary containing slide information
            
        Returns:
            object: The slide data structure
        """
        return {
            'type': 'architecture',
            'content': slide_data,
            'title': slide_data.get('title', 'System Architecture'),
            'components': slide_data.get('components', []),
            'architecture_type': slide_data.get('architecture_type', 'system')
        }
    
    def _parse_architecture_data(self, slide_data: Dict[str, Any]) -> ArchitectureData:
        """Parse slide data into architecture data structure."""
        components = []
        
        for comp_data in slide_data.get('components', []):
            component = ArchitectureComponent(
                name=comp_data.get('name', 'Component'),
                type=comp_data.get('type', 'service'),
                description=comp_data.get('description'),
                connections=comp_data.get('connections', []),
                position=comp_data.get('position')
            )
            components.append(component)
        
        return ArchitectureData(
            title=slide_data.get('title', 'Architecture'),
            components=components,
            architecture_type=slide_data.get('architecture_type', 'system'),
            description=slide_data.get('description'),
            layers=slide_data.get('layers', [])
        )
    
    def _add_title(self, slide: Any, title: str) -> None:
        """Add title to the slide."""
        try:
            title_shape = slide.shapes.title
            title_shape.text = title
        except AttributeError:
            # Fallback - add title as text box
            pass
    
    def _add_description(self, slide: Any, description: str) -> None:
        """Add description to the slide."""
        try:
            # Try to add as subtitle or text box
            if hasattr(slide, 'placeholders') and len(slide.placeholders) > 1:
                subtitle_shape = slide.placeholders[1]
                subtitle_shape.text = description
        except (AttributeError, IndexError):
            # Fallback - could add as text box
            pass
    
    def _create_architecture_diagram(self, slide: Any, arch_data: ArchitectureData, engine: Any = None) -> None:
        """Create the architecture diagram based on the architecture type."""
        if arch_data.architecture_type == 'microservices':
            self._create_microservices_diagram(slide, arch_data)
        elif arch_data.architecture_type == 'layered':
            self._create_layered_diagram(slide, arch_data)
        elif arch_data.architecture_type == 'system':
            self._create_system_diagram(slide, arch_data, engine)
        else:
            # Default to system diagram
            self._create_system_diagram(slide, arch_data, engine)
    
    def _create_microservices_diagram(self, slide: Any, arch_data: ArchitectureData) -> None:
        """Create microservices architecture diagram."""
        # Group components by type
        api_gateways = [c for c in arch_data.components if c.type == 'api_gateway']
        services = [c for c in arch_data.components if c.type == 'microservice']
        databases = [c for c in arch_data.components if c.type == 'database']
        
        # Position components
        y_positions = {
            'api_gateway': 0.2,
            'microservice': 0.5,
            'database': 0.8
        }
        
        # Add API gateway at the top
        for i, gateway in enumerate(api_gateways):
            x_pos = 0.5
            y_pos = y_positions['api_gateway']
            self._add_component_shape(slide, gateway, x_pos, y_pos)
        
        # Add services in the middle
        for i, service in enumerate(services):
            x_pos = 0.2 + (i * 0.6 / max(len(services) - 1, 1))
            y_pos = y_positions['microservice']
            self._add_component_shape(slide, service, x_pos, y_pos)
        
        # Add databases at the bottom
        for i, database in enumerate(databases):
            x_pos = 0.3 + (i * 0.4 / max(len(databases) - 1, 1))
            y_pos = y_positions['database']
            self._add_component_shape(slide, database, x_pos, y_pos)
    
    def _create_layered_diagram(self, slide: Any, arch_data: ArchitectureData) -> None:
        """Create layered architecture diagram."""
        layers = [c for c in arch_data.components if c.type == 'layer']
        
        for i, layer in enumerate(layers):
            y_pos = 0.2 + (i * 0.6 / max(len(layers) - 1, 1))
            self._add_layer_shape(slide, layer, 0.5, y_pos)
    
    def _create_system_diagram(self, slide: Any, arch_data: ArchitectureData, engine: Any = None) -> None:
        """Create system architecture diagram using SmartArt."""
        # Use SmartArt for system diagrams
        smartart_data = {
            'title': arch_data.title,
            'components': [
                {
                    'name': comp.name,
                    'description': comp.description or '',
                    'type': comp.type
                }
                for comp in arch_data.components
            ]
        }
        
        diagram = self.smartart_engine.create_diagram(
            smartart_data,
            SmartArtType.RELATIONSHIP,
            f"{arch_data.title} Components"
        )
        
        # Add SmartArt to slide using the presentation engine
        if engine and hasattr(engine, 'add_smartart_diagram'):
            engine.add_smartart_diagram(slide, diagram)
        else:
            # Fallback to text representation
            self._add_smartart_fallback(slide, diagram)
    
    def _add_smartart_fallback(self, slide: Any, diagram: Any) -> None:
        """Fallback method when SmartArt is not available - creates text representation."""
        try:
            # Create a simple text representation of the SmartArt
            fallback_text = f"{diagram.title}\n\n"
            
            for i, element in enumerate(diagram.elements):
                fallback_text += f"• {element.text}\n"
            
            # Try to add as text box (implementation depends on engine)
            # This is a basic fallback - in practice, we'd create simple shapes
            print(f"SmartArt fallback for: {diagram.title}")
            print(f"Elements: {len(diagram.elements)}")
            
        except Exception as e:
            print(f"Warning: Could not create SmartArt fallback: {e}")

    def _add_component_shape(self, slide: Any, component: ArchitectureComponent, x: float, y: float) -> None:
        """Add a component shape to the slide."""
        # This would depend on the presentation engine
        # For now, just add as text
        try:
            # Add component as text box or shape
            component_text = f"{component.name}\\n{component.description or ''}"
            # Position would be calculated based on slide dimensions
        except Exception:
            pass
    
    def _add_layer_shape(self, slide: Any, layer: ArchitectureComponent, x: float, y: float) -> None:
        """Add a layer shape to the slide."""
        # This would depend on the presentation engine
        try:
            # Add layer as horizontal rectangle
            layer_text = f"{layer.name}\\n{layer.description or ''}"
            # Position would be calculated based on slide dimensions
        except Exception:
            pass
    
    def _add_smartart_diagram(self, slide: Any, diagram: Any) -> None:
        """Add SmartArt diagram to the slide."""
        # This would depend on the presentation engine
        try:
            # Add SmartArt elements
            diagram_data = self.smartart_engine.export_diagram_data(diagram)
            # Use diagram_data to create shapes
        except Exception:
            pass
    
    def _add_legend(self, slide: Any, arch_data: ArchitectureData) -> None:
        """Add legend explaining component types."""
        component_types = set(comp.type for comp in arch_data.components)
        
        if len(component_types) > 1:
            # Add legend showing different component types
            legend_text = "Legend:\\n"
            for comp_type in component_types:
                legend_text += f"• {comp_type.replace('_', ' ').title()}\\n"
            
            # Add legend as text box in bottom right
            try:
                # This would depend on the presentation engine
                pass
            except Exception:
                pass

"""
SmartArt engine for generating and analyzing SmartArt diagrams.

This module provides intelligent SmartArt generation capabilities,
analyzing content structure and creating appropriate visual representations.
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict

from core.exceptions import FrameworkError
from design.color_system import ColorPalette


class SmartArtType(Enum):
    """SmartArt diagram types supported by the framework."""
    
    PROCESS = "process"
    HIERARCHY = "hierarchy"
    CYCLE = "cycle"
    RELATIONSHIP = "relationship"
    MATRIX = "matrix"
    PYRAMID = "pyramid"
    LIST = "list"
    PICTURE = "picture"


@dataclass
class SmartArtElement:
    """Represents a single element in a SmartArt diagram."""
    
    text: str
    level: int = 0
    children: Optional[List["SmartArtElement"]] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class SmartArtDiagram:
    """Represents a complete SmartArt diagram."""
    
    diagram_type: SmartArtType
    title: str
    elements: List[SmartArtElement]
    color_palette: Optional[ColorPalette] = None
    layout_options: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.layout_options is None:
            self.layout_options = {}


class SmartArtEngine:
    """
    Engine for creating and analyzing SmartArt diagrams.
    
    This class provides intelligent analysis of content structure
    and generates appropriate SmartArt representations.
    """
    
    def __init__(self, color_palette: Optional[ColorPalette] = None):
        """
        Initialize the SmartArt engine.
        
        Args:
            color_palette: Color palette for SmartArt styling
        """
        self.color_palette = color_palette
        self._type_analyzers = {
            SmartArtType.PROCESS: self._analyze_process,
            SmartArtType.HIERARCHY: self._analyze_hierarchy,
            SmartArtType.CYCLE: self._analyze_cycle,
            SmartArtType.RELATIONSHIP: self._analyze_relationship,
            SmartArtType.MATRIX: self._analyze_matrix,
            SmartArtType.PYRAMID: self._analyze_pyramid,
            SmartArtType.LIST: self._analyze_list,
        }
    
    def analyze_content_structure(self, content: Union[str, List[str], Dict[str, Any]]) -> SmartArtType:
        """
        Analyze content and determine the best SmartArt type.
        
        Args:
            content: Content to analyze (text, list, or structured data)
            
        Returns:
            SmartArtType: Recommended SmartArt type
        """
        if isinstance(content, str):
            return self._analyze_text_content(content)
        elif isinstance(content, list):
            return self._analyze_list_content(content)
        elif isinstance(content, dict):
            return self._analyze_structured_content(content)
        else:
            return SmartArtType.LIST  # Default fallback
    
    def create_diagram(
        self,
        content: Union[str, List[str], Dict[str, Any]],
        diagram_type: Optional[SmartArtType] = None,
        title: Optional[str] = None,
    ) -> SmartArtDiagram:
        """
        Create a SmartArt diagram from content.
        
        Args:
            content: Content to visualize
            diagram_type: Override automatic type detection
            title: Diagram title
            
        Returns:
            SmartArtDiagram: Generated diagram
        """
        if diagram_type is None:
            diagram_type = self.analyze_content_structure(content)
        
        analyzer = self._type_analyzers.get(diagram_type, self._analyze_list)
        elements = analyzer(content)
        
        return SmartArtDiagram(
            diagram_type=diagram_type,
            title=title or f"{diagram_type.value.title()} Diagram",
            elements=elements,
            color_palette=self.color_palette,
            layout_options=self._get_layout_options(diagram_type),
        )
    
    def _analyze_text_content(self, text: str) -> SmartArtType:
        """Analyze text content for SmartArt type."""
        text_lower = text.lower()
        
        # Look for process indicators
        process_keywords = ["step", "phase", "stage", "then", "next", "after", "before"]
        if any(keyword in text_lower for keyword in process_keywords):
            return SmartArtType.PROCESS
        
        # Look for hierarchy indicators
        hierarchy_keywords = ["manager", "director", "lead", "team", "reports to", "under"]
        if any(keyword in text_lower for keyword in hierarchy_keywords):
            return SmartArtType.HIERARCHY
        
        # Look for cycle indicators
        cycle_keywords = ["cycle", "loop", "repeat", "circular", "continuous"]
        if any(keyword in text_lower for keyword in cycle_keywords):
            return SmartArtType.CYCLE
        
        # Look for relationship indicators
        relationship_keywords = ["relationship", "connected", "linked", "associated"]
        if any(keyword in text_lower for keyword in relationship_keywords):
            return SmartArtType.RELATIONSHIP
        
        return SmartArtType.LIST  # Default
    
    def _analyze_list_content(self, content: List[str]) -> SmartArtType:
        """Analyze list content for SmartArt type."""
        if len(content) <= 3:
            return SmartArtType.LIST
        elif len(content) <= 6:
            return SmartArtType.PROCESS
        else:
            return SmartArtType.HIERARCHY
    
    def _analyze_structured_content(self, content: Dict[str, Any]) -> SmartArtType:
        """Analyze structured content for SmartArt type."""
        if "children" in str(content).lower():
            return SmartArtType.HIERARCHY
        elif "steps" in str(content).lower():
            return SmartArtType.PROCESS
        elif "matrix" in str(content).lower():
            return SmartArtType.MATRIX
        else:
            return SmartArtType.RELATIONSHIP
    
    def _analyze_process(self, content: Any) -> List[SmartArtElement]:
        """Create process diagram elements."""
        elements = []
        
        if isinstance(content, str):
            # Split by common delimiters
            steps = [s.strip() for s in content.split(". ") if s.strip()]
            for i, step in enumerate(steps):
                elements.append(SmartArtElement(
                    text=step,
                    level=0,
                    metadata={"step_number": i + 1}
                ))
        elif isinstance(content, list):
            for i, item in enumerate(content):
                elements.append(SmartArtElement(
                    text=str(item),
                    level=0,
                    metadata={"step_number": i + 1}
                ))
        
        return elements
    
    def _analyze_hierarchy(self, content: Any) -> List[SmartArtElement]:
        """Create hierarchy diagram elements."""
        elements = []
        
        if isinstance(content, dict):
            # Recursive hierarchy creation
            def create_hierarchy(data, level=0):
                for key, value in data.items():
                    element = SmartArtElement(text=str(key), level=level)
                    if isinstance(value, dict):
                        element.children = create_hierarchy(value, level + 1)
                    elif isinstance(value, list):
                        element.children = [
                            SmartArtElement(text=str(item), level=level + 1)
                            for item in value
                        ]
                    elements.append(element)
                return elements
            
            create_hierarchy(content)
        else:
            # Simple hierarchy
            if isinstance(content, list):
                for item in content:
                    elements.append(SmartArtElement(text=str(item), level=0))
        
        return elements
    
    def _analyze_cycle(self, content: Any) -> List[SmartArtElement]:
        """Create cycle diagram elements."""
        elements = []
        
        if isinstance(content, list):
            for item in content:
                elements.append(SmartArtElement(
                    text=str(item),
                    level=0,
                    metadata={"cycle_position": len(elements)}
                ))
        
        return elements
    
    def _analyze_relationship(self, content: Any) -> List[SmartArtElement]:
        """Create relationship diagram elements."""
        elements = []
        
        if isinstance(content, dict):
            for key, value in content.items():
                element = SmartArtElement(text=str(key), level=0)
                if isinstance(value, (list, tuple)):
                    element.children = [
                        SmartArtElement(text=str(item), level=1)
                        for item in value
                    ]
                elements.append(element)
        elif isinstance(content, list):
            for item in content:
                elements.append(SmartArtElement(text=str(item), level=0))
        
        return elements
    
    def _analyze_matrix(self, content: Any) -> List[SmartArtElement]:
        """Create matrix diagram elements."""
        elements = []
        
        if isinstance(content, dict):
            for key, value in content.items():
                elements.append(SmartArtElement(
                    text=str(key),
                    level=0,
                    metadata={"matrix_value": str(value)}
                ))
        
        return elements
    
    def _analyze_pyramid(self, content: Any) -> List[SmartArtElement]:
        """Create pyramid diagram elements."""
        elements = []
        
        if isinstance(content, list):
            for i, item in enumerate(content):
                elements.append(SmartArtElement(
                    text=str(item),
                    level=i,
                    metadata={"pyramid_level": i}
                ))
        
        return elements
    
    def _analyze_list(self, content: Any) -> List[SmartArtElement]:
        """Create list diagram elements."""
        elements = []
        
        if isinstance(content, list):
            for item in content:
                elements.append(SmartArtElement(text=str(item), level=0))
        elif isinstance(content, str):
            items = [s.strip() for s in content.split("\n") if s.strip()]
            for item in items:
                elements.append(SmartArtElement(text=item, level=0))
        
        return elements
    
    def _get_layout_options(self, diagram_type: SmartArtType) -> Dict[str, Any]:
        """Get layout options for a specific diagram type."""
        layout_options = {
            SmartArtType.PROCESS: {
                "direction": "horizontal",
                "connector_style": "arrow",
                "spacing": "medium",
            },
            SmartArtType.HIERARCHY: {
                "direction": "vertical",
                "connector_style": "line",
                "spacing": "large",
            },
            SmartArtType.CYCLE: {
                "direction": "circular",
                "connector_style": "arrow",
                "spacing": "medium",
            },
            SmartArtType.RELATIONSHIP: {
                "direction": "radial",
                "connector_style": "line",
                "spacing": "medium",
            },
            SmartArtType.MATRIX: {
                "direction": "grid",
                "connector_style": "none",
                "spacing": "small",
            },
            SmartArtType.PYRAMID: {
                "direction": "vertical",
                "connector_style": "none",
                "spacing": "small",
            },
            SmartArtType.LIST: {
                "direction": "vertical",
                "connector_style": "bullet",
                "spacing": "medium",
            },
        }
        
        return layout_options.get(diagram_type, {})
    
    def export_diagram_data(self, diagram: SmartArtDiagram) -> Dict[str, Any]:
        """
        Export diagram data for use with presentation engines.
        
        Args:
            diagram: SmartArt diagram to export
            
        Returns:
            dict: Diagram data suitable for presentation engines
        """
        return {
            "type": diagram.diagram_type.value,
            "title": diagram.title,
            "elements": [
                {
                    "text": element.text,
                    "level": element.level,
                    "children": [
                        {"text": child.text, "level": child.level}
                        for child in (element.children or [])
                    ],
                    "metadata": element.metadata,
                }
                for element in diagram.elements
            ],
            "color_palette": asdict(diagram.color_palette) if diagram.color_palette else None,
            "layout_options": diagram.layout_options,
        }

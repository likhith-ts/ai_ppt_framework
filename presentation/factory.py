"""
Presentation factory for the AI PowerPoint Framework.

This module provides a factory for creating presentation engines based on
system capabilities and user preferences, with automatic fallback handling.
"""

import platform
import sys
import importlib.util
from typing import Optional, List, Dict, Any
from pathlib import Path

from .base_engine import BasePresentationEngine, SlideData
from visual.enhanced_engine import EnhancedVisualEngine
from core.config import FrameworkConfig
from core.exceptions import PresentationGenerationError
from ai.content_analyzer import ContentAnalyzer


class PresentationFactory:
    """
    Factory for creating and managing presentation engines.

    Features:
    - Automatic engine selection based on system capabilities
    - Fallback engine handling for cross-platform compatibility
    - Engine availability detection
    - Unified presentation creation interface
    """

    def __init__(self, config: Optional[FrameworkConfig] = None):
        """
        Initialize the presentation factory.

        Args:
            config: Configuration object for engine initialization
        """
        self.config = config or FrameworkConfig()
        self._available_engines = self._detect_available_engines()
        
        # Initialize visual engine for AI-generated visuals
        try:
            from visual.enhanced_engine import EnhancedVisualEngine
            self.visual_engine = EnhancedVisualEngine(self.config)
        except Exception as e:
            print(f"Warning: Could not initialize visual engine: {e}")
            self.visual_engine = None

    def _detect_available_engines(self) -> List[str]:
        """Detect which presentation engines are available on this system."""
        available = []

        # Check for COM (Windows only) - test actual PowerPoint availability
        if platform.system() == "Windows":
            if importlib.util.find_spec("win32com"):
                if self._test_powerpoint_availability():
                    available.append("com")

        # Check for python-pptx (cross-platform)
        if importlib.util.find_spec("pptx"):
            available.append("pptx")

        return available
    
    def _test_powerpoint_availability(self) -> bool:
        """Test if PowerPoint is actually available via COM."""
        try:
            import win32com.client
            # Try to create PowerPoint instance
            powerpoint = win32com.client.Dispatch("PowerPoint.Application")
            powerpoint.Quit()
            return True
        except Exception:
            return False

    def get_available_engines(self) -> List[str]:
        """Get list of available presentation engines."""
        return self._available_engines.copy()

    def create_engine(
        self, engine_type: Optional[str] = None
    ) -> BasePresentationEngine:
        """
        Create a presentation engine instance.

        Args:
            engine_type: Specific engine type ("com", "pptx"). If None, auto-selects.

        Returns:
            Configured presentation engine instance

        Raises:
            PresentationGenerationError: If no engines are available
        """
        if not self._available_engines:
            raise PresentationGenerationError(
                "No presentation engines available. Please install python-pptx or run on Windows with COM support."
            )

        # Auto-select engine if not specified
        if engine_type is None:
            engine_type = self._get_preferred_engine()

        if engine_type not in self._available_engines:
            raise PresentationGenerationError(
                f"Engine '{engine_type}' is not available. Available engines: {self._available_engines}"
            )

        return self._create_engine_instance(engine_type)

    def _get_preferred_engine(self) -> str:
        """Get the preferred engine based on system and configuration."""
        # Prefer COM on Windows for better formatting if available
        if "com" in self._available_engines and self.config.enable_com_powerpoint:
            return "com"

        # Fall back to python-pptx for cross-platform compatibility
        if "pptx" in self._available_engines:
            return "pptx"

        # Return first available engine
        return self._available_engines[0]

    def _create_engine_instance(self, engine_type: str) -> BasePresentationEngine:
        """Create an instance of the specified engine type with fallback."""
        if engine_type == "com":
            try:
                from .com_engine import COMPresentationEngine
                return COMPresentationEngine(self.config)
            except Exception as e:
                # If COM fails and fallback is enabled, try pptx
                if self.config.enable_python_pptx_fallback and "pptx" in self._available_engines:
                    print(f"Warning: COM engine failed ({e}), falling back to python-pptx")
                    return self._create_engine_instance("pptx")
                else:
                    raise PresentationGenerationError(f"COM engine failed: {str(e)}")
        elif engine_type == "pptx":
            from .pptx_engine import PPTXPresentationEngine
            return PPTXPresentationEngine(self.config)
        else:
            raise PresentationGenerationError(f"Unknown engine type: {engine_type}")

    def create_presentation_from_analysis(
        self,
        analysis_result: str,
        output_path: Path,
        presentation_title: str = "AI Generated Presentation",
    ) -> bool:
        """
        Create a complete presentation from AI analysis result.

        Args:
            analysis_result: AI-generated presentation content
            output_path: Path where to save the presentation
            presentation_title: Title for the presentation

        Returns:
            True if successful, False otherwise

        Raises:
            PresentationGenerationError: If presentation creation fails
        """
        try:
            # Parse the analysis result into slide data
            slides_data = self._parse_analysis_result(analysis_result)
            
            print(f"Factory: Parsed {len(slides_data)} slides")
            for i, slide in enumerate(slides_data):
                print(f"  Slide {i+1}: {slide.title} ({len(slide.points)} points)")

            # Generate AI visuals for slides if enabled
            if self.config.enable_image_generation and hasattr(self, 'visual_engine'):
                print("Factory: Generating AI visuals...")
                slides_data = self._enhance_slides_with_visuals(slides_data, analysis_result)

            # Create presentation engine
            engine = self.create_engine()
            print(f"Factory: Using engine: {type(engine).__name__}")

            # Create the presentation
            success = engine.create_full_presentation(
                slides_data, output_path, presentation_title
            )
            
            print(f"Factory: Presentation creation success: {success}")

            return success

        except Exception as e:
            raise PresentationGenerationError(
                f"Failed to create presentation: {str(e)}"
            ) from e

    def create_presentation_from_zip(
        self,
        uploaded_file,
        output_path: Path,
        presentation_title: str = "Repository Analysis",
    ) -> bool:
        """
        Create a presentation directly from uploaded ZIP file.

        Args:
            uploaded_file: Streamlit uploaded file object
            output_path: Path where to save the presentation
            presentation_title: Title for the presentation

        Returns:
            True if successful, False otherwise
        """
        try:
            # Extract and analyze content
            analyzer = ContentAnalyzer()
            analyzer.extract_zip_contents(uploaded_file)
            analysis = analyzer.analyze_project()

            # Generate fallback content based on analysis
            from ai.prompt_templates import PromptTemplates

            analysis_result = PromptTemplates.get_fallback_content_template(
                project_type=analysis["project_type"],
                tech_stack=analyzer.get_primary_technologies(),
                complexity=analysis["complexity"],
                maturity=analysis["maturity"],
                file_count=analysis["file_metrics"]["total_files"],
            )

            # Create presentation
            return self.create_presentation_from_analysis(
                analysis_result, output_path, presentation_title
            )

        except Exception as e:
            raise PresentationGenerationError(
                f"Failed to create presentation from ZIP: {str(e)}"
            ) from e

    def _parse_analysis_result(self, analysis_result: str) -> List[SlideData]:
        """
        Parse AI analysis result into structured slide data.

        Args:
            analysis_result: Raw AI-generated content

        Returns:
            List of SlideData objects
        """
        slides_data = []
        current_slide = None

        lines = analysis_result.strip().split("\n")

        for line in lines:
            line = line.strip()
            
            # Remove markdown formatting
            clean_line = line.replace("**", "").replace("*", "")

            if (clean_line.startswith("SLIDE ") and " - " in clean_line) or line.startswith("**SLIDE "):
                # Save previous slide if exists
                if current_slide:
                    slides_data.append(current_slide)

                # Start new slide
                current_slide = {
                    "title": "",
                    "points": [],
                    "theme": "corporate_modern",
                    "slide_type": "content_slide",
                }

            elif (clean_line.startswith("TITLE:") or line.startswith("**TITLE:")) and current_slide is not None:
                title_text = clean_line.replace("TITLE:", "").strip()
                current_slide["title"] = title_text

            elif (clean_line.startswith("THEME_SUGGESTION:") or line.startswith("**THEME_SUGGESTION:")) and current_slide is not None:
                theme_value = clean_line.replace("THEME_SUGGESTION:", "").strip()
                current_slide["theme"] = theme_value

            elif (clean_line.startswith("SLIDE_TYPE:") or line.startswith("**SLIDE_TYPE:")) and current_slide is not None:
                slide_type = clean_line.replace("SLIDE_TYPE:", "").strip()
                current_slide["slide_type"] = slide_type

            elif (line.startswith("- ") or line.startswith("**- ")) and current_slide is not None:
                point = line.replace("**", "").replace("- ", "").strip()
                if point:
                    current_slide["points"].append(point)

        # Save last slide
        if current_slide:
            slides_data.append(current_slide)

        # Convert to SlideData objects
        from design.themes import DesignTheme

        result = []

        for slide_dict in slides_data:
            # Map theme string to enum
            theme_str = slide_dict.get("theme", "corporate_modern")
            try:
                theme = DesignTheme(theme_str)
            except ValueError:
                theme = DesignTheme.CORPORATE_MODERN

            # Generate AI visuals for the slide
            background_image = None
            diagram_image = None
            feature_icons = []
            
            if self.config.enable_image_generation and self.visual_engine:
                slide_type = slide_dict.get("slide_type", "content_slide")
                title = slide_dict.get("title", "")
                points = slide_dict.get("points", [])
                
                # Generate visuals based on slide type
                if slide_type == "architecture_slide":
                    # Extract tech stack and components from content
                    tech_stack = self._extract_tech_stack(f"{title} {' '.join(points)}")
                    components = self._extract_components(points)
                    diagram_image = self.visual_engine.create_architecture_visual(
                        tech_stack, components, theme
                    )
                elif slide_type == "roadmap_slide":
                    # Extract milestones from content
                    milestones = self._extract_milestones(points)
                    diagram_image = self.visual_engine.create_roadmap_visual(
                        milestones, "future", theme
                    )
                elif slide_type == "metrics_slide":
                    # Extract metrics from content
                    metrics = self._extract_metrics(points)
                    diagram_image = self.visual_engine.create_metrics_visual(
                        metrics, "mixed", theme
                    )
                elif slide_type == "features_slide":
                    # Generate feature icons
                    features = self._extract_features(points)
                    feature_icons = self.visual_engine.create_feature_icons(features, theme)

            slide_data = SlideData(
                title=slide_dict.get("title", "Untitled Slide"),
                points=slide_dict.get("points", []),
                theme=theme,
                slide_type=slide_dict.get("slide_type", "content_slide"),
                background_image=background_image,
                diagram_image=diagram_image,
                feature_icons=feature_icons,
            )
            result.append(slide_data)

        return result

    def _enhance_slides_with_visuals(self, slides_data: List[SlideData], analysis_result: str) -> List[SlideData]:
        """
        Enhance slides with AI-generated visuals and backgrounds.
        
        Args:
            slides_data: List of slide data to enhance
            analysis_result: Original analysis result for context
            
        Returns:
            Enhanced slide data with visuals
        """
        if not self.visual_engine:
            return slides_data
        
        enhanced_slides = []
        
        # Extract tech stack and project info for visual generation
        tech_stack = self._extract_tech_stack(analysis_result)
        project_type = self._extract_project_type(analysis_result)
        
        # Generate theme package
        theme_package = self.visual_engine.generate_theme_package(
            project_type, tech_stack, "moderate"
        )
        
        for i, slide in enumerate(slides_data):
            enhanced_slide = slide
            
            # Generate slide-specific visuals based on slide type
            if slide.slide_type == "architecture_slide" and self.visual_engine:
                components = self._extract_components(slide.points)
                diagram_image = self.visual_engine.create_architecture_visual(
                    tech_stack, components, slide.theme
                )
                if diagram_image:
                    enhanced_slide.diagram_image = diagram_image
                    
            elif slide.slide_type == "roadmap_slide" and self.visual_engine:
                milestones = self._extract_milestones(slide.points)
                diagram_image = self.visual_engine.create_roadmap_visual(
                    milestones, "future", slide.theme
                )
                if diagram_image:
                    enhanced_slide.diagram_image = diagram_image
                    
            elif slide.slide_type == "metrics_slide" and self.visual_engine:
                metrics = self._extract_metrics(slide.points)
                diagram_image = self.visual_engine.create_metrics_visual(
                    metrics, "mixed", slide.theme
                )
                if diagram_image:
                    enhanced_slide.diagram_image = diagram_image
                    
            elif slide.slide_type == "features_slide" and self.visual_engine:
                features = self._extract_features(slide.points)
                feature_icons = self.visual_engine.create_feature_icons(features, slide.theme)
                if feature_icons:
                    enhanced_slide.feature_icons = feature_icons
            
            # Generate background for all slides
            if theme_package.get("ai_backgrounds") and i < len(theme_package["ai_backgrounds"]):
                enhanced_slide.background_image = theme_package["ai_backgrounds"][i]
            
            # Apply dynamic color scheme
            if "primary_color" in theme_package:
                enhanced_slide.primary_color = theme_package["primary_color"]
            if "accent_colors" in theme_package:
                enhanced_slide.accent_colors = theme_package["accent_colors"]
            
            enhanced_slides.append(enhanced_slide)
        
        return enhanced_slides
    
    def _extract_tech_stack(self, analysis_result: str) -> List[str]:
        """Extract technology stack from analysis result."""
        # Simple extraction - look for common tech terms
        tech_terms = ["Python", "JavaScript", "TypeScript", "React", "Vue", "Angular", 
                     "Node.js", "Django", "Flask", "FastAPI", "Docker", "AWS", "Azure"]
        found_tech = []
        for tech in tech_terms:
            if tech.lower() in analysis_result.lower():
                found_tech.append(tech)
        return found_tech[:5]  # Limit to 5
    
    def _extract_project_type(self, analysis_result: str) -> str:
        """Extract project type from analysis result."""
        if "web" in analysis_result.lower():
            return "Web Application"
        elif "ai" in analysis_result.lower() or "ml" in analysis_result.lower():
            return "AI Application"
        elif "mobile" in analysis_result.lower():
            return "Mobile Application"
        else:
            return "Software Application"
    
    def _extract_components(self, points: List[str]) -> List[str]:
        """Extract system components from slide points."""
        # Extract component-like terms from points
        components = []
        for point in points:
            if any(keyword in point.lower() for keyword in ["component", "service", "module", "layer"]):
                components.append(point.split()[0])  # First word as component name
        return components[:6]  # Limit to 6 components
    
    def _extract_milestones(self, points: List[str]) -> List[str]:
        """Extract milestones from slide points."""
        return [point.split(".")[0] if "." in point else point for point in points[:4]]
    
    def _extract_metrics(self, points: List[str]) -> Dict[str, Any]:
        """Extract metrics from slide points."""
        metrics = {}
        for i, point in enumerate(points[:4]):
            metrics[f"Metric_{i+1}"] = f"Value_{i+1}"
        return metrics
    
    def _extract_features(self, points: List[str]) -> List[str]:
        """Extract features from slide points."""
        return [point.split()[0] if point else f"Feature_{i}" for i, point in enumerate(points[:4])]

    def get_engine_info(self) -> dict:
        """Get information about available engines and system capabilities."""
        return {
            "available_engines": self._available_engines,
            "preferred_engine": self._get_preferred_engine()
            if self._available_engines
            else None,
            "platform": platform.system(),
            "python_version": sys.version,
            "com_available": "com" in self._available_engines,
            "pptx_available": "pptx" in self._available_engines,
        }

    def create_presentation_from_agent_plan(
        self,
        presentation_plan,  # PresentationPlan from autogen_agents
        output_path: Path,
        presentation_title: str = "AI Generated Presentation",
    ) -> bool:
        """
        Create a complete presentation from AutoGen multi-agent plan.

        Args:
            presentation_plan: PresentationPlan object from multi-agent system
            output_path: Path where to save the presentation
            presentation_title: Title for the presentation

        Returns:
            True if successful, False otherwise

        Raises:
            PresentationGenerationError: If presentation creation fails
        """
        try:
            print(f"Factory: Creating presentation from multi-agent plan (quality: {presentation_plan.quality_score:.2f})")
            
            # Convert agent plan to slide data
            slides_data = self._convert_agent_plan_to_slides(presentation_plan)
            
            print(f"Factory: Converted to {len(slides_data)} slides")
            for i, slide in enumerate(slides_data):
                print(f"  Slide {i+1}: {slide.title} ({len(slide.points)} points)")

            # Generate AI visuals based on agent recommendations
            if self.config.enable_image_generation and hasattr(self, 'visual_engine'):
                print("Factory: Generating AI visuals from agent recommendations...")
                slides_data = self._enhance_slides_with_agent_visuals(slides_data, presentation_plan)

            # Create presentation engine
            engine = self.create_engine()
            print(f"Factory: Using engine: {type(engine).__name__}")

            # Create the presentation
            success = engine.create_full_presentation(
                slides_data, output_path, presentation_title
            )
            
            print(f"Factory: Multi-agent presentation creation success: {success}")

            return success

        except Exception as e:
            raise PresentationGenerationError(
                f"Failed to create presentation from agent plan: {str(e)}"
            ) from e

    def _convert_agent_plan_to_slides(self, presentation_plan) -> List[SlideData]:
        """Convert multi-agent presentation plan to slide data"""
        slides_data = []
        
        # Get design strategy for color scheme
        design_strategy = presentation_plan.design_strategy
        color_scheme = design_strategy.get("color_scheme", {})
        
        for slide_info in presentation_plan.content_structure:
            slide_data = SlideData(
                title=slide_info.get("title", ""),
                points=self._extract_slide_points(slide_info),
                slide_type=slide_info.get("slide_type", "content"),
                background_color=color_scheme.get("background", "#FFFFFF"),
                title_color=color_scheme.get("text", "#333333"),
                text_color=color_scheme.get("text", "#333333"),
                primary_color=color_scheme.get("primary", "#2E86AB"),
                accent_colors=[
                    color_scheme.get("secondary", "#A23B72"),
                    color_scheme.get("accent", "#F18F01")
                ],
                custom_visuals=slide_info.get("visual_elements", {})
            )
            slides_data.append(slide_data)
        
        return slides_data
    
    def _extract_slide_points(self, slide_info: Dict[str, Any]) -> List[str]:
        """Extract bullet points from slide content"""
        points = []
        
        content = slide_info.get("content", {})
        if isinstance(content, dict):
            # Extract main points
            main_points = content.get("main_points", [])
            if isinstance(main_points, list):
                points.extend(main_points)
            
            # Add supporting details as additional points
            supporting_details = content.get("supporting_details", [])
            if isinstance(supporting_details, list):
                points.extend(supporting_details)
        
        # If no structured content, create basic points
        if not points:
            points = [
                slide_info.get("title", "Content"),
                slide_info.get("subtitle", "Details"),
                "Key information and insights"
            ]
        
        return points[:5]  # Limit to 5 bullet points per slide
    
    def _enhance_slides_with_agent_visuals(self, slides_data: List[SlideData], presentation_plan) -> List[SlideData]:
        """Enhance slides with AI-generated visuals based on agent recommendations"""
        if not self.visual_engine or not self.visual_engine.dalle_client:
            return slides_data
        
        try:
            # Get diagram recommendations from agents
            diagram_plan = presentation_plan.visual_elements.get("diagrams", {})
            recommended_diagrams = diagram_plan.get("recommended_diagrams", [])
            
            # Get AI prompts from diagram expert
            ai_prompts = diagram_plan.get("ai_prompts", {})
            dalle_prompts = ai_prompts.get("dalle_prompts", [])
            
            # Enhance each slide with appropriate visuals
            for i, slide in enumerate(slides_data):
                # Find matching diagram for this slide
                matching_diagram = None
                for diagram in recommended_diagrams:
                    if diagram.get("slide_number") == i + 1:
                        matching_diagram = diagram
                        break
                
                if matching_diagram:
                    # Generate diagram-specific visuals
                    diagram_type = matching_diagram.get("diagram_type", "system_architecture")
                    
                    # Create specialized prompt for this slide
                    slide_prompt = f"Professional {diagram_type} diagram: {slide.title}"
                    if dalle_prompts and i < len(dalle_prompts):
                        slide_prompt = dalle_prompts[i]
                    
                    # Generate background image using DALL-E
                    try:
                        background_image = self.visual_engine.dalle_client.generate_background(
                            slide.title, slide_prompt
                        )
                        if background_image:
                            slide.background_image = background_image
                    except Exception as e:
                        print(f"Factory: Error generating background for slide {i+1}: {e}")
                    
                    # Generate diagram image for architecture slides
                    if diagram_type == "system_architecture":
                        try:
                            diagram_image = self.visual_engine.dalle_client.generate_architecture_diagram(
                                slide.points[:3], slide.points[3:], "professional"
                            )
                            if diagram_image:
                                slide.diagram_image = diagram_image
                        except Exception as e:
                            print(f"Factory: Error generating architecture diagram for slide {i+1}: {e}")
                
                print(f"Factory: Enhanced slide {i+1} with agent-recommended visuals")
        
        except Exception as e:
            print(f"Factory: Error enhancing slides with agent visuals: {e}")
        
        return slides_data

    def create_data_presentation(self, analysis_result: Dict[str, Any], 
                                output_path: str, title: str = "Data Analysis") -> str:
        """
        Create a presentation from data analysis results.
        
        Args:
            analysis_result: Results from DataVisualizationAgent
            output_path: Path for the output presentation
            title: Presentation title
            
        Returns:
            Path to the created presentation
        """
        try:
            # Get the appropriate engine
            engine = self.create_engine()
            
            # Convert analysis result to slide data
            slides_data = self._convert_data_analysis_to_slides(analysis_result, title)
            
            # Create presentation
            success = engine.create_full_presentation(slides_data, Path(output_path), title)
            
            if success:
                return output_path
            else:
                raise PresentationGenerationError("Presentation creation returned False")
            
            return presentation_path
            
        except Exception as e:
            raise PresentationGenerationError(f"Data presentation creation failed: {e}")
    
    def _convert_data_analysis_to_slides(self, analysis_result: Dict[str, Any], 
                                        title: str) -> List[SlideData]:
        """Convert data analysis results to slide data format"""
        slides = []
        
        try:
            # Title slide
            title_slide = SlideData(
                title=title,
                points=[f"Analysis of {analysis_result.get('data_overview', {}).get('name', 'Dataset')}"],
                slide_type="title"
            )
            slides.append(title_slide)
            
            # Data overview slide
            overview = analysis_result.get('data_overview', {})
            overview_points = [
                f"Dataset: {overview.get('name', 'Dataset')}",
                f"Records: {overview.get('rows', 0):,}",
                f"Columns: {overview.get('columns', 0)}",
                f"Data Types: {overview.get('numeric_columns', 0)} numeric, {overview.get('categorical_columns', 0)} categorical"
            ]
            
            overview_slide = SlideData(
                title="Dataset Overview",
                points=overview_points,
                slide_type="content"
            )
            slides.append(overview_slide)
            
            # Chart slides from insights
            insights = analysis_result.get('insights', [])
            chart_configs = analysis_result.get('chart_configurations', [])
            
            for i, (insight, chart_config) in enumerate(zip(insights, chart_configs)):
                chart_slide = SlideData(
                    title=insight.get('title', f'Analysis {i+1}'),
                    points=[insight.get('description', '')],
                    slide_type="chart",
                    custom_visuals={'chart_config': chart_config}  # Store chart configuration
                )
                slides.append(chart_slide)
            
            # Key findings slide
            findings = analysis_result.get('key_findings', [])
            if findings:
                findings_slide = SlideData(
                    title="Key Findings",
                    points=findings,
                    slide_type="content"
                )
                slides.append(findings_slide)
            
            # AI insights slide if available
            ai_analysis = analysis_result.get('ai_analysis', {})
            if ai_analysis and 'business_implications' in ai_analysis:
                implications = ai_analysis.get('business_implications', [])
                if isinstance(implications, str):
                    implications = [implications]
                
                ai_slide = SlideData(
                    title="AI Insights & Business Implications",
                    points=implications[:6],  # Max 6 points
                    slide_type="content"
                )
                slides.append(ai_slide)
            
            return slides
            
        except Exception as e:
            raise PresentationGenerationError(f"Failed to convert data analysis to slides: {e}")

"""
Main AI PowerPoint Framework interface.

This module provides the primary interface for the AI PowerPoint Framework,
offering a simple, unified API for presentation generation from various sources
with AutoGen multi-agent collaboration for enhanced quality.
"""

from typing import Optional, Union, List
from pathlib import Path
import logging

from core.config import FrameworkConfig
from core.exceptions import FrameworkError, PresentationGenerationError
from ai.gemini_client import GeminiClient
from ai.content_analyzer import ContentAnalyzer
from ai.prompt_templates import PromptTemplates
from ai.autogen_agents import create_multi_agent_system, MultiAgentPresentationSystem
from presentation.factory import PresentationFactory
from visual.enhanced_engine import EnhancedVisualEngine
from utils.file_handler import ZipExtractor


logger = logging.getLogger(__name__)


class AIPresenterFramework:
    """
    Main interface for the AI PowerPoint Framework.

    This class provides a high-level, easy-to-use interface for generating
    professional PowerPoint presentations from various sources using AI analysis.

    Features:
    - Automatic repository analysis
    - AI-powered content generation
    - Professional slide design
    - Multiple output formats
    - Robust error handling

    Example:
        Basic usage:
        ```python
        framework = AIPresenterFramework()
        ppt_path = framework.create_from_zip("repository.zip")
        ```

        Advanced usage:
        ```python
        config = FrameworkConfig()
        framework = AIPresenterFramework(config)
        ppt_path = framework.create_from_zip(
            "repository.zip",
            output_path="analysis.pptx",
            presentation_title="Repository Analysis"
        )
        ```
    """

    def __init__(self, config: Optional[FrameworkConfig] = None):
        """
        Initialize the AI PowerPoint Framework.

        Args:
            config: Configuration object. If None, uses default configuration.

        Raises:
            FrameworkError: If framework initialization fails
        """
        try:
            self.config = config or FrameworkConfig()
            self.gemini_client = GeminiClient(self.config)
            self.content_analyzer = ContentAnalyzer()
            self.presentation_factory = PresentationFactory(self.config)
            self.visual_engine = EnhancedVisualEngine(self.config)
            
            # Initialize multi-agent system for enhanced quality
            self.multi_agent_system = create_multi_agent_system(self.config)
            
            logger.info("AI PowerPoint Framework initialized successfully")
            
            # Log multi-agent system status
            agent_status = self.multi_agent_system.get_system_status()
            logger.info(f"Multi-agent system initialized: {agent_status}")

        except Exception as e:
            raise FrameworkError(f"Failed to initialize framework: {str(e)}") from e

    def create_from_zip(
        self,
        zip_file_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        presentation_title: str = "Repository Analysis",
        use_ai: bool = True,
        custom_theme_prompt: Optional[str] = None,
        custom_content_prompt: Optional[str] = None,
    ) -> Path:
        """
        Create a PowerPoint presentation from a ZIP file.

        Args:
            zip_file_path: Path to the ZIP file or uploaded file object
            output_path: Where to save the presentation. If None, auto-generates name.
            presentation_title: Title for the presentation
            use_ai: Whether to use AI for content generation (fallback if False)
            custom_theme_prompt: Custom theme description from user
            custom_content_prompt: Custom content instructions from user

        Returns:
            Path to the created PowerPoint file

        Raises:
            FrameworkError: If presentation creation fails
        """
        try:
            logger.info(f"Creating presentation from ZIP: {zip_file_path}")

            # Determine output path
            if output_path is None:
                output_path = Path("ai_generated_presentation.pptx")
            else:
                output_path = Path(output_path)

            # Extract and analyze content
            if hasattr(zip_file_path, "getvalue"):
                # Streamlit uploaded file
                content = self.content_analyzer.extract_zip_contents(zip_file_path)
            else:
                # File path
                content = self.content_analyzer.extract_zip_contents_from_path(zip_file_path)

            analysis = self.content_analyzer.analyze_project()

            # Generate presentation content
            if use_ai and self.config.gemini_api_key:
                try:
                    content_result = self._generate_ai_content(content, custom_content_prompt)
                    logger.info(f"AI content generated: {len(content_result)} characters")
                except Exception as e:
                    logger.warning(f"AI content generation failed, using fallback: {str(e)}")
                    content_result = self._generate_fallback_content(analysis)
                    logger.info(f"Fallback content generated: {len(content_result)} characters")
            else:
                content_result = self._generate_fallback_content(analysis)
                logger.info(f"Fallback content generated: {len(content_result)} characters")

            # Debug: Parse slides to check count
            parsed_slides = self.presentation_factory._parse_analysis_result(content_result)
            logger.info(f"Parsed {len(parsed_slides)} slides from content")

            # Create presentation
            success = self.presentation_factory.create_presentation_from_analysis(
                content_result, output_path, presentation_title
            )

            if success:
                logger.info(f"Presentation created successfully: {output_path}")
                return output_path
            else:
                raise PresentationGenerationError("Failed to create presentation")

        except Exception as e:
            logger.error(f"Failed to create presentation from ZIP: {str(e)}")
            raise FrameworkError(f"Failed to create presentation: {str(e)}") from e

    def create_from_content(
        self,
        content: str,
        output_path: Optional[Union[str, Path]] = None,
        presentation_title: str = "Content Analysis",
        use_ai: bool = True,
    ) -> Path:
        """
        Create a PowerPoint presentation from text content.

        Args:
            content: Text content to analyze and present
            output_path: Where to save the presentation
            presentation_title: Title for the presentation
            use_ai: Whether to use AI for content generation

        Returns:
            Path to the created PowerPoint file
        """
        try:
            logger.info("Creating presentation from content")

            # Determine output path
            if output_path is None:
                output_path = Path("content_presentation.pptx")
            else:
                output_path = Path(output_path)

            # Analyze content
            analysis = self.content_analyzer.analyze_project(content)

            # Generate presentation content
            if use_ai and self.config.gemini_api_key:
                try:
                    content_result = self._generate_ai_content(content)
                except Exception as e:
                    logger.warning(f"AI content generation failed, using fallback: {str(e)}")
                    content_result = self._generate_fallback_content(analysis)
            else:
                content_result = self._generate_fallback_content(analysis)

            # Create presentation
            success = self.presentation_factory.create_presentation_from_analysis(
                content_result, output_path, presentation_title
            )

            if success:
                logger.info(f"Presentation created successfully: {output_path}")
                return output_path
            else:
                raise PresentationGenerationError("Failed to create presentation")

        except Exception as e:
            logger.error(f"Failed to create presentation from content: {str(e)}")
            raise FrameworkError(f"Failed to create presentation: {str(e)}") from e

    def create_from_zip_with_agents(
        self,
        zip_file_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        presentation_title: str = "Repository Analysis",
        use_multi_agent: bool = True,
        custom_theme_prompt: Optional[str] = None,
        custom_content_prompt: Optional[str] = None,
    ) -> Path:
        """
        Create a PowerPoint presentation from a ZIP file using multi-agent collaboration.

        This method uses the AutoGen multi-agent system for enhanced quality,
        with specialized agents for content analysis, design, diagrams, and QA.

        Args:
            zip_file_path: Path to the ZIP file or uploaded file object
            output_path: Where to save the presentation. If None, auto-generates name.
            presentation_title: Title for the presentation
            use_multi_agent: Whether to use multi-agent system (fallback to single AI if False)
            custom_theme_prompt: Custom theme description from user
            custom_content_prompt: Custom content instructions from user

        Returns:
            Path to the created PowerPoint file

        Raises:
            FrameworkError: If presentation creation fails
        """
        try:
            logger.info(f"Creating presentation from ZIP using multi-agent system: {zip_file_path}")

            # Determine output path
            if output_path is None:
                output_path = Path("ai_generated_presentation.pptx")
            else:
                output_path = Path(output_path)

            # Extract and analyze content
            if hasattr(zip_file_path, "getvalue"):
                # Streamlit uploaded file
                content = self.content_analyzer.extract_zip_contents(zip_file_path)
            else:
                # File path
                content = self.content_analyzer.extract_zip_contents_from_path(zip_file_path)

            # Use multi-agent system for enhanced analysis
            if use_multi_agent and self.config.openai_api_key:
                try:
                    print("🤖 Starting multi-agent presentation generation...")
                    
                    # Generate comprehensive presentation plan using multiple agents
                    presentation_plan = self.multi_agent_system.generate_presentation_plan(content)
                    
                    logger.info(f"Multi-agent analysis complete. Quality score: {presentation_plan.quality_score:.2f}")
                    
                    # Create presentation from agent-generated plan
                    success = self.presentation_factory.create_presentation_from_agent_plan(
                        presentation_plan, output_path, presentation_title
                    )
                    
                    if success:
                        logger.info(f"Multi-agent presentation created successfully: {output_path}")
                        return output_path
                    else:
                        raise PresentationGenerationError("Failed to create multi-agent presentation")
                        
                except Exception as e:
                    logger.warning(f"Multi-agent generation failed, falling back to single AI: {str(e)}")
                    # Fall back to single AI approach
                    return self.create_from_zip(
                        zip_file_path, output_path, presentation_title, 
                        use_ai=True, custom_theme_prompt=custom_theme_prompt, 
                        custom_content_prompt=custom_content_prompt
                    )
            else:
                # Fall back to single AI approach
                logger.info("Using single AI approach (multi-agent disabled or no OpenAI key)")
                return self.create_from_zip(
                    zip_file_path, output_path, presentation_title, 
                    use_ai=True, custom_theme_prompt=custom_theme_prompt, 
                    custom_content_prompt=custom_content_prompt
                )

        except Exception as e:
            logger.error(f"Failed to create presentation from ZIP with agents: {str(e)}")
            raise FrameworkError(f"Failed to create presentation: {str(e)}") from e

    def _generate_ai_content(self, content: str, custom_prompt: Optional[str] = None) -> str:
        """Generate content using AI (Gemini)."""
        try:
            if custom_prompt:
                # Enhance the prompt with custom instructions
                base_prompt = PromptTemplates.get_repository_analysis_prompt(content)
                enhanced_prompt = f"{base_prompt}\n\nAdditional Instructions: {custom_prompt}"
                prompt = enhanced_prompt
            else:
                prompt = PromptTemplates.get_repository_analysis_prompt(content)
            
            return self.gemini_client.generate_content(prompt)
        except Exception as e:
            logger.warning(f"AI content generation failed: {str(e)}")
            # This exception will be caught by the caller, which will use fallback
            raise

    def _generate_fallback_content(self, analysis: dict) -> str:
        """Generate fallback content when AI is unavailable."""
        return PromptTemplates.get_fallback_content_template(
            project_type=analysis.get("project_type", "Software Application"),
            tech_stack=self.content_analyzer.get_primary_technologies(),
            complexity=analysis.get("complexity", "Moderate"),
            maturity=analysis.get("maturity", "Development-stage"),
            file_count=analysis.get("file_metrics", {}).get("total_files", 0),
        )

    def get_system_info(self) -> dict:
        """
        Get information about the framework and system capabilities.

        Returns:
            Dictionary with system information
        """
        return {
            "framework_version": "1.0.0",
            "config": {
                "gemini_available": bool(self.config.gemini_api_key),
                "max_slides": self.config.max_slides,
            },
            "engines": self.presentation_factory.get_engine_info(),
            "gemini_stats": self.gemini_client.get_usage_stats(),
        }

    def validate_setup(self) -> dict:
        """
        Validate that the framework is properly set up.

        Returns:
            Dictionary with validation results
        """
        validation = {"valid": True, "errors": [], "warnings": []}

        # Check API key
        if not self.config.gemini_api_key:
            validation["warnings"].append(
                "Gemini API key not configured - will use fallback content"
            )

        # Check presentation engines
        available_engines = self.presentation_factory.get_available_engines()
        if not available_engines:
            validation["valid"] = False
            validation["errors"].append("No presentation engines available")

        # Check configuration
        try:
            self.config.validate()
        except Exception as e:
            validation["valid"] = False
            validation["errors"].append(f"Configuration error: {str(e)}")

        return validation

    def create_from_data_source(self, data_source: str, 
                               output_path: Optional[Union[str, Path]] = None,
                               presentation_title: Optional[str] = None,
                               **kwargs) -> Path:
        """
        Create a presentation from a data source (Google Sheets, CSV, Excel).

        This method creates data-driven presentations with charts and insights
        from various data sources, similar to the DEV.to article approach.

        Args:
            data_source: Path/URL to data source (Google Sheets ID/URL, CSV/Excel file)
            output_path: Where to save the presentation
            presentation_title: Title for the presentation
            **kwargs: Additional parameters for data loading

        Returns:
            Path to the created PowerPoint file

        Raises:
            FrameworkError: If presentation creation fails
        """
        try:
            logger.info(f"Creating data-driven presentation from: {data_source}")

            # Initialize data visualization agent
            from ai.autogen_agents import DataVisualizationAgent
            data_agent = DataVisualizationAgent(self.config)

            # Analyze data source
            analysis_result = data_agent.analyze_data_for_presentation(
                data_source, **kwargs
            )

            # Determine output path
            if output_path is None:
                source_name = Path(data_source).stem if Path(data_source).exists() else "data"
                output_path = Path(f"{source_name}_presentation.pptx")
            else:
                output_path = Path(output_path)

            # Create presentation
            presentation_result = self.presentation_factory.create_data_presentation(
                analysis_result,
                str(output_path),
                title=presentation_title or "Data Analysis Presentation"
            )

            logger.info(f"Data-driven presentation created: {output_path}")
            return Path(presentation_result)

        except Exception as e:
            logger.error(f"Data-driven presentation creation failed: {e}")
            raise PresentationGenerationError(f"Failed to create data presentation: {e}")

    def create_quick_presentation(self, source: str, mode: str = "express",
                                 output_path: Optional[Union[str, Path]] = None) -> Path:
        """
        Create a presentation using quick/express mode (50-line approach).

        This method provides a simplified workflow similar to the DEV.to article,
        offering rapid presentation generation with minimal configuration.

        Args:
            source: Data source or repository path
            mode: Generation mode ("express", "standard", "comprehensive")
            output_path: Where to save the presentation

        Returns:
            Path to the created PowerPoint file
        """
        try:
            logger.info(f"Creating quick presentation in {mode} mode")

            if output_path is None:
                source_name = Path(source).stem if Path(source).exists() else "quick"
                output_path = Path(f"{source_name}_{mode}_presentation.pptx")
            else:
                output_path = Path(output_path)

            # Configure for quick mode
            quick_config = FrameworkConfig(
                max_slides=5 if mode == "express" else 8,
                max_points_per_slide=3 if mode == "express" else 5,
                enable_advanced_visuals=mode == "comprehensive",
                enable_image_generation=False,  # Quick mode - no AI images
                debug_mode=False
            )

            # Override current config temporarily
            original_config = self.config
            self.config = quick_config

            try:
                # Determine source type and create presentation
                if source.endswith('.zip'):
                    result = self.create_from_zip(source, str(output_path))
                elif any(source.endswith(ext) for ext in ['.csv', '.xlsx', '.xls']) or \
                     'spreadsheets' in source:
                    result = self.create_from_data_source(source, output_path)
                else:
                    raise ValueError(f"Unsupported source type: {source}")

                return result

            finally:
                # Restore original config
                self.config = original_config

        except Exception as e:
            logger.error(f"Quick presentation creation failed: {e}")
            raise PresentationGenerationError(f"Quick presentation failed: {e}")

    def create_with_composio_tools(self, data_source: str, 
                                  tools: Optional[List[str]] = None,
                                  output_path: Optional[Union[str, Path]] = None) -> Path:
        """
        Create presentation using Composio-style tool integration.

        This method mimics the Composio approach from the DEV.to article,
        integrating external tools and services for enhanced functionality.

        Args:
            data_source: Source for presentation data
            tools: List of Composio tools to use
            output_path: Where to save the presentation

        Returns:
            Path to the created PowerPoint file

        Note:
            This is a future enhancement placeholder. Full Composio integration
            requires additional dependencies and setup.
        """
        logger.warning("Composio integration not yet implemented. Using standard creation.")
        
        # For now, fall back to data-driven presentation
        return self.create_from_data_source(data_source, output_path)

    def get_data_source_info(self, source: str) -> dict:
        """
        Get information about a data source without creating presentation.

        Args:
            source: Data source path/URL

        Returns:
            Dictionary with source information
        """
        try:
            from data.google_sheets import DataSourceManager
            data_manager = DataSourceManager()
            
            if 'spreadsheets' in source:
                # Google Sheets
                sheet_id = data_manager._extract_sheet_id(source)
                from data.google_sheets import GoogleSheetsClient
                sheets_client = GoogleSheetsClient()
                return sheets_client.get_sheet_info(sheet_id)
            else:
                # File-based source
                import pandas as pd
                df = pd.read_csv(source) if source.endswith('.csv') else pd.read_excel(source)
                return {
                    'rows': len(df),
                    'columns': len(df.columns),
                    'column_names': df.columns.tolist(),
                    'data_types': df.dtypes.to_dict()
                }

        except Exception as e:
            logger.error(f"Failed to get data source info: {e}")
            return {'error': str(e)}

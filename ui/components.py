"""
UI components for the AI PowerPoint Framework Streamlit application.

This module provides reusable UI components and widgets for the web interface.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
import json

from core.config import FrameworkConfig
from core.constants import SUPPORTED_THEMES


class UIComponents:
    """Collection of reusable UI components."""
    
    @staticmethod
    def render_header(title: str, description: str = "") -> None:
        """
        Render application header with title and description.
        
        Args:
            title: Main title
            description: Optional description
        """
        st.title(f"🎯 {title}")
        if description:
            st.markdown(f"*{description}*")
        st.markdown("---")
    
    @staticmethod
    def render_config_sidebar() -> Dict[str, Any]:
        """
        Render configuration sidebar.
        
        Returns:
            Dict containing configuration values
        """
        with st.sidebar:
            st.header("⚙️ Configuration")
            
            # API Key input
            api_key = st.text_input(
                "Gemini API Key",
                type="password",
                help="Enter your Google Gemini API key"
            )
            
            # Theme selection
            theme = st.selectbox(
                "Design Theme",
                options=list(SUPPORTED_THEMES.keys()),
                format_func=lambda x: SUPPORTED_THEMES[x],
                help="Choose the design theme for your presentation"
            )
            
            # Advanced options
            with st.expander("Advanced Options"):
                max_slides = st.slider(
                    "Maximum Slides", 
                    min_value=5, 
                    max_value=20, 
                    value=10,
                    help="Maximum number of slides to generate"
                )
                
                max_points = st.slider(
                    "Max Points per Slide", 
                    min_value=3, 
                    max_value=10, 
                    value=6,
                    help="Maximum bullet points per slide"
                )
                
                enable_advanced = st.checkbox(
                    "Enable Advanced Visuals", 
                    value=True,
                    help="Enable advanced charts and visual elements"
                )
                
                use_com_engine = st.checkbox(
                    "Use COM Engine", 
                    value=False,
                    help="Use PowerPoint COM engine (Windows only)"
                )
                
                debug_mode = st.checkbox(
                    "Debug Mode", 
                    value=False,
                    help="Enable debug mode for detailed error messages"
                )
            
            return {
                'api_key': api_key,
                'theme': theme,
                'max_slides': max_slides,
                'max_points_per_slide': max_points,
                'enable_advanced_visuals': enable_advanced,
                'use_com_engine': use_com_engine,
                'debug_mode': debug_mode
            }
    
    @staticmethod
    def render_file_upload(
        label: str = "Upload Repository",
        file_types: Optional[List[str]] = None,
        help_text: str = ""
    ) -> Optional[Any]:
        """
        Render file upload component.
        
        Args:
            label: Upload section label
            file_types: Allowed file types
            help_text: Help text for the upload
            
        Returns:
            Uploaded file object or None
        """
        if file_types is None:
            file_types = ['zip']
        
        st.header(f"📁 {label}")
        
        uploaded_file = st.file_uploader(
            "Choose a ZIP file containing your repository",
            type=file_types,
            help=help_text or "Upload a ZIP file of your GitHub repository or project"
        )
        
        if uploaded_file is not None:
            st.success(f"✅ Uploaded: {uploaded_file.name}")
            
            # Show file details
            with st.expander("File Details"):
                st.write(f"**Name:** {uploaded_file.name}")
                st.write(f"**Size:** {uploaded_file.size:,} bytes")
                st.write(f"**Type:** {uploaded_file.type}")
        
        return uploaded_file
    
    @staticmethod
    def render_progress_section() -> Dict[str, Any]:
        """
        Render progress tracking section.
        
        Returns:
            Dict containing progress widgets
        """
        progress_container = st.container()
        
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Progress steps
            steps_container = st.container()
            
        return {
            'progress_bar': progress_bar,
            'status_text': status_text,
            'steps_container': steps_container,
            'progress_container': progress_container
        }
    
    @staticmethod
    def render_info_panel() -> None:
        """Render information panel with features and requirements."""
        st.header("ℹ️ About")
        st.markdown("""
        This tool automatically generates professional PowerPoint presentations 
        from your repository using AI analysis.
        
        **Features:**
        - 🤖 AI-powered content analysis
        - 🎨 Professional design themes
        - 📊 Smart visual layouts
        - 🔧 Customizable settings
        - 📈 Automatic chart generation
        - 🎯 Intelligent slide structuring
        
        **Supported repositories:**
        - Python projects
        - JavaScript/TypeScript projects
        - Documentation sites
        - General software projects
        - Open source repositories
        """)
        
        st.header("🔧 Requirements")
        st.markdown("""
        1. **Gemini API Key**: Get one from [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. **ZIP File**: Your repository as a ZIP archive
        3. **Internet Connection**: For AI analysis
        """)
        
        st.header("💡 Tips")
        st.markdown("""
        - Include a README.md file for better analysis
        - Ensure your repository has clear documentation
        - Use descriptive commit messages
        - Include examples or screenshots if available
        """)
    
    @staticmethod
    def render_results_section(result_path: str, original_filename: str) -> None:
        """
        Render results section with download button.
        
        Args:
            result_path: Path to generated presentation
            original_filename: Original ZIP filename
        """
        st.success("✅ Presentation generated successfully!")
        
        # Generate download filename
        download_filename = f"{Path(original_filename).stem}_presentation.pptx"
        
        # Download button
        with open(result_path, 'rb') as ppt_file:
            st.download_button(
                label="📥 Download Presentation",
                data=ppt_file.read(),
                file_name=download_filename,
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                help="Click to download your generated presentation"
            )
        
        # Show presentation info
        with st.expander("Presentation Details"):
            file_size = Path(result_path).stat().st_size
            st.write(f"**File Size:** {file_size:,} bytes")
            st.write(f"**Format:** PowerPoint (.pptx)")
            st.write(f"**Generated:** {Path(result_path).stat().st_mtime}")
    
    @staticmethod
    def render_error_section(error: Exception, debug_mode: bool = False) -> None:
        """
        Render error section with appropriate details.
        
        Args:
            error: Exception that occurred
            debug_mode: Whether to show debug details
        """
        st.error(f"❌ Error: {str(error)}")
        
        if debug_mode:
            with st.expander("Debug Information"):
                st.exception(error)
        
        # Helpful suggestions
        st.markdown("""
        **Troubleshooting:**
        - Check your API key is valid
        - Ensure the ZIP file is not corrupted
        - Try with a smaller repository
        - Check your internet connection
        """)
    
    @staticmethod
    def render_processing_steps(current_step: int, total_steps: int, 
                              step_descriptions: List[str]) -> None:
        """
        Render processing steps visualization.
        
        Args:
            current_step: Current step (0-indexed)
            total_steps: Total number of steps
            step_descriptions: List of step descriptions
        """
        st.markdown("### Processing Steps")
        
        for i, description in enumerate(step_descriptions):
            if i < current_step:
                st.markdown(f"✅ {description}")
            elif i == current_step:
                st.markdown(f"🔄 {description}")
            else:
                st.markdown(f"⏳ {description}")
        
        # Progress bar
        progress = (current_step + 1) / total_steps
        st.progress(progress)
    
    @staticmethod
    def render_metrics_dashboard(metrics: Dict[str, Any]) -> None:
        """
        Render metrics dashboard.
        
        Args:
            metrics: Dictionary of metrics to display
        """
        st.header("📊 Generation Metrics")
        
        cols = st.columns(len(metrics))
        
        for i, (key, value) in enumerate(metrics.items()):
            with cols[i]:
                st.metric(
                    label=key.replace('_', ' ').title(),
                    value=value
                )
    
    @staticmethod
    def render_preview_section(slide_data: List[Dict[str, Any]]) -> None:
        """
        Render slide preview section.
        
        Args:
            slide_data: List of slide data dictionaries
        """
        st.header("👁️ Slide Preview")
        
        for i, slide in enumerate(slide_data):
            with st.expander(f"Slide {i+1}: {slide.get('title', 'Untitled')}"):
                st.markdown(f"**Title:** {slide.get('title', 'Untitled')}")
                
                if 'points' in slide:
                    st.markdown("**Content:**")
                    for point in slide['points']:
                        st.markdown(f"- {point}")
                
                if 'slide_type' in slide:
                    st.markdown(f"**Type:** {slide['slide_type']}")
    
    @staticmethod
    def render_settings_export() -> None:
        """Render settings export/import functionality."""
        st.header("🔧 Settings Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Export Settings"):
                # Get current settings from session state
                settings = {
                    'theme': st.session_state.get('theme', 'corporate_modern'),
                    'max_slides': st.session_state.get('max_slides', 10),
                    'max_points_per_slide': st.session_state.get('max_points_per_slide', 6),
                    'enable_advanced_visuals': st.session_state.get('enable_advanced_visuals', True),
                    'use_com_engine': st.session_state.get('use_com_engine', False),
                    'debug_mode': st.session_state.get('debug_mode', False)
                }
                
                settings_json = json.dumps(settings, indent=2)
                st.download_button(
                    label="Download Settings",
                    data=settings_json,
                    file_name="ai_ppt_settings.json",
                    mime="application/json"
                )
        
        with col2:
            uploaded_settings = st.file_uploader(
                "Import Settings",
                type=['json'],
                help="Upload a settings JSON file"
            )
            
            if uploaded_settings is not None:
                try:
                    settings = json.loads(uploaded_settings.read())
                    
                    # Update session state
                    for key, value in settings.items():
                        st.session_state[key] = value
                    
                    st.success("Settings imported successfully!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Failed to import settings: {str(e)}")


class FormComponents:
    """Components for form-based input."""
    
    @staticmethod
    def render_manual_input_form() -> Optional[Dict[str, Any]]:
        """
        Render manual input form for direct content entry.
        
        Returns:
            Dict containing form data or None
        """
        with st.form("manual_input_form"):
            st.header("✍️ Manual Input")
            
            presentation_title = st.text_input(
                "Presentation Title",
                placeholder="Enter your presentation title"
            )
            
            presentation_description = st.text_area(
                "Description",
                placeholder="Describe your project or topic",
                height=100
            )
            
            # Slide content
            st.subheader("Slide Content")
            
            slides = []
            num_slides = st.number_input(
                "Number of Slides",
                min_value=1,
                max_value=10,
                value=5
            )
            
            for i in range(num_slides):
                st.markdown(f"**Slide {i+1}**")
                
                slide_title = st.text_input(
                    f"Title for Slide {i+1}",
                    key=f"slide_title_{i}"
                )
                
                slide_content = st.text_area(
                    f"Content for Slide {i+1}",
                    key=f"slide_content_{i}",
                    height=80
                )
                
                slides.append({
                    'title': slide_title,
                    'content': slide_content
                })
            
            submitted = st.form_submit_button("Generate Presentation")
            
            if submitted:
                return {
                    'presentation_title': presentation_title,
                    'description': presentation_description,
                    'slides': slides
                }
        
        return None
    
    @staticmethod
    def render_url_input_form() -> Optional[str]:
        """
        Render URL input form for GitHub repositories.
        
        Returns:
            URL string or None
        """
        with st.form("url_input_form"):
            st.header("🔗 GitHub Repository")
            
            repo_url = st.text_input(
                "Repository URL",
                placeholder="https://github.com/username/repository",
                help="Enter the URL of a public GitHub repository"
            )
            
            submitted = st.form_submit_button("Analyze Repository")
            
            if submitted and repo_url:
                return repo_url
        
        return None


class DialogComponents:
    """Components for dialog boxes and modals."""
    
    @staticmethod
    def show_confirmation_dialog(message: str, key: str) -> bool:
        """
        Show confirmation dialog.
        
        Args:
            message: Confirmation message
            key: Unique key for the dialog
            
        Returns:
            True if confirmed
        """
        if f"show_dialog_{key}" not in st.session_state:
            st.session_state[f"show_dialog_{key}"] = False
        
        if st.session_state[f"show_dialog_{key}"]:
            st.warning(message)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Yes", key=f"yes_{key}"):
                    st.session_state[f"show_dialog_{key}"] = False
                    st.session_state[f"confirmed_{key}"] = True
                    st.rerun()
            
            with col2:
                if st.button("No", key=f"no_{key}"):
                    st.session_state[f"show_dialog_{key}"] = False
                    st.session_state[f"confirmed_{key}"] = False
                    st.rerun()
            
            return False
        
        return st.session_state.get(f"confirmed_{key}", False)
    
    @staticmethod
    def show_info_dialog(title: str, content: str, key: str) -> None:
        """
        Show information dialog.
        
        Args:
            title: Dialog title
            content: Dialog content
            key: Unique key for the dialog
        """
        if f"show_info_{key}" not in st.session_state:
            st.session_state[f"show_info_{key}"] = False
        
        if st.session_state[f"show_info_{key}"]:
            st.info(f"**{title}**\n\n{content}")
            
            if st.button("OK", key=f"ok_{key}"):
                st.session_state[f"show_info_{key}"] = False
                st.rerun()


# Utility functions for component styling
def apply_custom_css():
    """Apply custom CSS styles to the Streamlit app."""
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-header {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)


def get_theme_colors(theme: str) -> Dict[str, str]:
    """
    Get color palette for a theme.
    
    Args:
        theme: Theme name
        
    Returns:
        Dict of color values
    """
    themes = {
        'corporate_modern': {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'accent': '#F18F01',
            'background': '#F8F9FA',
            'text': '#2C3E50'
        },
        'academic_formal': {
            'primary': '#1F4E79',
            'secondary': '#7F8C8D',
            'accent': '#E74C3C',
            'background': '#FFFFFF',
            'text': '#2C3E50'
        },
        'creative_vibrant': {
            'primary': '#FF6B6B',
            'secondary': '#4ECDC4',
            'accent': '#45B7D1',
            'background': '#F7F7F7',
            'text': '#2C3E50'
        }
    }
    
    return themes.get(theme, themes['corporate_modern'])

"""
Streamlit application interface for the AI PowerPoint Framework.

This module provides a web-based interface for generating presentations
using the framework's capabilities.
"""

import streamlit as st
import sys
import tempfile
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Add parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from framework import AIPresenterFramework
from core.config import FrameworkConfig


def run_streamlit_app():
    """
    Run the Streamlit web application.
    
    This function creates a web interface for the AI PowerPoint Framework,
    allowing users to upload ZIP files and generate presentations through
    a user-friendly web interface.
    """
    st.set_page_config(
        page_title="AI PowerPoint Generator",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🎯 AI PowerPoint Auto-Generator")
    st.markdown("---")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Check for environment API key
        config_temp = FrameworkConfig()
        env_api_key = config_temp.gemini_api_key
        env_openai_key = config_temp.openai_api_key
        
        # Gemini API Key
        if env_api_key:
            st.info("✅ Gemini API key found in environment")
            api_key = st.text_input(
                "Gemini API Key (Optional)",
                type="password",
                help="API key found in .env file. You can override it here.",
                placeholder="Using environment API key"
            )
            # Use environment key if no override provided
            if not api_key:
                api_key = env_api_key
        else:
            st.warning("⚠️ No Gemini API key found in environment")
            api_key = st.text_input(
                "Gemini API Key (Optional)",
                type="password",
                help="Enter your Google Gemini API key or add it to your .env file"
            )
        
        # OpenAI API Key for Enhanced Visuals
        if env_openai_key:
            st.info("✅ OpenAI API key found in environment")
            openai_key = st.text_input(
                "OpenAI API Key (Optional)",
                type="password",
                help="API key found in .env file. You can override it here.",
                placeholder="Using environment API key"
            )
            if not openai_key:
                openai_key = env_openai_key
        else:
            st.warning("⚠️ No OpenAI API key found")
            openai_key = st.text_input(
                "OpenAI API Key (Optional)",
                type="password",
                help="Enter your OpenAI API key for AI-generated visuals and backgrounds"
            )
        
        # Advanced options
        with st.expander("Advanced Options"):
            max_slides = st.slider("Max Slides", 5, 20, 10)
            max_points = st.slider("Max Points per Slide", 3, 10, 6)
            enable_advanced = st.checkbox("Enable Advanced Visuals", True)
            enable_ai_images = st.checkbox("Enable AI-Generated Images", bool(openai_key))
            
            # Multi-agent system option
            st.markdown("**🤖 AI Generation Mode:**")
            use_multi_agent = st.checkbox(
                "Use Multi-Agent AI System (Experimental)", 
                value=bool(openai_key),
                help="Use multiple specialized AI agents for enhanced quality. Requires OpenAI API key."
            )
            
            if use_multi_agent and not openai_key:
                st.warning("⚠️ Multi-agent system requires OpenAI API key")
                
            debug_mode = st.checkbox("Debug Mode", False)
        
        # Custom Theme & Prompt
        with st.expander("🎨 Custom Theme & Prompts"):
            st.markdown("**Customize your presentation theme and style:**")
            
            theme_style = st.selectbox(
                "Presentation Style",
                ["Professional Corporate", "Modern Tech", "Creative Startup", "Academic Research", "Custom"],
                help="Choose the overall style and tone for your presentation"
            )
            
            if theme_style == "Custom":
                custom_theme_prompt = st.text_area(
                    "Custom Theme Description",
                    placeholder="Describe your desired presentation theme, colors, and style...",
                    help="E.g., 'Dark theme with neon accents, futuristic tech vibes, cyberpunk aesthetic'"
                )
            else:
                custom_theme_prompt = None
            
            custom_content_prompt = st.text_area(
                "Additional Content Instructions",
                placeholder="Add specific instructions for content generation...",
                help="E.g., 'Focus on business impact and ROI', 'Emphasize technical innovation', 'Include market analysis'"
            )
            
            # Visual Enhancement Options
            st.markdown("**Visual Enhancements:**")
            col_vis1, col_vis2 = st.columns(2)
            with col_vis1:
                include_architecture = st.checkbox("Include Architecture Diagrams", True)
                include_roadmap = st.checkbox("Include Roadmap Visuals", True)
            with col_vis2:
                include_metrics = st.checkbox("Include Metrics Charts", True)
                include_backgrounds = st.checkbox("Custom AI Backgrounds", bool(openai_key))
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📁 Upload Content")
        
        # Input type selection
        input_type = st.selectbox(
            "Select Input Type",
            ["Repository (ZIP file)", "Data Source (Sheets/CSV/Excel)", "Quick Generation"],
            help="Choose the type of content to create presentation from"
        )
        
        if input_type == "Repository (ZIP file)":
            # File upload for repositories
            uploaded_file = st.file_uploader(
                "Choose a ZIP file containing your repository",
                type=['zip'],
                help="Upload a ZIP file of your GitHub repository or project"
            )
            
            if uploaded_file is not None:
                st.success(f"✅ Uploaded: {uploaded_file.name}")
                
                # Process button
                if st.button("🚀 Generate Presentation", type="primary"):
                    # Create configuration
                    config = FrameworkConfig(
                        gemini_api_key=api_key if api_key else None,
                        openai_api_key=openai_key if openai_key else None,
                        max_slides=max_slides,
                        max_points_per_slide=max_points,
                        enable_advanced_visuals=enable_advanced,
                        enable_image_generation=enable_ai_images,
                        debug_mode=debug_mode
                    )
                    _process_repository_upload(uploaded_file, config, use_multi_agent, custom_theme_prompt, custom_content_prompt, openai_key, api_key, enable_ai_images, debug_mode)
        
        elif input_type == "Data Source (Sheets/CSV/Excel)":
            # Data source input
            st.markdown("**📊 Data-Driven Presentation Generation**")
            st.markdown("Create presentations from data with automated charts and insights.")
            
            data_source_type = st.selectbox(
                "Data Source Type",
                ["Google Sheets", "CSV File", "Excel File"],
                help="Choose your data source type"
            )
            
            if data_source_type == "Google Sheets":
                sheet_input = st.text_input(
                    "Google Sheets URL or ID",
                    placeholder="https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit or just the ID",
                    help="Paste the Google Sheets URL or just the sheet ID"
                )
                
                # Optional sheet parameters
                with st.expander("Advanced Sheet Options"):
                    sheet_name = st.text_input("Specific Sheet Name (optional)", help="Leave empty to use first sheet")
                    range_name = st.text_input("Cell Range (optional)", help="e.g., A1:E10 - leave empty for all data")
                
                if sheet_input and st.button("📊 Generate Data Presentation", type="primary"):
                    # Create configuration
                    config = FrameworkConfig(
                        gemini_api_key=api_key if api_key else None,
                        openai_api_key=openai_key if openai_key else None,
                        max_slides=max_slides,
                        max_points_per_slide=max_points,
                        enable_advanced_visuals=enable_advanced,
                        enable_image_generation=enable_ai_images,
                        debug_mode=debug_mode
                    )
                    _process_data_source(sheet_input, "Google Sheets", config, debug_mode, 
                                       sheet_name=sheet_name if sheet_name else None,
                                       range_name=range_name if range_name else None)
            
            elif data_source_type in ["CSV File", "Excel File"]:
                file_types = ['csv'] if data_source_type == "CSV File" else ['xlsx', 'xls']
                uploaded_data_file = st.file_uploader(
                    f"Choose a {data_source_type}",
                    type=file_types,
                    help=f"Upload your {data_source_type.lower()}"
                )
                
                if uploaded_data_file is not None:
                    st.success(f"✅ Uploaded: {uploaded_data_file.name}")
                    
                    if st.button("📊 Generate Data Presentation", type="primary"):
                        # Create configuration
                        config = FrameworkConfig(
                            gemini_api_key=api_key if api_key else None,
                            openai_api_key=openai_key if openai_key else None,
                            max_slides=max_slides,
                            max_points_per_slide=max_points,
                            enable_advanced_visuals=enable_advanced,
                            enable_image_generation=enable_ai_images,
                            debug_mode=debug_mode
                        )
                        _process_uploaded_data_file(uploaded_data_file, config, debug_mode)
        
        elif input_type == "Quick Generation":
            # Quick generation mode
            st.markdown("**⚡ Quick Presentation Generation**")
            st.markdown("Rapid presentation creation with minimal configuration (inspired by 50-line approach).")
            
            quick_mode = st.selectbox(
                "Generation Mode",
                ["Express (5 slides)", "Standard (8 slides)", "Comprehensive (12 slides)"],
                help="Choose the complexity level for quick generation"
            )
            
            quick_source_type = st.selectbox(
                "Source Type",
                ["Repository ZIP", "Data File"],
                help="What type of source do you want to use?"
            )
            
            if quick_source_type == "Repository ZIP":
                quick_zip = st.file_uploader("ZIP File for Quick Analysis", type=['zip'])
                if quick_zip and st.button("⚡ Quick Generate", type="primary"):
                    # Create configuration
                    config = FrameworkConfig(
                        gemini_api_key=api_key if api_key else None,
                        openai_api_key=openai_key if openai_key else None,
                        max_slides=max_slides,
                        max_points_per_slide=max_points,
                        enable_advanced_visuals=enable_advanced,
                        enable_image_generation=enable_ai_images,
                        debug_mode=debug_mode
                    )
                    mode = quick_mode.split()[0].lower()  # "express", "standard", "comprehensive"
                    _process_quick_generation(quick_zip, mode, config, debug_mode)
            
            elif quick_source_type == "Data File":
                quick_data = st.file_uploader("Data File for Quick Analysis", type=['csv', 'xlsx', 'xls'])
                if quick_data and st.button("⚡ Quick Generate", type="primary"):
                    # Create configuration
                    config = FrameworkConfig(
                        gemini_api_key=api_key if api_key else None,
                        openai_api_key=openai_key if openai_key else None,
                        max_slides=max_slides,
                        max_points_per_slide=max_points,
                        enable_advanced_visuals=enable_advanced,
                        enable_image_generation=enable_ai_images,
                        debug_mode=debug_mode
                    )
                    mode = quick_mode.split()[0].lower()
                    _process_quick_data_generation(quick_data, mode, config, debug_mode)
    
    with col2:
        # st.header("ℹ️ About")
        # st.markdown("""
        # This tool automatically generates professional PowerPoint presentations 
        # from your repository using advanced AI analysis and visual generation.
        
        # **🚀 AI-Powered Features:**
        # - 🤖 **Multi-Agent AI System** - Specialized agents for content, design, diagrams, and QA
        # - 🧠 **Smart Content Analysis** - Deep repository understanding with ContentAnalyst
        # - 🎨 **AI-Generated Visuals** - Custom backgrounds, diagrams, and icons via DesignSpecialist
        # - � **Technical Diagrams** - Architecture and flowcharts from DiagramExpert
        # - ✏️ **Content Optimization** - Refined text and bullet points via ContentCurator
        # - 🔍 **Quality Assurance** - Multi-level quality review and improvement
        # - 🎯 **Custom Themes** - Adaptive color schemes based on your project
        # - 💬 **Custom Prompts** - Personalized content and styling instructions
        
        # **🎨 Visual Enhancements:**
        # - **Architecture Diagrams** - AI-generated system visualizations
        # - **Roadmap Graphics** - Timeline and milestone representations
        # - **Metrics Dashboards** - Professional data visualizations
        # - **Feature Icons** - Custom icons for key capabilities
        # - **Smart Backgrounds** - Theme-appropriate AI-generated backgrounds
        
        # **📁 Supported Projects:**
        # - Python (Flask, Django, FastAPI)
        # - JavaScript/TypeScript (React, Vue, Angular, Node.js)
        # - AI/ML projects and data science
        # - Web applications and APIs
        # - Mobile and desktop applications
        # - Documentation and research projects
        # """)
        
        st.header("Setup Requirements")
        st.markdown("""
        **Required:**
        1. **ZIP File** - Your repository as a ZIP archive
        2. **Internet Connection** - For AI analysis
        
        **Optional for Enhanced Features:**
        3. **Gemini API Key** - For AI content generation ([Get Here](https://aistudio.google.com/))
        4. **OpenAI API Key** - For AI-generated visuals ([Get Here](https://platform.openai.com/))
        
        **💡 Pro Tips:**
        - Add both API keys for full AI enhancement
        - Use custom prompts to tailor the presentation style
        - Enable debug mode to see generation details
        - Try different presentation styles for variety
        """)
        
        # API Key Status
        config_check = FrameworkConfig()
        st.header("🔑 API Status")
        
        col_status1, col_status2 = st.columns(2)
        with col_status1:
            if config_check.gemini_api_key:
                st.success("✅ Gemini API Ready")
            else:
                st.warning("⚠️ Gemini API Missing")
        
        with col_status2:
            if config_check.openai_api_key and config_check.openai_api_key != "your_openai_api_key_here":
                st.success("✅ OpenAI API Ready")
            else:
                st.warning("⚠️ OpenAI API Missing")


def _process_repository_upload(uploaded_file, config, use_multi_agent, custom_theme_prompt, 
                              custom_content_prompt, openai_key, api_key, enable_ai_images, debug_mode):
    """Process repository ZIP file upload and generate presentation"""
    try:
        # Initialize framework
        framework = AIPresenterFramework(config)
        
        # Show warnings for missing API keys
        if not api_key:
            st.warning("⚠️ No Gemini API key provided. Using fallback content generation.")
        if not openai_key and enable_ai_images:
            st.warning("⚠️ No OpenAI API key provided. AI-generated images will be disabled.")
        if openai_key and enable_ai_images:
            st.info("✨ AI-generated visuals enabled! This will create custom backgrounds and diagrams.")
        
        # Multi-agent system info
        if use_multi_agent and openai_key:
            st.info("🤖 Multi-agent AI system enabled! Using specialized agents for enhanced quality.")
        elif use_multi_agent and not openai_key:
            st.warning("⚠️ Multi-agent system disabled due to missing OpenAI API key.")
        
        # Create progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_zip_path = tmp_file.name
        
        try:
            # Update progress
            progress_bar.progress(20)
            status_text.text("📊 Analyzing repository content...")
            
            # Generate presentation
            progress_bar.progress(50)
            if use_multi_agent and openai_key:
                status_text.text("🤖 Multi-agent AI system creating presentation...")
                
                result_path = framework.create_from_zip_with_agents(
                    temp_zip_path,
                    use_multi_agent=True,
                    custom_theme_prompt=custom_theme_prompt,
                    custom_content_prompt=custom_content_prompt if custom_content_prompt else None
                )
            else:
                status_text.text("🎨 Creating presentation...")
                
                result_path = framework.create_from_zip(
                    temp_zip_path,
                    custom_theme_prompt=custom_theme_prompt,
                    custom_content_prompt=custom_content_prompt if custom_content_prompt else None
                )
            
            # Debug: Check the generated file
            if debug_mode:
                st.write(f"Debug: Generated file path: {result_path}")
                st.write(f"Debug: File exists: {Path(result_path).exists()}")
                st.write(f"Debug: File size: {Path(result_path).stat().st_size} bytes")
                
                # Check slide count
                try:
                    from pptx import Presentation
                    prs = Presentation(str(result_path))
                    st.write(f"Debug: Slide count: {len(prs.slides)}")
                except Exception as e:
                    st.write(f"Debug: Error checking slides: {e}")
            
            # Completion
            progress_bar.progress(100)
            status_text.text("✅ Presentation generated successfully!")
            
            # Provide download link
            with open(result_path, 'rb') as ppt_file:
                st.download_button(
                    label="📥 Download Presentation",
                    data=ppt_file.read(),
                    file_name=f"{Path(uploaded_file.name).stem}_presentation.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )
            
        finally:
            # Cleanup
            Path(temp_zip_path).unlink(missing_ok=True)
            
    except Exception as e:
        st.error(f"❌ Error generating presentation: {str(e)}")
        if debug_mode:
            st.exception(e)


def _process_data_source(data_source, source_type, config, debug_mode, **kwargs):
    """Process data source and generate data-driven presentation"""
    try:
        # Initialize framework
        framework = AIPresenterFramework(config)
        
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Analyze data source
        progress_bar.progress(20)
        status_text.text(f"📊 Analyzing {source_type} data...")
        
        # Generate presentation
        progress_bar.progress(50)
        status_text.text("📈 Creating data-driven presentation...")
        
        result_path = framework.create_from_data_source(
            data_source,
            presentation_title=f"{source_type} Data Analysis",
            **kwargs
        )
        
        # Debug info
        if debug_mode:
            st.write(f"Debug: Data source: {data_source}")
            st.write(f"Debug: Generated file path: {result_path}")
            st.write(f"Debug: File exists: {Path(result_path).exists()}")
        
        # Completion
        progress_bar.progress(100)
        status_text.text("✅ Data presentation generated successfully!")
        
        # Download link
        with open(result_path, 'rb') as ppt_file:
            st.download_button(
                label="📥 Download Data Presentation",
                data=ppt_file.read(),
                file_name=f"data_analysis_presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
        
    except Exception as e:
        st.error(f"❌ Error generating data presentation: {str(e)}")
        if debug_mode:
            st.exception(e)


def _process_uploaded_data_file(uploaded_file, config, debug_mode):
    """Process uploaded data file and generate presentation"""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{uploaded_file.name.split(".")[-1]}') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_file_path = tmp_file.name
        
        try:
            _process_data_source(temp_file_path, uploaded_file.type, config, debug_mode)
        finally:
            # Cleanup
            Path(temp_file_path).unlink(missing_ok=True)
            
    except Exception as e:
        st.error(f"❌ Error processing uploaded file: {str(e)}")
        if debug_mode:
            st.exception(e)


def _process_quick_generation(uploaded_file, mode, config, debug_mode):
    """Process quick generation for repository ZIP"""
    try:
        # Initialize framework
        framework = AIPresenterFramework(config)
        
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_zip_path = tmp_file.name
        
        try:
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            progress_bar.progress(30)
            status_text.text(f"⚡ Quick generation ({mode} mode)...")
            
            # Use quick generation method
            result_path = framework.create_quick_presentation(
                temp_zip_path,
                mode=mode
            )
            
            progress_bar.progress(100)
            status_text.text("✅ Quick presentation generated!")
            
            # Download link
            with open(result_path, 'rb') as ppt_file:
                st.download_button(
                    label="📥 Download Quick Presentation",
                    data=ppt_file.read(),
                    file_name=f"quick_{mode}_presentation.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )
        finally:
            Path(temp_zip_path).unlink(missing_ok=True)
            
    except Exception as e:
        st.error(f"❌ Quick generation failed: {str(e)}")
        if debug_mode:
            st.exception(e)


def _process_quick_data_generation(uploaded_file, mode, config, debug_mode):
    """Process quick generation for data files"""
    try:
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{uploaded_file.name.split(".")[-1]}') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_file_path = tmp_file.name
        
        try:
            # Initialize framework
            framework = AIPresenterFramework(config)
            
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            progress_bar.progress(30)
            status_text.text(f"⚡ Quick data analysis ({mode} mode)...")
            
            # Use quick generation method
            result_path = framework.create_quick_presentation(
                temp_file_path,
                mode=mode
            )
            
            progress_bar.progress(100)
            status_text.text("✅ Quick data presentation generated!")
            
            # Download link
            with open(result_path, 'rb') as ppt_file:
                st.download_button(
                    label="📥 Download Quick Data Presentation",
                    data=ppt_file.read(),
                    file_name=f"quick_data_{mode}_presentation.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )
        finally:
            Path(temp_file_path).unlink(missing_ok=True)
            
    except Exception as e:
        st.error(f"❌ Quick data generation failed: {str(e)}")
        if debug_mode:
            st.exception(e)


if __name__ == "__main__":
    run_streamlit_app()

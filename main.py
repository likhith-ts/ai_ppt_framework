"""
Main entry point for the AI PowerPoint Framework.

This module provides a clean interface to run the Streamlit application
using the new modular architecture while maintaining full compatibility
with the original functionality.
"""

import sys
from pathlib import Path

# Add the framework to the Python path
framework_path = Path(__file__).parent
print(framework_path)
sys.path.insert(0, str(framework_path))


def main():
    """
    Main entry point for the AI PowerPoint Framework.

    This function initializes the framework and starts the Streamlit application
    with all the modular components properly configured.
    """
    try:
        # Import and validate core components
        print("🔍 Importing core components...")
        from core.config import validate_environment
        print("🔍 Importing streamlit_app components...")
        from ui.streamlit_app import run_streamlit_app


        # Validate environment and dependencies
        print("🔧 Validating environment...")
        validate_environment()
        print("✅ Environment validation complete")

        # Start the Streamlit application
        print("🚀 Starting AI PowerPoint Framework...")
        run_streamlit_app()

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install streamlit google-generativeai python-pptx python-dotenv")
        sys.exit(1)

    except Exception as e:
        print(f"❌ Framework initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

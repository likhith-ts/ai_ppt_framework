# 🔌 AI PowerPoint Framework - API Reference

## Core Classes and Functions

### AIPresenterFramework

The main framework class that orchestrates presentation generation.

```python
class AIPresenterFramework:
    def __init__(self, config: FrameworkConfig = None)
    def create_from_zip(self, zip_path: str, output_dir: str = None) -> str
    def create_from_directory(self, directory_path: str, output_dir: str = None) -> str
    def create_from_content(self, content: str, output_dir: str = None) -> str
```

#### Methods

##### `create_from_zip(zip_path, output_dir=None)`

Generate a presentation from a ZIP file containing a repository.

**Parameters:**

- `zip_path` (str): Path to the ZIP file
- `output_dir` (str, optional): Output directory for the presentation

**Returns:**

- `str`: Path to the generated presentation file

**Example:**

```python
framework = AIPresenterFramework()
presentation_path = framework.create_from_zip("my_repo.zip")
```

##### `create_from_directory(directory_path, output_dir=None)`

Generate a presentation from a directory containing a repository.

**Parameters:**

- `directory_path` (str): Path to the repository directory
- `output_dir` (str, optional): Output directory for the presentation

**Returns:**

- `str`: Path to the generated presentation file

**Example:**

```python
framework = AIPresenterFramework()
presentation_path = framework.create_from_directory("./my_project")
```

---

## Configuration

### FrameworkConfig

Central configuration class for the framework.

```python
@dataclass
class FrameworkConfig:
    gemini_api_key: str = None
    max_retries: int = 3
    retry_delay: float = 1.0
    temp_dir: str = None
    output_dir: str = None
    enable_com_powerpoint: bool = True
    enable_python_pptx_fallback: bool = True
    enable_advanced_visuals: bool = True
    enable_smartart: bool = True
    enable_custom_backgrounds: bool = True
    max_slides: int = 10
    max_points_per_slide: int = 6
    max_content_length: int = 50000
    debug_mode: bool = False
    enable_caching: bool = True
    parallel_processing: bool = False
```

#### Class Methods

##### `from_env()`

Create configuration from environment variables.

**Returns:**

- `FrameworkConfig`: Configuration instance

**Example:**

```python
config = FrameworkConfig.from_env()
framework = AIPresenterFramework(config)
```

---

## Design System

### DesignTheme

Enumeration of available design themes.

```python
class DesignTheme(Enum):
    CORPORATE_MODERN = "corporate_modern"
    CREATIVE_GRADIENT = "creative_gradient"
    MINIMALIST_LUXURY = "minimalist_luxury"
    TECH_INNOVATION = "tech_innovation"
    ADOBE_INSPIRED = "adobe_inspired"
    BEHANCE_STYLE = "behance_style"
```

### ColorPalette

Industry-grade color palette with psychological impact.

```python
@dataclass
class ColorPalette:
    primary: int
    secondary: int
    accent: int
    background: int
    text_primary: int
    text_secondary: int
    success: int
    warning: int
    gradient_start: int
    gradient_end: int
```

#### Methods

##### `get_harmony_colors(base_color, harmony_type="complementary")`

Generate harmonious colors using color theory.

**Parameters:**

- `base_color` (int): Base color as RGB integer
- `harmony_type` (str): Type of harmony ("complementary", "triadic", "analogous")

**Returns:**

- `List[int]`: List of harmonious colors

**Example:**

```python
colors = ColorPalette.get_harmony_colors(0x3498DB, "triadic")
```

### DesignPalettes

Collection of pre-defined color palettes.

#### Class Methods

##### `get_palette(theme)`

Get the color palette for a specific design theme.

**Parameters:**

- `theme` (DesignTheme): The design theme

**Returns:**

- `ColorPalette`: Complete color palette for the theme

**Example:**

```python
palette = DesignPalettes.get_palette(DesignTheme.CORPORATE_MODERN)
```

---

## Theme Selection

### ThemeSelector

Intelligent theme selection based on content analysis.

#### Static Methods

##### `select_theme_by_keywords(content)`

Select a theme based on keywords found in the content.

**Parameters:**

- `content` (str): Content to analyze

**Returns:**

- `DesignTheme`: Most appropriate theme

**Example:**

```python
theme = ThemeSelector.select_theme_by_keywords("python machine learning AI")
# Returns: DesignTheme.TECH_INNOVATION
```

##### `select_theme_by_file_types(file_extensions)`

Select a theme based on file types in the repository.

**Parameters:**

- `file_extensions` (List[str]): List of file extensions

**Returns:**

- `DesignTheme`: Most appropriate theme

**Example:**

```python
theme = ThemeSelector.select_theme_by_file_types([".py", ".js", ".md"])
# Returns: DesignTheme.TECH_INNOVATION
```

---

## Constants and Layout

### Layout Constants

```python
class LayoutConstants:
    SLIDE = {
        'width': 960,
        'height': 540,
        'aspect_ratio': 16/9
    }
    
    MARGINS = {
        'small': 24,
        'medium': 40,
        'large': 64
    }
    
    SPACING = {
        'unit': 8,
        'gutter': 16,
        'component': 32
    }
```

### Typography Constants

```python
class TypographyConstants:
    SIZES = {
        'giant': 48,
        'large': 36,
        'title': 32,
        'subtitle': 24,
        'body': 18,
        'caption': 14,
        'small': 12
    }
    
    FAMILIES = {
        'primary': 'Calibri',
        'secondary': 'Arial',
        'monospace': 'Consolas',
        'serif': 'Times New Roman'
    }
```

---

## Error Handling

### Exception Hierarchy

```python
FrameworkError
├── ConfigurationError
├── AIClientError
├── PresentationGenerationError
├── SlideBuilderError
├── DesignSystemError
├── FileHandlingError
├── ContentAnalysisError
├── ValidationError
└── DependencyError
```

#### Base Exception

```python
class FrameworkError(Exception):
    def __init__(self, message: str, error_code: str = None, context: dict = None)
```

**Attributes:**

- `message` (str): Human-readable error message
- `error_code` (str): Machine-readable error code
- `context` (dict): Additional context information

**Example:**

```python
try:
    framework = AIPresenterFramework()
    result = framework.create_from_zip("repo.zip")
except FrameworkError as e:
    print(f"Error: {e.message}")
    print(f"Code: {e.error_code}")
    print(f"Context: {e.context}")
```

---

## Utility Functions

### Color Utilities

```python
class ColorUtilities:
    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]
    
    @staticmethod
    def int_to_rgb(color_int: int) -> Tuple[int, int, int]
    
    @staticmethod
    def rgb_to_int(r: int, g: int, b: int) -> int
    
    @staticmethod
    def is_dark_color(color: int, threshold: float = 0.5) -> bool
    
    @staticmethod
    def get_readable_text_color(background_color: int) -> int
```

### Layout Utilities

```python
def get_responsive_font_size(base_size: int, scale_factor: float = 1.0) -> int
def get_grid_width(columns: int, total_columns: int = 12) -> int
def get_vertical_rhythm(lines: int) -> int
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | *Required* | Google Gemini API key |
| `AI_PPT_MAX_RETRIES` | `3` | Maximum API retry attempts |
| `AI_PPT_RETRY_DELAY` | `1.0` | Delay between retries (seconds) |
| `AI_PPT_TEMP_DIR` | System temp | Temporary file directory |
| `AI_PPT_OUTPUT_DIR` | System temp | Output directory |
| `AI_PPT_ENABLE_COM` | `true` | Enable COM-based PowerPoint |
| `AI_PPT_ADVANCED_VISUALS` | `true` | Enable advanced visual elements |
| `AI_PPT_MAX_SLIDES` | `10` | Maximum slides per presentation |
| `AI_PPT_MAX_POINTS` | `6` | Maximum points per slide |
| `AI_PPT_DEBUG` | `false` | Enable debug mode |

---

## Extension Points

### Custom Slide Builders

```python
from ai_ppt_framework.presentation.slide_builders.base_builder import BaseSlideBuilder

class CustomSlideBuilder(BaseSlideBuilder):
    def build(self, slide_data: dict) -> object:
        """Custom slide implementation"""
        # Your custom slide logic here
        return self.create_custom_layout(slide_data)
    
    def supports_slide_type(self, slide_type: str) -> bool:
        return slide_type == "custom_slide"
```

### Custom Themes

```python
from ai_ppt_framework.design.color_system import ColorPalette
from ai_ppt_framework.design.themes import DesignTheme

# Extend the enum (in your custom module)
class CustomTheme:
    SPACE_MODERN = "space_modern"

# Create custom palette
SPACE_MODERN_PALETTE = ColorPalette(
    primary=0x1a1a2e,
    secondary=0x16213e,
    accent=0x0f3460,
    background=0x0e0e23,
    text_primary=0xffffff,
    text_secondary=0xb0bec5,
    success=0x00d4aa,
    warning=0xff9800,
    gradient_start=0x1a1a2e,
    gradient_end=0x0f3460
)
```

### Custom AI Providers

```python
from ai_ppt_framework.ai.base_client import BaseAIClient

class OpenAIClient(BaseAIClient):
    def analyze_repository(self, content: str) -> dict:
        """Custom AI implementation using OpenAI"""
        # Your OpenAI integration here
        pass
```

---

## Performance Optimization

### Caching

The framework includes intelligent caching for AI responses:

```python
# Enable caching (default)
config = FrameworkConfig(enable_caching=True)

# Disable caching for always-fresh results
config = FrameworkConfig(enable_caching=False)
```

### Parallel Processing

```python
# Enable parallel processing for multi-slide generation
config = FrameworkConfig(parallel_processing=True)
```

### Memory Management

```python
# Limit content length for large repositories
config = FrameworkConfig(max_content_length=25000)  # 25KB limit
```

---

## Examples

### Basic Usage

```python
from ai_ppt_framework import AIPresenterFramework

# Simple presentation generation
framework = AIPresenterFramework()
presentation_path = framework.create_from_zip("repository.zip")
print(f"Presentation created: {presentation_path}")
```

### Advanced Configuration

```python
from ai_ppt_framework import AIPresenterFramework
from ai_ppt_framework.core.config import FrameworkConfig
from ai_ppt_framework.design.themes import DesignTheme

# Custom configuration
config = FrameworkConfig(
    gemini_api_key="your_api_key",
    max_slides=15,
    enable_advanced_visuals=True,
    debug_mode=True,
    output_dir="./presentations"
)

framework = AIPresenterFramework(config)
presentation_path = framework.create_from_directory("./my_project")
```

### Batch Processing

```python
import os
from ai_ppt_framework import AIPresenterFramework

def process_repositories(repo_dir: str):
    framework = AIPresenterFramework()
    
    for filename in os.listdir(repo_dir):
        if filename.endswith('.zip'):
            repo_path = os.path.join(repo_dir, filename)
            try:
                ppt_path = framework.create_from_zip(repo_path)
                print(f"✅ Created: {ppt_path}")
            except Exception as e:
                print(f"❌ Failed {filename}: {e}")

process_repositories("./repositories")
```

### Custom Theme Selection

```python
from ai_ppt_framework.design.themes import ThemeSelector, DesignTheme

# Analyze content for theme selection
content = "This is a machine learning project using Python and TensorFlow"
recommended_theme = ThemeSelector.select_theme_by_keywords(content)
print(f"Recommended theme: {recommended_theme}")
# Output: DesignTheme.TECH_INNOVATION
```

---

## Migration from Monolithic Code

### Before (smartArt.py)

```python
# Old monolithic approach
from smartArt import (
    create_extraordinary_powerpoint_presentation,
    parse_github_multiSlide_response,
    analyze_with_gemini_with_retry,
    extract_zip_contents
)

# Complex multi-step process
content = extract_zip_contents(zip_file)
analysis = analyze_with_gemini_with_retry(content)
slides_data = parse_github_multiSlide_response(analysis)
ppt_path = create_extraordinary_powerpoint_presentation(slides_data)
```

### After (Framework)

```python
# New modular approach
from ai_ppt_framework import AIPresenterFramework

# Simple one-line solution
framework = AIPresenterFramework()
ppt_path = framework.create_from_zip("repository.zip")
```

This maintains 100% functionality while providing a much cleaner, more maintainable interface.

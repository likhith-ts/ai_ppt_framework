"""
Content analyzer for extracting and processing repository content.

This module provides advanced analysis of GitHub repositories, including
technology stack detection, project complexity assessment, and content
categorization for presentation generation.
"""

import zipfile
import tempfile
import os
from typing import List, Dict, Optional, Union
from pathlib import Path

from core.exceptions import ContentAnalysisError


class ContentAnalyzer:
    """
    Advanced repository content analyzer for AI PowerPoint generation.

    Features:
    - Technology stack detection
    - Project complexity assessment
    - File structure analysis
    - Code quality metrics
    - Business impact evaluation
    """

    # Technology detection patterns
    TECH_INDICATORS = {
        "Python": [
            ".py",
            "requirements.txt",
            "setup.py",
            "pyproject.toml",
            "pip",
            "python",
        ],
        "JavaScript": [".js", ".jsx", "package.json", "node_modules", "npm", "yarn"],
        "TypeScript": [".ts", ".tsx", "tsconfig.json", "typescript"],
        "React": ["react", "jsx", "component", "@react"],
        "Vue": ["vue", ".vue", "vuejs"],
        "Angular": ["angular", "@angular", "ng"],
        "Django": ["django", "settings.py", "models.py", "urls.py"],
        "Flask": ["flask", "app.py", "@app.route"],
        "FastAPI": ["fastapi", "main.py", "uvicorn"],
        "Express": ["express", "server.js", "app.js"],
        "Node.js": ["express", "server.js", "app.js", "nodejs"],
        "Docker": ["Dockerfile", "docker-compose", ".dockerignore"],
        "Git": [".git", ".gitignore", "README.md"],
        "Streamlit": ["streamlit", "st.", ".streamlit"],
        "PowerPoint": ["powerpoint", "pptx", "win32com"],
        "AI/ML": [
            "tensorflow",
            "pytorch",
            "scikit",
            "pandas",
            "numpy",
            "keras",
            "gemini",
            "openai",
        ],
        "Database": ["sqlite", "postgresql", "mysql", "mongodb", "redis"],
        "Cloud": ["aws", "azure", "gcp", "heroku", "vercel", "netlify"],
    }

    # File extensions to analyze
    CODE_EXTENSIONS = {
        ".py",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".java",
        ".cpp",
        ".c",
        ".cs",
        ".php",
        ".rb",
        ".go",
        ".rs",
        ".swift",
        ".kt",
        ".scala",
        ".r",
        ".m",
    }

    def __init__(self):
        """Initialize the content analyzer."""
        self.reset()

    def reset(self) -> None:
        """Reset analyzer state for new analysis."""
        self.files = []
        self.content = ""
        self.tech_stack = {}
        self.metrics = {}

    def extract_zip_contents(self, uploaded_file) -> str:
        """
        Extract and analyze contents from uploaded ZIP file.

        Args:
            uploaded_file: Streamlit uploaded file object

        Returns:
            Concatenated text content of all files

        Raises:
            ContentAnalysisError: If ZIP extraction fails
        """
        extracted_texts = []

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        try:
            with zipfile.ZipFile(tmp_path, "r") as zip_ref:
                for file_name in zip_ref.namelist():
                    if not file_name.endswith("/"):  # Skip directories
                        try:
                            with zip_ref.open(file_name) as file:
                                content = file.read().decode("utf-8", errors="ignore")
                                extracted_texts.append(
                                    f"File: {file_name}\n\n{content}"
                                )
                                self.files.append(file_name)
                        except Exception:
                            # Skip files that can't be decoded
                            continue
        except zipfile.BadZipFile:
            raise ContentAnalysisError("Invalid ZIP file format")
        except Exception as e:
            raise ContentAnalysisError(f"Failed to extract ZIP contents: {str(e)}")
        finally:
            os.unlink(tmp_path)

        self.content = "\n\n".join(extracted_texts)
        return self.content

    def extract_zip_contents_from_path(self, zip_path: Union[str, Path]) -> str:
        """
        Extract and analyze contents from ZIP file path.

        Args:
            zip_path: Path to ZIP file

        Returns:
            Concatenated text content of all files

        Raises:
            ContentAnalysisError: If ZIP extraction fails
        """
        from utils.file_handler import ZipExtractor

        extracted_texts = []

        try:
            extractor = ZipExtractor()
            extraction_results = extractor.extract_zip(zip_path)

            extract_path = Path(extraction_results["extract_path"])

            # Process extracted files
            for file_info in extraction_results["files"]:
                file_path = Path(file_info["path"])

                # Skip if file doesn't exist or is a directory
                if not file_path.exists() or file_path.is_dir():
                    continue

                # Check if it's a text file we can process
                if (
                    file_path.suffix.lower() in self.CODE_EXTENSIONS
                    or file_path.suffix.lower()
                    in [
                        ".txt",
                        ".md",
                        ".rst",
                        ".json",
                        ".xml",
                        ".yml",
                        ".yaml",
                        ".cfg",
                        ".ini",
                        ".toml",
                    ]
                ):
                    try:
                        with open(
                            file_path, "r", encoding="utf-8", errors="ignore"
                        ) as f:
                            content = f.read()
                            extracted_texts.append(
                                f"File: {file_info['name']}\n\n{content}"
                            )
                            self.files.append(file_info["name"])
                    except Exception:
                        # Skip files that can't be read
                        continue

            self.content = "\n\n".join(extracted_texts)
            return self.content

        except Exception as e:
            raise ContentAnalysisError(f"Failed to extract ZIP contents from path: {str(e)}")

    def analyze_project(self, content: Optional[str] = None) -> Dict:
        """
        Perform comprehensive project analysis.

        Args:
            content: Content to analyze. If None, uses previously extracted content.

        Returns:
            Comprehensive analysis results
        """
        if content:
            self.content = content

        if not self.content:
            raise ContentAnalysisError("No content to analyze")

        analysis = {
            "technology_stack": self._detect_technologies(),
            "project_type": self._determine_project_type(),
            "complexity": self._assess_complexity(),
            "maturity": self._assess_maturity(),
            "file_metrics": self._calculate_file_metrics(),
            "code_quality": self._assess_code_quality(),
            "business_impact": self._assess_business_impact(),
        }

        self.metrics = analysis
        return analysis

    def _detect_technologies(self) -> Dict[str, int]:
        """Detect technologies used in the project."""
        detected_techs = {}
        content_lower = self.content.lower()

        for tech, indicators in self.TECH_INDICATORS.items():
            matches = sum(
                1 for indicator in indicators if indicator.lower() in content_lower
            )
            if matches > 0:
                detected_techs[tech] = matches

        # Sort by relevance (number of matches)
        return dict(sorted(detected_techs.items(), key=lambda x: x[1], reverse=True))

    def _determine_project_type(self) -> str:
        """Determine the primary project type based on technologies."""
        tech_stack = self.tech_stack or self._detect_technologies()

        if "Streamlit" in tech_stack and "AI/ML" in tech_stack:
            return "AI-Powered Web Application"
        elif "React" in tech_stack or "Vue" in tech_stack:
            return "Frontend Web Application"
        elif "Django" in tech_stack or "Flask" in tech_stack:
            return "Backend Web Service"
        elif "AI/ML" in tech_stack:
            return "Machine Learning Project"
        elif "Docker" in tech_stack:
            return "Containerized Application"
        elif "Node.js" in tech_stack or "Express" in tech_stack:
            return "Node.js Application"
        else:
            return "Software Application"

    def _assess_complexity(self) -> str:
        """Assess project complexity based on size and structure."""
        file_count = len(self.files)
        code_lines = len(
            [
                line
                for line in self.content.split("\n")
                if line.strip() and not line.strip().startswith("#")
            ]
        )

        if file_count > 20 and code_lines > 1000:
            return "Enterprise-grade"
        elif file_count > 10 and code_lines > 500:
            return "Professional"
        elif file_count > 5:
            return "Moderate"
        else:
            return "Simple"

    def _assess_maturity(self) -> str:
        """Assess project maturity based on structure and practices."""
        has_tests = any("test" in file.lower() for file in self.files)
        has_docs = any(
            "readme" in file.lower() or "doc" in file.lower() for file in self.files
        )
        has_config = any(
            file in ["requirements.txt", "package.json", "setup.py", "Dockerfile"]
            for file in self.files
        )

        complexity = self._assess_complexity()

        if complexity == "Enterprise-grade" and has_tests and has_docs and has_config:
            return "Production-ready"
        elif complexity in ["Professional", "Enterprise-grade"] and has_config:
            return "Production-capable"
        elif has_config or has_docs:
            return "Development-stage"
        else:
            return "Prototype/MVP"

    def _calculate_file_metrics(self) -> Dict[str, int]:
        """Calculate basic file and content metrics."""
        lines = self.content.split("\n")

        return {
            "total_files": len(self.files),
            "total_lines": len(lines),
            "code_files": len(
                [f for f in self.files if Path(f).suffix in self.CODE_EXTENSIONS]
            ),
            "non_empty_lines": len([line for line in lines if line.strip()]),
            "comment_lines": len(
                [line for line in lines if line.strip().startswith("#")]
            ),
        }

    def _assess_code_quality(self) -> Dict[str, str]:
        """Assess code quality indicators."""
        metrics = self._calculate_file_metrics()

        # Basic quality indicators
        has_structure = len(self.files) > 3
        has_docs = any("readme" in file.lower() for file in self.files)
        has_tests = any("test" in file.lower() for file in self.files)

        comment_ratio = (
            metrics["comment_lines"] / metrics["non_empty_lines"] * 100
            if metrics["non_empty_lines"] > 0
            else 0
        )

        return {
            "organization": "Well-structured" if has_structure else "Basic structure",
            "documentation": "Comprehensive" if has_docs else "Limited",
            "testing": "Test coverage included" if has_tests else "No visible tests",
            "comment_density": f"{comment_ratio:.1f}% commented",
            "maintainability": "High" if has_structure and has_docs else "Moderate",
        }

    def _assess_business_impact(self) -> Dict[str, str]:
        """Assess potential business impact and market value."""
        tech_stack = self._detect_technologies()
        complexity = self._assess_complexity()
        project_type = self._determine_project_type()

        # Determine market potential based on technology and complexity
        if "AI/ML" in tech_stack:
            market_potential = "High - AI/ML solutions in high demand"
        elif complexity in ["Enterprise-grade", "Professional"]:
            market_potential = "Medium-High - Professional-grade solution"
        else:
            market_potential = "Medium - Solid technical foundation"

        return {
            "value_proposition": f"Solves real-world problems using {project_type.lower()}",
            "market_potential": market_potential,
            "technical_advantage": f"Built with modern {list(tech_stack.keys())[0] if tech_stack else 'technology'} stack",
            "scalability": complexity + " architecture supporting growth",
            "innovation_factor": "High" if "AI/ML" in tech_stack else "Medium",
        }

    def get_primary_technologies(self, limit: int = 3) -> List[str]:
        """Get the primary technologies used in the project."""
        tech_stack = self.tech_stack or self._detect_technologies()
        return list(tech_stack.keys())[:limit]

    def get_analysis_summary(self) -> str:
        """Get a concise summary of the analysis results."""
        if not self.metrics:
            return "No analysis performed yet"

        primary_techs = ", ".join(self.get_primary_technologies())

        return (
            f"{self.metrics['project_type']} built with {primary_techs}. "
            f"{self.metrics['complexity']} complexity, {self.metrics['maturity']} maturity. "
            f"{self.metrics['file_metrics']['total_files']} files analyzed."
        )

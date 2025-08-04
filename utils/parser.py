"""
Response parsing and content extraction utilities.

This module provides intelligent parsing of AI responses, content extraction,
and structured data processing for the presentation framework.
"""

import re
import json
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum

from core.exceptions import ValidationError


class ContentType(Enum):
    """Types of content that can be parsed."""
    
    SLIDE_CONTENT = "slide_content"
    BULLET_POINTS = "bullet_points"
    TITLE_SUBTITLE = "title_subtitle"
    JSON_DATA = "json_data"
    MARKDOWN = "markdown"
    PLAIN_TEXT = "plain_text"
    CODE_SNIPPET = "code_snippet"
    STRUCTURED_DATA = "structured_data"


@dataclass
class ParsedContent:
    """Represents parsed content with metadata."""
    
    content_type: ContentType
    title: Optional[str] = None
    subtitle: Optional[str] = None
    points: Optional[List[str]] = None
    raw_content: str = ""
    metadata: Optional[Dict[str, Any]] = None
    confidence: float = 1.0
    
    def __post_init__(self):
        if self.points is None:
            self.points = []
        if self.metadata is None:
            self.metadata = {}


@dataclass
class SlideData:
    """Structured slide data."""
    
    title: str
    points: List[str]
    slide_type: str = "content"
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class ResponseParser:
    """
    Intelligent parser for AI responses and content extraction.
    
    This class provides robust parsing of various content formats,
    with fallback mechanisms and confidence scoring.
    """
    
    def __init__(self):
        """Initialize the response parser."""
        self._slide_patterns = self._init_slide_patterns()
        self._bullet_patterns = self._init_bullet_patterns()
        self._title_patterns = self._init_title_patterns()
    
    def parse_response(
        self,
        response: str,
        expected_type: Optional[ContentType] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> ParsedContent:
        """
        Parse AI response into structured content.
        
        Args:
            response: Raw response text
            expected_type: Expected content type for optimization
            context: Additional context for parsing
            
        Returns:
            ParsedContent: Parsed and structured content
        """
        if not response or not response.strip():
            return ParsedContent(
                content_type=ContentType.PLAIN_TEXT,
                raw_content=response,
                confidence=0.0
            )
        
        # Try specific parser if type is expected
        if expected_type:
            result = self._parse_by_type(response, expected_type)
            if result.confidence > 0.7:
                return result
        
        # Try all parsers and return best result
        results = []
        
        # Try JSON parsing first
        json_result = self._parse_json(response)
        if json_result.confidence > 0.8:
            results.append(json_result)
        
        # Try slide content parsing
        slide_result = self._parse_slide_content(response)
        results.append(slide_result)
        
        # Try bullet points parsing
        bullet_result = self._parse_bullet_points(response)
        results.append(bullet_result)
        
        # Try title/subtitle parsing
        title_result = self._parse_title_subtitle(response)
        results.append(title_result)
        
        # Try markdown parsing
        markdown_result = self._parse_markdown(response)
        results.append(markdown_result)
        
        # Return result with highest confidence
        best_result = max(results, key=lambda x: x.confidence)
        
        # Fallback to plain text if confidence is too low
        if best_result.confidence < 0.3:
            return ParsedContent(
                content_type=ContentType.PLAIN_TEXT,
                raw_content=response,
                confidence=0.5
            )
        
        return best_result
    
    def parse_slide_list(self, response: str) -> List[SlideData]:
        """
        Parse response into a list of slide data.
        
        Args:
            response: Raw response containing multiple slides
            
        Returns:
            List[SlideData]: List of parsed slides
        """
        slides = []
        
        # Try to parse as JSON first
        try:
            json_data = json.loads(response)
            if isinstance(json_data, list):
                for item in json_data:
                    if isinstance(item, dict) and "title" in item:
                        slides.append(SlideData(
                            title=item.get("title", "Untitled"),
                            points=item.get("points", []),
                            slide_type=item.get("type", "content"),
                            metadata=item.get("metadata", {})
                        ))
                return slides
        except (json.JSONDecodeError, KeyError):
            pass
        
        # Parse as text with slide separators
        slide_sections = self._split_into_slides(response)
        
        for section in slide_sections:
            parsed = self.parse_response(section, ContentType.SLIDE_CONTENT)
            
            if parsed.title or parsed.points:
                slides.append(SlideData(
                    title=parsed.title or "Untitled Slide",
                    points=parsed.points or [],
                    slide_type="content",
                    metadata=parsed.metadata or {}
                ))
        
        return slides
    
    def extract_key_points(self, text: str, max_points: int = 10) -> List[str]:
        """
        Extract key points from text.
        
        Args:
            text: Source text
            max_points: Maximum number of points to extract
            
        Returns:
            List[str]: Extracted key points
        """
        # Parse bullet points first
        bullet_result = self._parse_bullet_points(text)
        if bullet_result.points and len(bullet_result.points) <= max_points:
            return bullet_result.points
        
        # Extract sentences and rank by importance
        sentences = self._extract_sentences(text)
        important_sentences = self._rank_sentences(sentences)
        
        return important_sentences[:max_points]
    
    def clean_and_format_text(self, text: str) -> str:
        """
        Clean and format text content.
        
        Args:
            text: Raw text to clean
            
        Returns:
            str: Cleaned and formatted text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\\s+', ' ', text.strip())
        
        # Remove markdown artifacts
        text = re.sub(r'\\*\\*([^*]+)\\*\\*', r'\\1', text)  # Bold
        text = re.sub(r'\\*([^*]+)\\*', r'\\1', text)        # Italic
        text = re.sub(r'`([^`]+)`', r'\\1', text)            # Code
        
        # Remove extra punctuation
        text = re.sub(r'[.]{2,}', '.', text)
        text = re.sub(r'[!]{2,}', '!', text)
        text = re.sub(r'[?]{2,}', '?', text)
        
        # Ensure proper sentence endings
        if text and not text.endswith(('.', '!', '?', ':')):
            text += '.'
        
        return text
    
    def _parse_by_type(self, response: str, content_type: ContentType) -> ParsedContent:
        """Parse response by specific type."""
        parsers = {
            ContentType.SLIDE_CONTENT: self._parse_slide_content,
            ContentType.BULLET_POINTS: self._parse_bullet_points,
            ContentType.TITLE_SUBTITLE: self._parse_title_subtitle,
            ContentType.JSON_DATA: self._parse_json,
            ContentType.MARKDOWN: self._parse_markdown,
            ContentType.PLAIN_TEXT: self._parse_plain_text,
            ContentType.CODE_SNIPPET: self._parse_code_snippet,
            ContentType.STRUCTURED_DATA: self._parse_structured_data,
        }
        
        parser = parsers.get(content_type, self._parse_plain_text)
        return parser(response)
    
    def _parse_json(self, response: str) -> ParsedContent:
        """Parse JSON content."""
        try:
            # Try to extract JSON from response
            json_match = re.search(r'```json\\n(.+?)\\n```', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Try to parse entire response as JSON
                json_str = response.strip()
            
            data = json.loads(json_str)
            
            # Extract title and points if structured as slide data
            title = None
            points = []
            
            if isinstance(data, dict):
                title = data.get("title")
                points = data.get("points", data.get("bullets", []))
            elif isinstance(data, list):
                # If it's a list, treat as points
                points = [str(item) for item in data]
            
            return ParsedContent(
                content_type=ContentType.JSON_DATA,
                title=title,
                points=points,
                raw_content=response,
                metadata={"parsed_data": data},
                confidence=0.9
            )
            
        except json.JSONDecodeError:
            return ParsedContent(
                content_type=ContentType.JSON_DATA,
                raw_content=response,
                confidence=0.0
            )
    
    def _parse_slide_content(self, response: str) -> ParsedContent:
        """Parse slide content with title and points."""
        title = None
        points = []
        confidence = 0.0
        
        # Look for title patterns
        for pattern in self._title_patterns:
            match = re.search(pattern, response, re.MULTILINE | re.IGNORECASE)
            if match:
                title = self.clean_and_format_text(match.group(1))
                confidence += 0.3
                break
        
        # Look for bullet points
        bullet_result = self._parse_bullet_points(response)
        if bullet_result.points:
            points = bullet_result.points
            confidence += bullet_result.confidence * 0.7
        
        # If no title found, try to extract from first line
        if not title and response:
            lines = response.strip().split('\\n')
            if lines:
                first_line = lines[0].strip()
                if len(first_line) < 100 and not any(bullet in first_line for bullet in ['•', '-', '*', '1.']):
                    title = self.clean_and_format_text(first_line)
                    confidence += 0.2
        
        return ParsedContent(
            content_type=ContentType.SLIDE_CONTENT,
            title=title,
            points=points,
            raw_content=response,
            confidence=min(confidence, 1.0)
        )
    
    def _parse_bullet_points(self, response: str) -> ParsedContent:
        """Parse bullet points from text."""
        points = []
        confidence = 0.0
        
        # Look for various bullet point patterns
        for pattern in self._bullet_patterns:
            matches = re.findall(pattern, response, re.MULTILINE)
            if matches:
                for match in matches:
                    point = self.clean_and_format_text(match)
                    if point and len(point) > 3:  # Minimum point length
                        points.append(point)
                confidence = min(0.8, len(matches) * 0.2)
                break
        
        # Remove duplicates while preserving order
        seen = set()
        unique_points = []
        for point in points:
            if point.lower() not in seen:
                seen.add(point.lower())
                unique_points.append(point)
        
        return ParsedContent(
            content_type=ContentType.BULLET_POINTS,
            points=unique_points,
            raw_content=response,
            confidence=confidence
        )
    
    def _parse_title_subtitle(self, response: str) -> ParsedContent:
        """Parse title and subtitle."""
        title = None
        subtitle = None
        confidence = 0.0
        
        lines = [line.strip() for line in response.split('\\n') if line.strip()]
        
        if len(lines) >= 1:
            # First non-empty line is likely the title
            title = self.clean_and_format_text(lines[0])
            confidence += 0.5
            
            if len(lines) >= 2:
                # Second line might be subtitle
                potential_subtitle = lines[1]
                if len(potential_subtitle) < len(title) * 2:  # Reasonable length
                    subtitle = self.clean_and_format_text(potential_subtitle)
                    confidence += 0.3
        
        return ParsedContent(
            content_type=ContentType.TITLE_SUBTITLE,
            title=title,
            subtitle=subtitle,
            raw_content=response,
            confidence=confidence
        )
    
    def _parse_markdown(self, response: str) -> ParsedContent:
        """Parse markdown content."""
        title = None
        points = []
        confidence = 0.0
        
        # Look for markdown headers
        header_match = re.search(r'^#+\\s+(.+)$', response, re.MULTILINE)
        if header_match:
            title = self.clean_and_format_text(header_match.group(1))
            confidence += 0.4
        
        # Look for markdown lists
        list_items = re.findall(r'^[-*+]\\s+(.+)$', response, re.MULTILINE)
        if list_items:
            points = [self.clean_and_format_text(item) for item in list_items]
            confidence += 0.4
        
        # Look for numbered lists
        numbered_items = re.findall(r'^\\d+\\.\\s+(.+)$', response, re.MULTILINE)
        if numbered_items:
            points.extend([self.clean_and_format_text(item) for item in numbered_items])
            confidence += 0.3
        
        return ParsedContent(
            content_type=ContentType.MARKDOWN,
            title=title,
            points=points,
            raw_content=response,
            confidence=min(confidence, 1.0)
        )
    
    def _parse_plain_text(self, response: str) -> ParsedContent:
        """Parse plain text."""
        return ParsedContent(
            content_type=ContentType.PLAIN_TEXT,
            raw_content=self.clean_and_format_text(response),
            confidence=0.5
        )
    
    def _parse_code_snippet(self, response: str) -> ParsedContent:
        """Parse code snippets."""
        # Look for code blocks
        code_blocks = re.findall(r'```(?:\\w+)?\\n(.+?)\\n```', response, re.DOTALL)
        
        if code_blocks:
            return ParsedContent(
                content_type=ContentType.CODE_SNIPPET,
                raw_content=response,
                metadata={"code_blocks": code_blocks},
                confidence=0.8
            )
        
        return ParsedContent(
            content_type=ContentType.CODE_SNIPPET,
            raw_content=response,
            confidence=0.1
        )
    
    def _parse_structured_data(self, response: str) -> ParsedContent:
        """Parse structured data formats."""
        # Try to identify structured patterns
        confidence = 0.0
        
        # Look for key-value pairs
        kv_pairs = re.findall(r'^([^:]+):\\s*(.+)$', response, re.MULTILINE)
        if kv_pairs:
            confidence += 0.4
        
        # Look for structured sections
        sections = re.findall(r'^([A-Z][^\\n]+):$', response, re.MULTILINE)
        if sections:
            confidence += 0.3
        
        return ParsedContent(
            content_type=ContentType.STRUCTURED_DATA,
            raw_content=response,
            metadata={"kv_pairs": kv_pairs, "sections": sections},
            confidence=confidence
        )
    
    def _split_into_slides(self, response: str) -> List[str]:
        """Split response into individual slide sections."""
        # Look for slide separators
        slide_separators = [
            r'---+',  # Horizontal rules
            r'Slide \\d+',  # Slide numbers
            r'#{1,3}\\s+[^\\n]+',  # Headers
        ]
        
        sections = []
        current_section = ""
        
        lines = response.split('\\n')
        
        for line in lines:
            is_separator = any(re.match(pattern, line.strip()) for pattern in slide_separators)
            
            if is_separator and current_section.strip():
                sections.append(current_section.strip())
                current_section = line + '\\n'
            else:
                current_section += line + '\\n'
        
        # Add the last section
        if current_section.strip():
            sections.append(current_section.strip())
        
        return sections if sections else [response]
    
    def _extract_sentences(self, text: str) -> List[str]:
        """Extract sentences from text."""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
    
    def _rank_sentences(self, sentences: List[str]) -> List[str]:
        """Rank sentences by importance."""
        # Simple ranking based on length and keywords
        importance_keywords = [
            'important', 'key', 'main', 'primary', 'essential', 'critical',
            'significant', 'major', 'crucial', 'fundamental', 'core'
        ]
        
        scored_sentences = []
        
        for sentence in sentences:
            score = len(sentence) / 100  # Base score on length
            
            # Boost score for importance keywords
            for keyword in importance_keywords:
                if keyword in sentence.lower():
                    score += 0.5
            
            # Boost score for sentences at the beginning
            if sentences.index(sentence) < len(sentences) * 0.3:
                score += 0.3
            
            scored_sentences.append((score, sentence))
        
        # Sort by score and return sentences
        scored_sentences.sort(key=lambda x: x[0], reverse=True)
        return [sentence for score, sentence in scored_sentences]
    
    def _init_slide_patterns(self) -> List[str]:
        """Initialize slide parsing patterns."""
        return [
            r'^Slide\\s+\\d+:?\\s*(.+)$',
            r'^##?\\s+(.+)$',
            r'^Title:?\\s+(.+)$',
            r'^(.+)\\s*:$',
        ]
    
    def _init_bullet_patterns(self) -> List[str]:
        """Initialize bullet point patterns."""
        return [
            r'^\\s*[•▪▫‣⁃]\\s+(.+)$',  # Bullet symbols
            r'^\\s*[-*+]\\s+(.+)$',     # Dash/asterisk/plus
            r'^\\s*\\d+\\.\\s+(.+)$',   # Numbered lists
            r'^\\s*\\([a-zA-Z0-9]+\\)\\s+(.+)$',  # Lettered/numbered in parentheses
            r'^\\s*[a-zA-Z]\\)\\s+(.+)$',  # Lettered lists
        ]
    
    def _init_title_patterns(self) -> List[str]:
        """Initialize title parsing patterns."""
        return [
            r'^#+\\s+(.+)$',  # Markdown headers
            r'^Title:?\\s*(.+)$',  # Explicit title
            r'^(.+)\\n=+$',  # Underlined with equals
            r'^(.+)\\n-+$',  # Underlined with dashes
            r'^\\*\\*(.+)\\*\\*$',  # Bold text
        ]


class ContentParser:
    """
    Specialized parser for different content types.
    
    This class provides targeted parsing for specific content structures
    like presentations, documents, and code repositories.
    """
    
    def __init__(self):
        """Initialize content parser."""
        self.response_parser = ResponseParser()
    
    def parse_presentation_content(self, content: str) -> Dict[str, Any]:
        """
        Parse content for presentation creation.
        
        Args:
            content: Raw content to parse
            
        Returns:
            dict: Structured presentation data
        """
        # Parse slides
        slides = self.response_parser.parse_slide_list(content)
        
        # Extract presentation metadata
        title_result = self.response_parser.parse_response(content, ContentType.TITLE_SUBTITLE)
        
        return {
            "title": title_result.title or "Presentation",
            "subtitle": title_result.subtitle,
            "slides": [
                {
                    "title": slide.title,
                    "points": slide.points,
                    "type": slide.slide_type,
                    "metadata": slide.metadata
                }
                for slide in slides
            ],
            "metadata": {
                "slide_count": len(slides),
                "total_points": sum(len(slide.points) for slide in slides)
            }
        }
    
    def parse_repository_structure(self, structure_data: str) -> Dict[str, Any]:
        """
        Parse repository structure data.
        
        Args:
            structure_data: Repository structure information
            
        Returns:
            dict: Parsed repository structure
        """
        parsed = self.response_parser.parse_response(structure_data, ContentType.STRUCTURED_DATA)
        
        # Extract file lists, directories, etc.
        files = []
        directories = []
        
        # Simple parsing logic (can be enhanced)
        lines = structure_data.split('\\n')
        for line in lines:
            line = line.strip()
            if line.endswith('/'):
                directories.append(line[:-1])
            elif '.' in line:
                files.append(line)
        
        return {
            "files": files,
            "directories": directories,
            "raw_structure": structure_data,
            "metadata": parsed.metadata
        }
    
    def extract_code_insights(self, code_content: str, language: str = "unknown") -> Dict[str, Any]:
        """
        Extract insights from code content.
        
        Args:
            code_content: Source code content
            language: Programming language
            
        Returns:
            dict: Code insights and analysis
        """
        insights = {
            "language": language,
            "line_count": len(code_content.split('\\n')),
            "functions": [],
            "classes": [],
            "imports": [],
            "comments": [],
            "complexity_indicators": []
        }
        
        # Language-specific parsing (simplified)
        if language.lower() in ['python', 'py']:
            insights.update(self._parse_python_code(code_content))
        elif language.lower() in ['javascript', 'js', 'typescript', 'ts']:
            insights.update(self._parse_javascript_code(code_content))
        elif language.lower() in ['java']:
            insights.update(self._parse_java_code(code_content))
        
        return insights
    
    def _parse_python_code(self, code: str) -> Dict[str, List[str]]:
        """Parse Python code for insights."""
        return {
            "functions": re.findall(r'^def\\s+(\\w+)\\s*\\(', code, re.MULTILINE),
            "classes": re.findall(r'^class\\s+(\\w+)\\s*[:\\(]', code, re.MULTILINE),
            "imports": re.findall(r'^(?:from\\s+\\w+\\s+)?import\\s+([\\w.,\\s]+)', code, re.MULTILINE),
            "comments": re.findall(r'#\\s*(.+)', code),
        }
    
    def _parse_javascript_code(self, code: str) -> Dict[str, List[str]]:
        """Parse JavaScript code for insights."""
        return {
            "functions": re.findall(r'function\\s+(\\w+)\\s*\\(', code) + 
                        re.findall(r'(\\w+)\\s*=>\\s*[{(]', code),
            "classes": re.findall(r'class\\s+(\\w+)\\s*[{]', code),
            "imports": re.findall(r'import\\s+.*?from\\s+[\'"]([^\'"]+)[\'"]', code),
            "comments": re.findall(r'//\\s*(.+)', code),
        }
    
    def _parse_java_code(self, code: str) -> Dict[str, List[str]]:
        """Parse Java code for insights."""
        return {
            "functions": re.findall(r'\\w+\\s+(\\w+)\\s*\\([^)]*\\)\\s*{', code),
            "classes": re.findall(r'class\\s+(\\w+)\\s*[{]', code),
            "imports": re.findall(r'import\\s+([\\w.]+);', code),
            "comments": re.findall(r'//\\s*(.+)', code),
        }

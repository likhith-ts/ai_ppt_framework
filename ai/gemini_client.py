"""
Gemini AI client for the AI PowerPoint Framework.

This module provides a robust interface to Google's Gemini AI for content analysis
and generation with retry logic, error handling, and fallback mechanisms.
"""

import time
import random
from typing import Optional, Dict, Union

import google.genai as genai

from core.config import FrameworkConfig
from core.exceptions import AIClientError


class GeminiClient:
    """
    Google Gemini AI client with advanced error handling and retry logic.

    Features:
    - Exponential backoff with jitter for rate limiting
    - Configurable retry attempts
    - Comprehensive error handling
    - Multiple model support
    - Usage tracking and monitoring
    """

    def __init__(self, config: Optional[FrameworkConfig] = None):
        """
        Initialize the Gemini client.

        Args:
            config: Configuration instance. If None, uses default config.

        Raises:
            AIClientError: If API key is not configured when AI is required
        """
        self.config = config or FrameworkConfig()
        self.client = None
        self.model_name = "gemini-1.5-flash"  # Default model
        self.max_retries = self.config.max_retries
        self.request_count = 0
        self.error_count = 0

        # Only initialize client if API key is available
        if self.config.gemini_api_key:
            try:
                self.client = genai.Client(api_key=self.config.gemini_api_key)
            except Exception as e:
                raise AIClientError(f"Failed to initialize Gemini client: {str(e)}")
        else:
            # Client will be None, which will be handled in generate_content
            pass

    def generate_content(
        self,
        prompt: str,
        max_retries: Optional[int] = None,
        model: Optional[str] = None,
    ) -> str:
        """
        Generate content using Gemini AI with retry logic.

        Args:
            prompt: The prompt to send to Gemini
            max_retries: Override default retry count
            model: Override default model

        Returns:
            Generated content as string

        Raises:
            AIClientError: If generation fails after all retries
        """
        if not self.client:
            raise AIClientError("Gemini client not initialized - API key not configured")

        retries = max_retries or self.max_retries
        model_name = model or self.model_name

        self.request_count += 1

        for attempt in range(retries):
            try:
                response = self.client.models.generate_content(
                    model=model_name, contents=prompt
                )

                if not response.text:
                    raise AIClientError("Empty response from Gemini")

                return response.text

            except Exception as e:
                self.error_count += 1
                error_msg = str(e)

                # Check if it's a rate limit or overload error
                if self._is_rate_limit_error(error_msg):
                    if attempt < retries - 1:
                        delay = self._calculate_retry_delay(attempt)
                        time.sleep(delay)
                        continue
                    else:
                        raise AIClientError(
                            f"Rate limit exceeded after {retries} attempts"
                        ) from e
                else:
                    # For other errors, don't retry
                    raise AIClientError(f"Gemini API error: {error_msg}") from e

        # Should never reach here, but just in case
        raise AIClientError(f"Failed to generate content after {retries} attempts")

    def _is_rate_limit_error(self, error_msg: str) -> bool:
        """Check if error indicates rate limiting or service overload."""
        rate_limit_indicators = [
            "503",
            "overloaded",
            "unavailable",
            "rate limit",
            "quota exceeded",
            "too many requests",
        ]
        return any(
            indicator in error_msg.lower() for indicator in rate_limit_indicators
        )

    def _calculate_retry_delay(self, attempt: int) -> float:
        """Calculate retry delay with exponential backoff and jitter."""
        base_delay = 2**attempt  # 1, 2, 4, 8 seconds
        jitter = random.uniform(0.1, 0.5)  # Add random jitter
        return base_delay + jitter

    def get_usage_stats(self) -> Dict[str, Union[int, float]]:
        """Get client usage statistics."""
        return {
            "total_requests": self.request_count,
            "total_errors": self.error_count,
            "success_rate": (
                (self.request_count - self.error_count) / self.request_count * 100
                if self.request_count > 0
                else 0
            ),
        }

    def reset_stats(self) -> None:
        """Reset usage statistics."""
        self.request_count = 0
        self.error_count = 0

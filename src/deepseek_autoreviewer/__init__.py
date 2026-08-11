"""DeepSeek AutoReviewer."""

from .core import ReviewerConfig, review_pdf, review_text

__all__ = ["ReviewerConfig", "review_pdf", "review_text"]
__version__ = "0.1.0"

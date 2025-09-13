"""
Week 4: AI News Summarizer & Q&A Tool
Modular implementation with real API integration
"""


from .api_client import LLMClient, APIClientManager
from .summarizer_engine import ArticleSummarizer, SummaryAnalyzer
from .qa_engine import ArticleQAEngine, QuestionSuggester, QAAnalyzer
from .models import (
    Article, APIResponse, SummaryResult, QAResult, 
    ExperimentResults, SessionData
)
from .config import (
    DEFAULT_GEMINI_MODEL, DEFAULT_OPENAI_MODEL,
    TEMPERATURE_SETTINGS, PROMPTS, PERSONALITY_STYLES
)

__all__ = [
    "LLMClient",
    "APIClientManager", 
    "ArticleSummarizer",
    "SummaryAnalyzer",
    "ArticleQAEngine",
    "QuestionSuggester",
    "QAAnalyzer",
    "Article",
    "APIResponse",
    "SummaryResult",
    "QAResult",
    "ExperimentResults",
    "SessionData",
    "DEFAULT_GEMINI_MODEL",
    "DEFAULT_OPENAI_MODEL",
    "TEMPERATURE_SETTINGS",
    "PROMPTS",
    "PERSONALITY_STYLES"
]
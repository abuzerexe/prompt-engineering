"""
Data models for Week 4 API Usage Assignment
"""
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime

@dataclass
class APIResponse:
    """Structure to hold API response data"""
    content: str
    model: str
    temperature: float
    tokens_used: int = 0
    success: bool = True
    error_message: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def word_count(self) -> int:
        """Calculate word count of response content"""
        return len(self.content.split()) if self.content else 0

@dataclass
class Article:
    """Structure to hold article information"""
    title: str
    content: str
    url: Optional[str] = None
    source: Optional[str] = None
    
    @property
    def word_count(self) -> int:
        """Calculate word count of article content"""
        return len(self.content.split()) if self.content else 0
    
    @property
    def char_count(self) -> int:
        """Calculate character count of article content"""
        return len(self.content) if self.content else 0

@dataclass
class SummaryResult:
    """Structure to hold summarization results"""
    original_article: Article
    summary: APIResponse
    temperature_used: float
    
    @property
    def compression_ratio(self) -> float:
        """Calculate compression ratio (original/summary word count)"""
        if self.summary.word_count == 0:
            return 0.0
        return self.original_article.word_count / self.summary.word_count

@dataclass
class QAResult:
    """Structure to hold Q&A results"""
    question: str
    answer: APIResponse
    article: Article
    
@dataclass
class ExperimentResults:
    """Structure to hold temperature experiment results"""
    article: Article
    results: Dict[str, SummaryResult] = field(default_factory=dict)
    
    def add_result(self, temperature_name: str, result: SummaryResult):
        """Add a temperature experiment result"""
        self.results[temperature_name] = result
    
    def get_all_summaries(self) -> Dict[str, str]:
        """Get all summaries keyed by temperature name"""
        return {name: result.summary.content for name, result in self.results.items()}
    
    def get_token_usage(self) -> Dict[str, int]:
        """Get token usage for each temperature setting"""
        return {name: result.summary.tokens_used for name, result in self.results.items()}

@dataclass  
class SessionData:
    """Structure to hold complete session data"""
    article: Article
    summary_experiments: ExperimentResults
    qa_results: list[QAResult] = field(default_factory=list)
    total_tokens_used: int = 0
    
    def add_qa_result(self, qa_result: QAResult):
        """Add a Q&A result to the session"""
        self.qa_results.append(qa_result)
        self.total_tokens_used += qa_result.answer.tokens_used
    
    def get_session_summary(self) -> str:
        """Generate a summary of the session"""
        summary = f"Session Summary:\n"
        summary += f"Article: {self.article.title}\n"
        summary += f"Article Length: {self.article.word_count} words\n"
        summary += f"Temperature Experiments: {len(self.summary_experiments.results)}\n"
        summary += f"Q&A Sessions: {len(self.qa_results)}\n"
        summary += f"Total Tokens Used: {self.total_tokens_used}\n"
        return summary
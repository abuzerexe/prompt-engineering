"""
Data models for Week 3 Advanced Prompting Assignment
"""
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class TestResult:
    """Structure to hold test results for evaluation"""
    task_id: int
    task_text: str
    expected_answer: str
    prompt_type: str
    prompt_used: str
    model_response: str
    model_used: str
    tokens_used: int = 0
    correctness_score: int = 0
    reasoning_clarity_score: int = 0
    completeness_score: int = 0
    conciseness_score: int = 0
    
    @property
    def total_score(self) -> int:
        """Calculate total score across all criteria"""
        return (self.correctness_score + self.reasoning_clarity_score + 
                self.completeness_score + self.conciseness_score)
    
    @property
    def max_possible_score(self) -> int:
        """Maximum possible score (3 points per criteria)"""
        return 12

@dataclass
class TaskData:
    """Structure to hold task information"""
    task_id: int
    task_type: str
    question: str
    expected_answer: str
    difficulty: str = "medium"
    
    def __post_init__(self):
        """Validate task data after initialization"""
        if not self.question.strip():
            raise ValueError("Question cannot be empty")
        if not self.expected_answer.strip():
            raise ValueError("Expected answer cannot be empty")

@dataclass
class APIResponse:
    """Structure to hold API response data"""
    response: str
    model: str
    token_usage: Dict[str, int]
    success: bool = True
    error_message: str = ""
    
    @property
    def total_tokens(self) -> int:
        """Get total tokens used"""
        return self.token_usage.get("total_tokens", 0)
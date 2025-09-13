"""
Evaluation logic and scoring system for prompting strategies
"""
import re
from typing import List, Dict, Any
from config import SCORING_RUBRIC
from models import TaskData, APIResponse, TestResult

class ResponseEvaluator:
    """Evaluates LLM responses based on predefined criteria"""
    
    def __init__(self):
        self.scoring_rubric = SCORING_RUBRIC
    
    def evaluate_correctness(self, expected: str, actual: str, task_type: str) -> int:
        """
        Evaluate correctness of the response
        
        Args:
            expected: Expected answer
            actual: Actual model response
            task_type: Type of task (logic, math, reasoning)
            
        Returns:
            Score from 0-3
        """
        expected_lower = expected.lower().strip()
        actual_lower = actual.lower().strip()
        
        # For math problems, look for numeric answers
        if task_type == "math":
            expected_nums = re.findall(r'\d+', expected)
            actual_nums = re.findall(r'\d+', actual)
            
            if expected_nums and actual_nums:
                if expected_nums[0] == actual_nums[0]:
                    return 3  # Exact match
                else:
                    return 0  # Wrong answer
        
        # For logic problems, check key concepts
        if task_type == "logic":
            if expected_lower in actual_lower:
                return 3  # Contains expected answer
            
            # Check for logical reasoning keywords
            key_words = expected_lower.split()
            matches = sum(1 for word in key_words if word in actual_lower)
            if matches > len(key_words) * 0.5:
                return 2  # Partial match
            else:
                return 1  # Some reasoning present
        
        # For reasoning tasks, check conceptual understanding
        if task_type == "reasoning":
            # Check if key concepts are present
            if "not necessarily" in expected_lower and "not necessarily" in actual_lower:
                return 3
            elif "necessarily" in expected_lower and "necessarily" in actual_lower:
                return 3
            elif any(word in actual_lower for word in expected_lower.split()):
                return 2
            else:
                return 1
        
        # General text matching fallback
        if expected_lower == actual_lower:
            return 3
        elif expected_lower in actual_lower or actual_lower in expected_lower:
            return 2
        else:
            return 1
    
    def evaluate_reasoning_clarity(self, response: str, strategy_name: str) -> int:
        """
        Evaluate clarity of reasoning in the response
        
        Args:
            response: Model response
            strategy_name: Strategy used (affects expectations)
            
        Returns:
            Score from 0-3
        """
        response_lower = response.lower()
        
        # Chain-of-thought should have step-by-step reasoning
        if strategy_name == "COT":
            step_indicators = ["step", "first", "second", "next", "then", "therefore", "because"]
            step_count = sum(1 for indicator in step_indicators if indicator in response_lower)
            
            if step_count >= 3:
                return 3  # Clear step-by-step reasoning
            elif step_count >= 2:
                return 2  # Some structured reasoning
            else:
                return 1  # Minimal reasoning structure
        
        # For other strategies, check for logical connectors
        reasoning_words = ["because", "since", "therefore", "thus", "hence", "so", "if", "then"]
        reasoning_count = sum(1 for word in reasoning_words if word in response_lower)
        
        if reasoning_count >= 2:
            return 3  # Clear reasoning
        elif reasoning_count >= 1:
            return 2  # Some reasoning
        else:
            return 1  # Minimal reasoning
    
    def evaluate_completeness(self, response: str, task: TaskData, strategy_name: str) -> int:
        """
        Evaluate completeness of the response
        
        Args:
            response: Model response
            task: Original task
            strategy_name: Strategy used
            
        Returns:
            Score from 0-3
        """
        # Check response length as a proxy for completeness
        response_length = len(response.strip())
        
        if strategy_name == "COT":
            # CoT should be more detailed
            if response_length >= 200:
                return 3  # Comprehensive
            elif response_length >= 100:
                return 2  # Adequate
            else:
                return 1  # Brief
        else:
            # Other strategies can be more concise
            if response_length >= 50:
                return 3  # Complete
            elif response_length >= 20:
                return 2  # Adequate
            else:
                return 1  # Brief
    
    def evaluate_conciseness(self, response: str, strategy_name: str) -> int:
        """
        Evaluate conciseness of the response
        
        Args:
            response: Model response
            strategy_name: Strategy used
            
        Returns:
            Score from 0-3 (higher = more concise, but appropriate for strategy)
        """
        response_length = len(response.strip())
        word_count = len(response.split())
        
        if strategy_name == "COT":
            # CoT is expected to be longer, so different standards
            if word_count <= 150:
                return 3  # Appropriately detailed
            elif word_count <= 250:
                return 2  # Somewhat verbose
            else:
                return 1  # Too verbose
        else:
            # Other strategies should be more concise
            if word_count <= 50:
                return 3  # Concise
            elif word_count <= 100:
                return 2  # Moderate length
            else:
                return 1  # Too verbose
    
    def evaluate_response(self, task: TaskData, response: APIResponse, 
                         strategy_name: str, prompt_used: str) -> TestResult:
        """
        Evaluate a complete response using all criteria
        
        Args:
            task: Original task
            response: API response
            strategy_name: Strategy used
            prompt_used: Prompt that was used
            
        Returns:
            TestResult with all scores
        """
        if not response.success:
            # Return zero scores for failed responses
            return TestResult(
                task_id=task.task_id,
                task_text=task.question,
                expected_answer=task.expected_answer,
                prompt_type=strategy_name,
                prompt_used=prompt_used,
                model_response=f"API Error: {response.error_message}",
                model_used=response.model,
                tokens_used=0
            )
        
        # Evaluate all criteria
        correctness_score = self.evaluate_correctness(
            task.expected_answer, response.response, task.task_type
        )
        
        reasoning_clarity_score = self.evaluate_reasoning_clarity(
            response.response, strategy_name
        )
        
        completeness_score = self.evaluate_completeness(
            response.response, task, strategy_name
        )
        
        conciseness_score = self.evaluate_conciseness(
            response.response, strategy_name
        )
        
        return TestResult(
            task_id=task.task_id,
            task_text=task.question,
            expected_answer=task.expected_answer,
            prompt_type=strategy_name,
            prompt_used=prompt_used,
            model_response=response.response,
            model_used=response.model,
            tokens_used=response.total_tokens,
            correctness_score=correctness_score,
            reasoning_clarity_score=reasoning_clarity_score,
            completeness_score=completeness_score,
            conciseness_score=conciseness_score
        )

class ResultAnalyzer:
    """Analyzes and summarizes evaluation results"""
    
    def __init__(self):
        pass
    
    def calculate_strategy_averages(self, results: List[TestResult]) -> Dict[str, Dict[str, float]]:
        """
        Calculate average scores by strategy
        
        Args:
            results: List of test results
            
        Returns:
            Dictionary with strategy averages
        """
        strategy_data = {}
        
        for result in results:
            strategy = result.prompt_type
            if strategy not in strategy_data:
                strategy_data[strategy] = {
                    "total_scores": [],
                    "correctness": [],
                    "reasoning_clarity": [],
                    "completeness": [],
                    "conciseness": [],
                    "tokens": []
                }
            
            strategy_data[strategy]["total_scores"].append(result.total_score)
            strategy_data[strategy]["correctness"].append(result.correctness_score)
            strategy_data[strategy]["reasoning_clarity"].append(result.reasoning_clarity_score)
            strategy_data[strategy]["completeness"].append(result.completeness_score)
            strategy_data[strategy]["conciseness"].append(result.conciseness_score)
            strategy_data[strategy]["tokens"].append(result.tokens_used)
        
        # Calculate averages
        averages = {}
        for strategy, data in strategy_data.items():
            averages[strategy] = {
                "avg_total": sum(data["total_scores"]) / len(data["total_scores"]),
                "avg_correctness": sum(data["correctness"]) / len(data["correctness"]),
                "avg_reasoning": sum(data["reasoning_clarity"]) / len(data["reasoning_clarity"]),
                "avg_completeness": sum(data["completeness"]) / len(data["completeness"]),
                "avg_conciseness": sum(data["conciseness"]) / len(data["conciseness"]),
                "avg_tokens": sum(data["tokens"]) / len(data["tokens"]),
                "total_tokens": sum(data["tokens"])
            }
        
        return averages
    
    def generate_summary_report(self, results: List[TestResult]) -> str:
        """
        Generate a summary report of all results
        
        Args:
            results: List of test results
            
        Returns:
            Formatted summary report as string
        """
        if not results:
            return "No results to analyze."
        
        averages = self.calculate_strategy_averages(results)
        total_tokens = sum(result.tokens_used for result in results)
        
        report = "# Advanced Prompting Strategy Comparison Report\n\n"
        report += f"**Total Tokens Used**: {total_tokens:,}\n"
        report += f"**Model Used**: {results[0].model_used}\n\n"
        
        report += "## Strategy Performance Summary\n\n"
        
        for strategy, data in averages.items():
            report += f"### {strategy.upper()}\n"
            report += f"- **Average Total Score**: {data['avg_total']:.1f}/12\n"
            report += f"- **Correctness**: {data['avg_correctness']:.1f}/3\n"
            report += f"- **Reasoning Clarity**: {data['avg_reasoning']:.1f}/3\n"
            report += f"- **Completeness**: {data['avg_completeness']:.1f}/3\n"
            report += f"- **Conciseness**: {data['avg_conciseness']:.1f}/3\n"
            report += f"- **Average Tokens**: {data['avg_tokens']:.0f}\n"
            report += f"- **Total Tokens**: {data['total_tokens']}\n\n"
        
        return report
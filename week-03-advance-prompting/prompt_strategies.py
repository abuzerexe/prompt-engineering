"""
Implementation of different prompting strategies
"""
from typing import List, Dict, Any
from config import PROMPT_TEMPLATES
from models import TaskData, APIResponse
from api_client import LLMAPIClient

class PromptStrategy:
    """Base class for prompting strategies"""
    
    def __init__(self, name: str, api_client: LLMAPIClient):
        self.name = name
        self.api_client = api_client
    
    def generate_prompt(self, task: TaskData) -> str:
        """Generate prompt for the given task"""
        raise NotImplementedError("Subclasses must implement generate_prompt")
    
    def execute(self, task: TaskData, provider: str = "gemini") -> APIResponse:
        """Execute the strategy on a given task"""
        prompt = self.generate_prompt(task)
        return self.api_client.call_api(prompt, provider)

class ZeroShotStrategy(PromptStrategy):
    """Zero-shot prompting strategy"""
    
    def __init__(self, api_client: LLMAPIClient):
        super().__init__("ZERO_SHOT", api_client)
    
    def generate_prompt(self, task: TaskData) -> str:
        """Generate zero-shot prompt"""
        template = PROMPT_TEMPLATES["zero_shot"][task.task_type]
        return template.format(question=task.question)

class FewShotStrategy(PromptStrategy):
    """Few-shot prompting strategy with examples"""
    
    def __init__(self, api_client: LLMAPIClient):
        super().__init__("FEW_SHOT", api_client)
    
    def generate_prompt(self, task: TaskData) -> str:
        """Generate few-shot prompt with examples"""
        template = PROMPT_TEMPLATES["few_shot"][task.task_type]
        return template.format(question=task.question)

class ChainOfThoughtStrategy(PromptStrategy):
    """Chain-of-thought prompting strategy"""
    
    def __init__(self, api_client: LLMAPIClient):
        super().__init__("COT", api_client)
    
    def generate_prompt(self, task: TaskData) -> str:
        """Generate chain-of-thought prompt"""
        template = PROMPT_TEMPLATES["cot"][task.task_type]
        return template.format(question=task.question)

class PromptStrategyRunner:
    """Runner class to execute multiple strategies on tasks"""
    
    def __init__(self, api_client: LLMAPIClient):
        self.api_client = api_client
        self.strategies = {
            "zero_shot": ZeroShotStrategy(api_client),
            "few_shot": FewShotStrategy(api_client),
            "cot": ChainOfThoughtStrategy(api_client)
        }
    
    def run_strategy(self, strategy_name: str, task: TaskData, provider: str = "gemini") -> Dict[str, Any]:
        """
        Run a specific strategy on a task
        
        Args:
            strategy_name: Name of the strategy to run
            task: Task to execute
            provider: API provider to use
            
        Returns:
            Dictionary containing execution results
        """
        if strategy_name not in self.strategies:
            raise ValueError(f"Unknown strategy: {strategy_name}")
        
        strategy = self.strategies[strategy_name]
        prompt = strategy.generate_prompt(task)
        response = strategy.execute(task, provider)
        
        return {
            "task": task,
            "strategy": strategy_name,
            "prompt": prompt,
            "response": response
        }
    
    def run_all_strategies(self, task: TaskData, provider: str = "gemini") -> List[Dict[str, Any]]:
        """
        Run all strategies on a single task
        
        Args:
            task: Task to execute
            provider: API provider to use
            
        Returns:
            List of results from all strategies
        """
        results = []
        for strategy_name in self.strategies.keys():
            result = self.run_strategy(strategy_name, task, provider)
            results.append(result)
        return results
    
    def run_strategies_on_tasks(self, tasks: List[TaskData], provider: str = "gemini") -> List[Dict[str, Any]]:
        """
        Run all strategies on multiple tasks
        
        Args:
            tasks: List of tasks to execute
            provider: API provider to use
            
        Returns:
            List of all results
        """
        all_results = []
        for task in tasks:
            task_results = self.run_all_strategies(task, provider)
            all_results.extend(task_results)
        return all_results
    
    def get_available_strategies(self) -> List[str]:
        """Get list of available strategy names"""
        return list(self.strategies.keys())
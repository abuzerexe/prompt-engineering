"""
Configuration settings for Week 3 Advanced Prompting Assignment
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_KEY")
OPEN_ROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Model Configuration
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
DEFAULT_OPENAI_MODEL = "openai/gpt-4o"
MAX_TOKENS = 1000

# Evaluation Configuration
SCORING_RUBRIC = {
    "correctness": {
        "max_score": 3,
        "description": "How accurate is the answer?"
    },
    "reasoning_clarity": {
        "max_score": 3,
        "description": "How clear and logical is the reasoning?"
    },
    "completeness": {
        "max_score": 3,
        "description": "How thorough is the response?"
    },
    "conciseness": {
        "max_score": 3,
        "description": "How concise and to-the-point is the response?"
    }
}

# Prompt Templates
PROMPT_TEMPLATES = {
    "zero_shot": {
        "logic": "Solve this logic puzzle: {question}",
        "math": "Solve this math problem: {question}",
        "reasoning": "Answer this question: {question}"
    },
    "few_shot": {
        "logic": """Solve these logic puzzles:

Example 1:
Puzzle: If all cats are animals and Fluffy is a cat, is Fluffy an animal?
Answer: Yes, because if all cats are animals and Fluffy is a cat, then Fluffy must be an animal.

Example 2:
Puzzle: Tom is taller than Jerry. Jerry is taller than Spike. Who is the shortest?
Answer: Spike, because if Tom > Jerry and Jerry > Spike, then Spike is the shortest.

Now solve:
Puzzle: {question}
Answer:""",
        "math": """Solve these math problems:

Example 1:
Problem: A car travels 50 km in 1 hour. How far will it go in 3 hours?
Answer: 150 km (50 km/hour × 3 hours = 150 km)

Example 2:
Problem: What is 15 × 8?
Answer: 120

Now solve:
Problem: {question}
Answer:""",
        "reasoning": """Answer these reasoning questions:

Example 1:
Question: If Sarah is older than Mike, and Mike is older than Lisa, who is the oldest?
Answer: Sarah is the oldest.

Example 2:
Question: A bakery makes 12 cookies per hour. How many cookies in 4 hours?
Answer: 48 cookies (12 × 4 = 48)

Now answer:
Question: {question}
Answer:"""
    },
    "cot": {
        "logic": """Solve this logic puzzle step by step, showing your reasoning:

Puzzle: {question}

Think step by step and explain your reasoning:""",
        "math": """Solve this math problem step by step:

Problem: {question}

Show your work step by step:""",
        "reasoning": """Answer this question by thinking through it step by step:

Question: {question}

Think step by step and explain your reasoning:"""
    }
}
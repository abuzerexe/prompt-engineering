"""
Test datasets for Week 3 Advanced Prompting Assignment
"""
import json
import os
from typing import List
from models import TaskData

# Embedded datasets as fallback if files not found
EMBEDDED_DATASETS = {
    "logic_puzzles": [
        {
            "task_id": 1,
            "task_type": "logic",
            "question": "Alice is older than Bob. Bob is older than Charlie. Who is the youngest?",
            "expected_answer": "Charlie",
            "difficulty": "easy"
        },
        {
            "task_id": 2,
            "task_type": "logic", 
            "question": "If all roses are flowers and some flowers are red, can we conclude that some roses are red?",
            "expected_answer": "No, we cannot conclude that. While all roses are flowers, we don't know if the red flowers include roses.",
            "difficulty": "medium"
        },
        {
            "task_id": 3,
            "task_type": "logic",
            "question": "In a group of people, everyone who likes pizza also likes cheese. Sarah doesn't like cheese. Does Sarah like pizza?",
            "expected_answer": "No, Sarah does not like pizza. If she did, she would have to like cheese too.",
            "difficulty": "medium"
        }
    ],
    "math_problems": [
        {
            "task_id": 4,
            "task_type": "math",
            "question": "What is 23 × 17?",
            "expected_answer": "391",
            "difficulty": "easy"
        },
        {
            "task_id": 5,
            "task_type": "math",
            "question": "If a train travels 120 km in 2 hours, what is its average speed in km/h?",
            "expected_answer": "60 km/h",
            "difficulty": "easy"
        },
        {
            "task_id": 6,
            "task_type": "math",
            "question": "Solve for x: 2x + 5 = 17",
            "expected_answer": "x = 6",
            "difficulty": "medium"
        }
    ],
    "reasoning_tasks": [
        {
            "task_id": 7,
            "task_type": "reasoning",
            "question": "If it is raining, the ground will be wet. The ground is wet. Does it mean it rained?",
            "expected_answer": "Not necessarily (other causes possible).",
            "difficulty": "medium"
        },
        {
            "task_id": 8,
            "task_type": "reasoning",
            "question": "A company's profits increased by 20% this year. Last year they made $100,000. How much did they make this year?",
            "expected_answer": "$120,000",
            "difficulty": "easy"
        },
        {
            "task_id": 9,
            "task_type": "reasoning",
            "question": "Every bird can fly. Penguins are birds. Can penguins fly?",
            "expected_answer": "This presents a logical contradiction. The premise 'every bird can fly' is actually false, as penguins are flightless birds.",
            "difficulty": "hard"
        }
    ]
}

def load_datasets() -> List[TaskData]:
    """
    Load test datasets from JSON files or embedded data as fallback
    
    Returns:
        List of TaskData objects containing all test cases
    """
    all_tasks = []
    
    # Try to load from JSON files first
    dataset_files = [
        "data/logic_puzzles.json",
        "data/math_problems.json", 
        "data/reasoning_tasks.json"
    ]
    
    loaded_from_files = False
    for file_path in dataset_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data:
                        all_tasks.append(TaskData(**item))
                loaded_from_files = True
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Warning: Could not load {file_path}: {e}")
    
    # Fallback to embedded datasets if files not found
    if not loaded_from_files:
        print("Using embedded datasets as fallback...")
        for dataset_name, tasks in EMBEDDED_DATASETS.items():
            for task_data in tasks:
                all_tasks.append(TaskData(**task_data))
    
    return all_tasks

def get_tasks_by_type(task_type: str) -> List[TaskData]:
    """
    Get tasks filtered by type
    
    Args:
        task_type: Type of task ('logic', 'math', 'reasoning')
        
    Returns:
        List of TaskData objects of the specified type
    """
    all_tasks = load_datasets()
    return [task for task in all_tasks if task.task_type == task_type]

def get_sample_tasks(n_per_type: int = 1) -> List[TaskData]:
    """
    Get sample tasks for testing (n tasks per type)
    
    Args:
        n_per_type: Number of tasks to get per type
        
    Returns:
        List of sample TaskData objects
    """
    sample_tasks = []
    task_types = ["logic", "math", "reasoning"]
    
    for task_type in task_types:
        tasks = get_tasks_by_type(task_type)
        sample_tasks.extend(tasks[:n_per_type])
    
    return sample_tasks
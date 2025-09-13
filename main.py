#!/usr/bin/env python3
"""
Week 3 Assignment: Advanced Prompting Comparison
Main execution script for testing different prompting strategies
"""
import sys
import argparse
from typing import List
from api_client import LLMAPIClient
from prompt_strategies import PromptStrategyRunner
from evaluator import ResponseEvaluator, ResultAnalyzer
from datasets import load_datasets, get_sample_tasks

def setup_argument_parser():
    """Setup command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Compare prompting strategies using real LLM APIs"
    )
    
    parser.add_argument(
        "--provider",
        choices=["gemini", "openai"],
        default="gemini",
        help="API provider to use (default: gemini)"
    )
    
    parser.add_argument(
        "--strategies",
        nargs="+",
        choices=["zero_shot", "few_shot", "cot"],
        default=["zero_shot", "few_shot", "cot"],
        help="Prompting strategies to test (default: all)"
    )
    
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Use sample tasks only (1 per type)"
    )
    
    parser.add_argument(
        "--output",
        help="Output file for detailed results (optional)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser

def display_task_header(task_num: int, total_tasks: int, task):
    """Display header for current task"""
    print(f"\n{'='*60}")
    print(f"TASK {task_num}/{total_tasks}: {task.task_type.upper()}")
    print(f"Question: {task.question}")
    print(f"Expected: {task.expected_answer}")
    print(f"{'='*60}")

def display_strategy_result(result: dict, verbose: bool = False):
    """Display results for a single strategy"""
    task = result["task"]
    strategy = result["strategy"]
    response = result["response"]
    
    print(f"\n--- {strategy.upper()} STRATEGY ---")
    
    if verbose:
        print(f"Prompt: {result['prompt'][:100]}...")
    
    if response.success:
        print(f"Response: {response.response}")
        print(f"Tokens Used: {response.total_tokens}")
    else:
        print(f"ERROR: {response.error_message}")

def run_comparison(args):
    """Run the prompting strategy comparison"""
    print("Initializing Advanced Prompting Strategy Comparison...")
    
    # Initialize components
    api_client = LLMAPIClient()
    strategy_runner = PromptStrategyRunner(api_client)
    evaluator = ResponseEvaluator()
    analyzer = ResultAnalyzer()
    
    # Check API availability
    if not api_client.test_connection(args.provider):
        print(f"WARNING: Could not connect to {args.provider} API")
        print("Proceeding anyway - errors will be logged")
    
    # Load tasks
    if args.sample:
        tasks = get_sample_tasks(n_per_type=1)
        print(f"Using sample tasks: {len(tasks)} tasks loaded")
    else:
        tasks = load_datasets()
        print(f"Using full dataset: {len(tasks)} tasks loaded")
    
    # Run strategies on tasks
    all_results = []
    task_count = 0
    
    for task in tasks:
        task_count += 1
        display_task_header(task_count, len(tasks), task)
        
        for strategy_name in args.strategies:
            try:
                print(f"\nRunning {strategy_name.upper()} strategy...")
                
                # Execute strategy
                result = strategy_runner.run_strategy(
                    strategy_name, task, args.provider
                )
                
                # Display result
                display_strategy_result(result, args.verbose)
                
                # Evaluate result
                test_result = evaluator.evaluate_response(
                    task, result["response"], strategy_name, result["prompt"]
                )
                
                # Display evaluation scores
                print(f"Scores: Correctness={test_result.correctness_score}/3, "
                      f"Clarity={test_result.reasoning_clarity_score}/3, "
                      f"Complete={test_result.completeness_score}/3, "
                      f"Concise={test_result.conciseness_score}/3")
                print(f"Total Score: {test_result.total_score}/12")
                
                all_results.append(test_result)
                
            except Exception as e:
                print(f"ERROR in {strategy_name}: {e}")
                continue
    
    # Generate summary report
    print("\n" + "="*60)
    print("FINAL ANALYSIS")
    print("="*60)
    
    if all_results:
        summary = analyzer.generate_summary_report(all_results)
        print(summary)
        
        # Save detailed results if requested
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(summary)
                    f.write("\n\n## Detailed Results\n\n")
                    for result in all_results:
                        f.write(f"### Task {result.task_id}: {result.prompt_type}\n")
                        f.write(f"**Question**: {result.task_text}\n")
                        f.write(f"**Expected**: {result.expected_answer}\n")
                        f.write(f"**Response**: {result.model_response}\n")
                        f.write(f"**Scores**: {result.total_score}/12\n\n")
                print(f"\nDetailed results saved to: {args.output}")
            except Exception as e:
                print(f"Error saving results: {e}")
    else:
        print("No results to analyze.")
    
    return all_results

def interactive_mode():
    """Run in interactive mode"""
    print("Advanced Prompting Strategy Comparison")
    print("=====================================")
    
    # Initialize API client
    api_client = LLMAPIClient()
    
    # Check available providers
    providers = api_client.get_available_providers()
    if not providers:
        print("ERROR: No API providers available. Check your .env file.")
        return
    
    print(f"Available providers: {', '.join(providers)}")
    
    # Get provider choice
    if len(providers) == 1:
        provider = providers[0]
        print(f"Using {provider} (only available provider)")
    else:
        while True:
            provider = input(f"Choose provider ({'/'.join(providers)}): ").lower()
            if provider in providers:
                break
            print("Invalid choice. Please try again.")
    
    # Test connection
    print(f"Testing {provider} connection...")
    if api_client.test_connection(provider):
        print("Connection successful!")
    else:
        print("Connection failed, but proceeding anyway...")
    
    # Get dataset choice
    while True:
        choice = input("Use sample tasks? (y/n): ").lower()
        if choice in ['y', 'yes']:
            use_sample = True
            break
        elif choice in ['n', 'no']:
            use_sample = False
            break
        print("Please enter 'y' or 'n'")
    
    # Create mock args object
    class Args:
        def __init__(self):
            self.provider = provider
            self.strategies = ["zero_shot", "few_shot", "cot"]
            self.sample = use_sample
            self.output = None
            self.verbose = False
    
    args = Args()
    
    # Run comparison
    return run_comparison(args)

def main():
    """Main entry point"""
    if len(sys.argv) == 1:
        # No arguments provided, run in interactive mode
        try:
            return interactive_mode()
        except KeyboardInterrupt:
            print("\nExiting...")
            return []
    else:
        # Parse command line arguments
        parser = setup_argument_parser()
        args = parser.parse_args()
        return run_comparison(args)

if __name__ == "__main__":
    results = main()
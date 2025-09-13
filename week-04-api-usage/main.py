#!/usr/bin/env python3
"""
Week 4 Assignment: AI News Summarizer & Q&A Tool
"""
import sys
import argparse
from typing import Optional
from api_client import APIClientManager, LLMClient
from summarizer_engine import ArticleSummarizer, SummaryAnalyzer
from qa_engine import ArticleQAEngine, QuestionSuggester, QAAnalyzer
from models import Article, SessionData
from config import SAMPLE_ARTICLE, PERSONALITY_STYLES

def setup_argument_parser():
    """Setup command line argument parser"""
    parser = argparse.ArgumentParser(
        description="AI News Summarizer & Q&A Tool with real API integration"
    )
    
    parser.add_argument(
        "--provider",
        choices=["gemini", "openai"],
        help="API provider to use (default: first available)"
    )
    
    parser.add_argument(
        "--article-file",
        help="Path to text file containing article content"
    )
    
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Temperature for text generation (0.0-1.0, default: 0.7)"
    )
    
    parser.add_argument(
        "--style",
        choices=list(PERSONALITY_STYLES.keys()),
        help="Generate summary in a specific style"
    )
    
    parser.add_argument(
        "--experiments",
        action="store_true",
        help="Run temperature experiments"
    )
    
    parser.add_argument(
        "--qa-only",
        action="store_true",
        help="Skip summarization, go directly to Q&A"
    )
    
    parser.add_argument(
        "--batch-questions",
        nargs="+",
        help="Ask specific questions (non-interactive mode)"
    )
    
    parser.add_argument(
        "--output-file",
        help="Save results to file"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser

def load_article_from_file(file_path: str) -> Article:
    """Load article from text file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Extract title from first line if it looks like a title
        lines = content.split('\\n')
        if len(lines) > 1 and len(lines[0]) < 200 and not lines[0].endswith('.'):
            title = lines[0].strip()
            content = '\\n'.join(lines[1:]).strip()
        else:
            title = f"Article from {file_path}"
        
        return Article(title=title, content=content)
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading article from file: {e}")
        sys.exit(1)

def get_sample_article() -> Article:
    """Get the sample article for testing"""
    return Article(
        title="OpenAI Announces GPT-4 Turbo with Enhanced Capabilities",
        content=SAMPLE_ARTICLE.strip()
    )

def display_article_info(article: Article):
    """Display basic article information"""
    print(f"\\n{'='*60}")
    print(f"ARTICLE: {article.title}")
    print(f"{'='*60}")
    print(f"Length: {article.word_count} words ({article.char_count} characters)")
    
    # Show preview
    preview = article.content[:200] + "..." if len(article.content) > 200 else article.content
    print(f"Preview: {preview}")
    print(f"{'='*60}")

def run_summarization(summarizer: ArticleSummarizer, article: Article, 
                     temperature: float, style: Optional[str] = None):
    """Run summarization with specified parameters"""
    print(f"\\n--- SUMMARIZATION ---")
    
    if style:
        print(f"Generating {style} style summary...")
        result = summarizer.summarize_with_style(article, style, temperature)
        print(f"\\n{style.title()} Style Summary:")
    else:
        print(f"Generating summary (temperature: {temperature})...")
        result = summarizer.summarize(article, temperature)
        print(f"\\nSummary:")
    
    if result.summary.success:
        print(result.summary.content)
        print(f"\\nSummary Stats:")
        print(f"- Length: {result.summary.word_count} words")
        print(f"- Compression ratio: {result.compression_ratio:.1f}x")
        print(f"- Tokens used: {result.summary.tokens_used}")
        print(f"- Model: {result.summary.model}")
    else:
        print(f"Error generating summary: {result.summary.error_message}")
    
    return result

def run_temperature_experiments(summarizer: ArticleSummarizer, article: Article):
    """Run temperature experiments"""
    print(f"\\n--- TEMPERATURE EXPERIMENTS ---")
    print("Testing different temperature settings...")
    
    experiments = summarizer.experiment_with_temperatures(article)
    
    # Display results
    for temp_name, result in experiments.results.items():
        print(f"\\n{temp_name.upper()} (Temperature: {result.temperature_used})")
        print("-" * 40)
        
        if result.summary.success:
            print(result.summary.content)
            print(f"Length: {result.summary.word_count} words | "
                  f"Tokens: {result.summary.tokens_used}")
        else:
            print(f"Error: {result.summary.error_message}")
    
    # Generate analysis
    analyzer = SummaryAnalyzer()
    observations = analyzer.generate_observations_report(experiments)
    
    print(f"\\n--- TEMPERATURE ANALYSIS ---")
    print(observations)
    
    return experiments

def run_qa_session(qa_engine: ArticleQAEngine, article: Article, 
                  batch_questions: Optional[list] = None):
    """Run Q&A session"""
    print(f"\\n--- Q&A SESSION ---")
    
    if batch_questions:
        print(f"Asking {len(batch_questions)} predefined questions...")
        results = qa_engine.ask_multiple_questions(article, batch_questions)
        
        for i, result in enumerate(results, 1):
            print(f"\\nQ{i}: {result.question}")
            if result.answer.success:
                print(f"A{i}: {result.answer.content}")
                print(f"    (Tokens: {result.answer.tokens_used})")
            else:
                print(f"A{i}: Error - {result.answer.error_message}")
    else:
        # Interactive mode
        results = qa_engine.interactive_qa_session(article)
    
    # Generate analysis if we have results
    if results:
        analyzer = QAAnalyzer()
        report = analyzer.generate_qa_report(results)
        print(f"\\n--- Q&A ANALYSIS ---")
        print(report)
    
    return results

def save_session_results(session: SessionData, output_file: str):
    """Save session results to file"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# AI News Summarizer & Q&A Session Results\\n\\n")
            f.write(session.get_session_summary())
            f.write("\\n\\n")
            
            # Write temperature experiment results if available
            if session.summary_experiments.results:
                analyzer = SummaryAnalyzer()
                observations = analyzer.generate_observations_report(session.summary_experiments)
                f.write(observations)
                f.write("\\n\\n")
            
            # Write Q&A results if available
            if session.qa_results:
                qa_analyzer = QAAnalyzer()
                qa_report = qa_analyzer.generate_qa_report(session.qa_results)
                f.write(qa_report)
            
        print(f"\\nResults saved to: {output_file}")
        
    except Exception as e:
        print(f"Error saving results: {e}")

def interactive_mode():
    """Run application in interactive mode"""
    print("AI News Summarizer & Q&A Tool")
    print("==============================")
    
    # Initialize API client manager
    manager = APIClientManager()
    providers = manager.get_available_providers()
    
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
            choice = input(f"Choose provider ({'/'.join(providers)}): ").lower()
            if choice in providers:
                provider = choice
                break
            print("Invalid choice. Please try again.")
    
    # Get client
    client = manager.get_client(provider)
    print(f"\\nTesting {provider} connection...")
    if client.test_connection():
        print("Connection successful!")
    else:
        print("Connection test failed, but proceeding anyway...")
    
    # Initialize components
    summarizer = ArticleSummarizer(client)
    qa_engine = ArticleQAEngine(client)
    
    # Get article
    while True:
        choice = input("\\nUse sample article? (y/n): ").lower()
        if choice in ['y', 'yes']:
            article = get_sample_article()
            break
        elif choice in ['n', 'no']:
            file_path = input("Enter path to article file: ")
            try:
                article = load_article_from_file(file_path)
                break
            except:
                print("Could not load article. Try again.")
        else:
            print("Please enter 'y' or 'n'")
    
    display_article_info(article)
    
    # Initialize session data
    session = SessionData(article=article, summary_experiments=None)
    
    # Main interaction loop
    while True:
        print("\\n" + "="*50)
        print("What would you like to do?")
        print("1. Generate summary")
        print("2. Generate summary with style")
        print("3. Run temperature experiments")
        print("4. Ask questions (interactive)")
        print("5. View article info")
        print("6. Save results and exit")
        print("0. Exit")
        
        try:
            choice = input("\\nYour choice: ").strip()
            
            if choice == "1":
                temp = float(input("Enter temperature (0.0-1.0, default 0.7): ") or "0.7")
                result = run_summarization(summarizer, article, temp)
                if result.summary.success:
                    session.total_tokens_used += result.summary.tokens_used
                    
            elif choice == "2":
                print(f"Available styles: {', '.join(PERSONALITY_STYLES.keys())}")
                style = input("Choose style: ").strip()
                if style in PERSONALITY_STYLES:
                    temp = float(input("Enter temperature (0.0-1.0, default 0.8): ") or "0.8")
                    result = run_summarization(summarizer, article, temp, style)
                    if result.summary.success:
                        session.total_tokens_used += result.summary.tokens_used
                else:
                    print("Invalid style choice.")
                    
            elif choice == "3":
                experiments = run_temperature_experiments(summarizer, article)
                session.summary_experiments = experiments
                for result in experiments.results.values():
                    if result.summary.success:
                        session.total_tokens_used += result.summary.tokens_used
                        
            elif choice == "4":
                qa_results = run_qa_session(qa_engine, article)
                for result in qa_results:
                    session.add_qa_result(result)
                    
            elif choice == "5":
                display_article_info(article)
                
            elif choice == "6":
                filename = input("Enter filename (default: session_results.md): ") or "session_results.md"
                save_session_results(session, filename)
                break
                
            elif choice == "0":
                break
                
            else:
                print("Invalid choice. Please try again.")
                
        except KeyboardInterrupt:
            print("\\nExiting...")
            break
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main entry point"""
    if len(sys.argv) == 1:
        # No arguments, run interactive mode
        try:
            return interactive_mode()
        except KeyboardInterrupt:
            print("\\nExiting...")
            return
    
    # Parse command line arguments
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # Initialize API client
    manager = APIClientManager()
    
    try:
        client = manager.get_client(args.provider)
    except ValueError as e:
        print(f"Error: {e}")
        available = manager.get_available_providers()
        if available:
            print(f"Available providers: {', '.join(available)}")
        return
    
    # Initialize components
    summarizer = ArticleSummarizer(client)
    qa_engine = ArticleQAEngine(client)
    
    # Load article
    if args.article_file:
        article = load_article_from_file(args.article_file)
    else:
        article = get_sample_article()
    
    display_article_info(article)
    
    # Initialize session
    from models import ExperimentResults
    session = SessionData(article=article, summary_experiments=ExperimentResults(article))
    
    # Run operations based on arguments
    if not args.qa_only:
        if args.experiments:
            experiments = run_temperature_experiments(summarizer, article)
            session.summary_experiments = experiments
        elif args.style:
            result = run_summarization(summarizer, article, args.temperature, args.style)
            if result.summary.success:
                session.total_tokens_used += result.summary.tokens_used
        else:
            result = run_summarization(summarizer, article, args.temperature)
            if result.summary.success:
                session.total_tokens_used += result.summary.tokens_used
    
    # Run Q&A if requested
    if args.batch_questions or not (args.experiments or args.style or not args.qa_only):
        qa_results = run_qa_session(qa_engine, article, args.batch_questions)
        for result in qa_results:
            session.add_qa_result(result)
    
    # Save results if requested
    if args.output_file:
        save_session_results(session, args.output_file)
    
    print(f"\\nSession completed. Total tokens used: {session.total_tokens_used}")

if __name__ == "__main__":
    main()
"""
Q&A engine for interactive questioning about articles
"""
import logging
from typing import List, Dict
from api_client import LLMClient
from models import Article, QAResult, APIResponse
from config import PROMPTS

logger = logging.getLogger(__name__)

class ArticleQAEngine:
    """Engine for answering questions about articles"""
    
    def __init__(self, client: LLMClient):
        """
        Initialize Q&A engine
        
        Args:
            client: LLM API client to use
        """
        self.client = client
    
    def ask_question(self, article: Article, question: str, 
                    temperature: float = 0.3) -> QAResult:
        """
        Ask a question about an article
        
        Args:
            article: Article to ask about
            question: Question to ask
            temperature: Sampling temperature (lower for factual answers)
            
        Returns:
            QAResult with question, answer, and metadata
        """
        prompt = PROMPTS["qa"].format(
            question=question,
            article_text=article.content
        )
        
        logger.info(f"Asking question: {question[:50]}...")
        response = self.client.generate_response(prompt, temperature=temperature)
        
        return QAResult(
            question=question,
            answer=response,
            article=article
        )
    
    def ask_multiple_questions(self, article: Article, questions: List[str],
                              temperature: float = 0.3) -> List[QAResult]:
        """
        Ask multiple questions about an article
        
        Args:
            article: Article to ask about
            questions: List of questions to ask
            temperature: Sampling temperature
            
        Returns:
            List of QAResults
        """
        results = []
        
        for i, question in enumerate(questions, 1):
            logger.info(f"Processing question {i}/{len(questions)}")
            
            try:
                result = self.ask_question(article, question, temperature)
                results.append(result)
                
                logger.info(f"Question {i} answered ({result.answer.tokens_used} tokens)")
                
            except Exception as e:
                logger.error(f"Failed to answer question {i}: {e}")
                # Create error response
                error_response = APIResponse(
                    content=f"Error answering question: {e}",
                    model=self.client.get_provider_info()["model"],
                    temperature=temperature,
                    success=False,
                    error_message=str(e)
                )
                error_result = QAResult(
                    question=question,
                    answer=error_response,
                    article=article
                )
                results.append(error_result)
        
        return results
    
    def interactive_qa_session(self, article: Article) -> List[QAResult]:
        """
        Run an interactive Q&A session
        
        Args:
            article: Article to ask about
            
        Returns:
            List of QAResults from the session
        """
        print(f"\\nStarting interactive Q&A session for: {article.title}")
        print(f"Article length: {article.word_count} words")
        print("\\nType 'quit', 'exit', or 'done' to end the session.")
        print("-" * 50)
        
        results = []
        question_count = 0
        
        while True:
            try:
                question = input(f"\\nQuestion {question_count + 1}: ").strip()
                
                if not question:
                    print("Please enter a question.")
                    continue
                
                # Check for exit commands
                if question.lower() in ['quit', 'exit', 'done', 'q']:
                    break
                
                # Ask the question
                result = self.ask_question(article, question)
                
                if result.answer.success:
                    print(f"\\nAnswer: {result.answer.content}")
                    print(f"(Used {result.answer.tokens_used} tokens)")
                else:
                    print(f"\\nError: {result.answer.error_message}")
                
                results.append(result)
                question_count += 1
                
            except KeyboardInterrupt:
                print("\\nSession interrupted by user.")
                break
            except Exception as e:
                print(f"\\nError during Q&A session: {e}")
                break
        
        print(f"\\nQ&A session completed. Asked {len(results)} questions.")
        return results

class QuestionSuggester:
    """Suggests relevant questions about articles"""
    
    def __init__(self, client: LLMClient):
        """
        Initialize question suggester
        
        Args:
            client: LLM API client to use
        """
        self.client = client
    
    def suggest_questions(self, article: Article, num_questions: int = 5) -> List[str]:
        """
        Suggest relevant questions about an article
        
        Args:
            article: Article to generate questions for
            num_questions: Number of questions to suggest
            
        Returns:
            List of suggested questions
        """
        prompt = f"""Based on the following article, suggest {num_questions} insightful questions that would help readers better understand the key points, implications, or details.

Article: {article.content}

Please provide exactly {num_questions} questions, each on a new line, without numbering:"""
        
        logger.info(f"Generating {num_questions} question suggestions")
        
        try:
            response = self.client.generate_response(prompt, temperature=0.7)
            
            if response.success:
                # Parse questions from response
                questions = []
                for line in response.content.split('\\n'):
                    line = line.strip()
                    if line and not line.isdigit():
                        # Remove common prefixes
                        for prefix in ['- ', '• ', '* ', 'Q: ', 'Question: ']:
                            if line.startswith(prefix):
                                line = line[len(prefix):]
                        
                        # Remove trailing question marks if doubled
                        if line.endswith('??'):
                            line = line[:-1]
                        
                        questions.append(line)
                
                # Return up to requested number of questions
                return questions[:num_questions]
            else:
                logger.error(f"Failed to generate questions: {response.error_message}")
                return self._get_default_questions()
                
        except Exception as e:
            logger.error(f"Error generating question suggestions: {e}")
            return self._get_default_questions()
    
    def _get_default_questions(self) -> List[str]:
        """Return default questions when generation fails"""
        return [
            "What are the main points discussed in this article?",
            "What are the key implications or consequences mentioned?",
            "Who are the main people or organizations involved?",
            "What evidence or data is presented to support the claims?",
            "What questions or concerns are raised by this information?"
        ]

class QAAnalyzer:
    """Analyzer for Q&A session results"""
    
    def __init__(self):
        """Initialize analyzer"""
        pass
    
    def analyze_qa_session(self, qa_results: List[QAResult]) -> Dict:
        """
        Analyze Q&A session results
        
        Args:
            qa_results: List of Q&A results to analyze
            
        Returns:
            Dictionary with analysis data
        """
        if not qa_results:
            return {"error": "No Q&A results to analyze"}
        
        successful_results = [r for r in qa_results if r.answer.success]
        
        analysis = {
            "total_questions": len(qa_results),
            "successful_answers": len(successful_results),
            "failed_answers": len(qa_results) - len(successful_results),
            "total_tokens_used": sum(r.answer.tokens_used for r in qa_results),
            "average_answer_length": 0,
            "question_types": self._classify_questions(qa_results),
            "longest_answer": "",
            "shortest_answer": ""
        }
        
        if successful_results:
            answer_lengths = [r.answer.word_count for r in successful_results]
            analysis["average_answer_length"] = sum(answer_lengths) / len(answer_lengths)
            
            # Find longest and shortest answers
            longest_result = max(successful_results, key=lambda r: r.answer.word_count)
            shortest_result = min(successful_results, key=lambda r: r.answer.word_count)
            
            analysis["longest_answer"] = {
                "question": longest_result.question,
                "answer_preview": longest_result.answer.content[:100] + "...",
                "word_count": longest_result.answer.word_count
            }
            
            analysis["shortest_answer"] = {
                "question": shortest_result.question,
                "answer_preview": shortest_result.answer.content[:100] + "...",
                "word_count": shortest_result.answer.word_count
            }
        
        return analysis
    
    def _classify_questions(self, qa_results: List[QAResult]) -> Dict[str, int]:
        """
        Classify questions by type based on keywords
        
        Args:
            qa_results: Q&A results to classify
            
        Returns:
            Dictionary with question type counts
        """
        types = {
            "what": 0,
            "how": 0,
            "why": 0,
            "when": 0,
            "where": 0,
            "who": 0,
            "other": 0
        }
        
        for result in qa_results:
            question_lower = result.question.lower()
            
            classified = False
            for question_type in types.keys():
                if question_type != "other" and question_lower.startswith(question_type):
                    types[question_type] += 1
                    classified = True
                    break
            
            if not classified:
                types["other"] += 1
        
        return types
    
    def generate_qa_report(self, qa_results: List[QAResult]) -> str:
        """
        Generate human-readable Q&A session report
        
        Args:
            qa_results: Q&A results to report on
            
        Returns:
            Formatted Q&A session report
        """
        if not qa_results:
            return "No Q&A results to report."
        
        analysis = self.analyze_qa_session(qa_results)
        
        report = "# Q&A Session Report\\n\\n"
        report += f"**Total Questions Asked**: {analysis['total_questions']}\\n"
        report += f"**Successful Answers**: {analysis['successful_answers']}\\n"
        
        if analysis['failed_answers'] > 0:
            report += f"**Failed Answers**: {analysis['failed_answers']}\\n"
        
        report += f"**Total Tokens Used**: {analysis['total_tokens_used']}\\n"
        
        if analysis['successful_answers'] > 0:
            report += f"**Average Answer Length**: {analysis['average_answer_length']:.1f} words\\n\\n"
            
            report += "## Question Types\\n\\n"
            for q_type, count in analysis["question_types"].items():
                if count > 0:
                    report += f"- **{q_type.title()}**: {count}\\n"
            
            if "longest_answer" in analysis:
                report += f"\\n## Longest Answer ({analysis['longest_answer']['word_count']} words)\\n"
                report += f"**Question**: {analysis['longest_answer']['question']}\\n"
                report += f"**Answer**: {analysis['longest_answer']['answer_preview']}\\n\\n"
            
            if "shortest_answer" in analysis:
                report += f"## Shortest Answer ({analysis['shortest_answer']['word_count']} words)\\n"
                report += f"**Question**: {analysis['shortest_answer']['question']}\\n"
                report += f"**Answer**: {analysis['shortest_answer']['answer_preview']}\\n"
        
        return report
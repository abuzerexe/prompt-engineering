"""
Summarization engine for news articles
"""
import logging
from typing import Dict, List
from api_client import LLMClient
from models import Article, APIResponse, SummaryResult, ExperimentResults
from config import PROMPTS, TEMPERATURE_SETTINGS, PERSONALITY_STYLES

logger = logging.getLogger(__name__)

class ArticleSummarizer:
    """Engine for summarizing news articles with different parameters"""
    
    def __init__(self, client: LLMClient):
        """
        Initialize summarizer
        
        Args:
            client: LLM API client to use
        """
        self.client = client
    
    def summarize(self, article: Article, temperature: float = 0.7) -> SummaryResult:
        """
        Generate summary for an article
        
        Args:
            article: Article to summarize
            temperature: Sampling temperature
            
        Returns:
            SummaryResult with summary and metadata
        """
        prompt = PROMPTS["summarize"].format(article_text=article.content)
        
        logger.info(f"Generating summary with temperature {temperature}")
        response = self.client.generate_response(prompt, temperature=temperature)
        
        return SummaryResult(
            original_article=article,
            summary=response,
            temperature_used=temperature
        )
    
    def summarize_with_style(self, article: Article, style: str, 
                           temperature: float = 0.8) -> SummaryResult:
        """
        Generate summary in a specific style (pirate, comedian, etc.)
        
        Args:
            article: Article to summarize
            style: Style to use (must be in PERSONALITY_STYLES)
            temperature: Sampling temperature
            
        Returns:
            SummaryResult with styled summary
        """
        if style not in PERSONALITY_STYLES:
            raise ValueError(f"Unknown style: {style}. Available: {list(PERSONALITY_STYLES.keys())}")
        
        style_description = PERSONALITY_STYLES[style]
        prompt = PROMPTS["style_summary"].format(
            article_text=article.content,
            style=style_description
        )
        
        logger.info(f"Generating {style} style summary")
        response = self.client.generate_response(prompt, temperature=temperature)
        
        return SummaryResult(
            original_article=article,
            summary=response,
            temperature_used=temperature
        )
    
    def experiment_with_temperatures(self, article: Article) -> ExperimentResults:
        """
        Run temperature experiments on an article
        
        Args:
            article: Article to experiment with
            
        Returns:
            ExperimentResults containing all temperature experiment results
        """
        logger.info("Starting temperature experiments")
        experiments = ExperimentResults(article=article)
        
        for temp_name, temp_value in TEMPERATURE_SETTINGS.items():
            logger.info(f"Running experiment: {temp_name} (temperature={temp_value})")
            
            try:
                result = self.summarize(article, temperature=temp_value)
                experiments.add_result(temp_name, result)
                
                logger.info(f"{temp_name} summary generated ({result.summary.tokens_used} tokens)")
                
            except Exception as e:
                logger.error(f"Failed to generate {temp_name} summary: {e}")
                # Create error response
                error_response = APIResponse(
                    content=f"Error generating summary: {e}",
                    model=self.client.get_provider_info()["model"],
                    temperature=temp_value,
                    success=False,
                    error_message=str(e)
                )
                error_result = SummaryResult(
                    original_article=article,
                    summary=error_response,
                    temperature_used=temp_value
                )
                experiments.add_result(temp_name, error_result)
        
        logger.info("Temperature experiments completed")
        return experiments
    
    def batch_summarize(self, articles: List[Article], 
                       temperature: float = 0.7) -> List[SummaryResult]:
        """
        Summarize multiple articles
        
        Args:
            articles: List of articles to summarize
            temperature: Sampling temperature to use
            
        Returns:
            List of SummaryResults
        """
        results = []
        
        for i, article in enumerate(articles, 1):
            logger.info(f"Summarizing article {i}/{len(articles)}: {article.title}")
            
            try:
                result = self.summarize(article, temperature)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to summarize article {i}: {e}")
                # Add error result
                error_response = APIResponse(
                    content=f"Error: {e}",
                    model=self.client.get_provider_info()["model"],
                    temperature=temperature,
                    success=False,
                    error_message=str(e)
                )
                error_result = SummaryResult(
                    original_article=article,
                    summary=error_response,
                    temperature_used=temperature
                )
                results.append(error_result)
        
        return results

class SummaryAnalyzer:
    """Analyzer for comparing and evaluating summaries"""
    
    def __init__(self):
        """Initialize analyzer"""
        pass
    
    def analyze_temperature_effects(self, experiments: ExperimentResults) -> Dict:
        """
        Analyze the effects of different temperature settings
        
        Args:
            experiments: Temperature experiment results
            
        Returns:
            Dictionary with analysis results
        """
        analysis = {
            "original_word_count": experiments.article.word_count,
            "temperature_results": {},
            "observations": []
        }
        
        for temp_name, result in experiments.results.items():
            if result.summary.success:
                analysis["temperature_results"][temp_name] = {
                    "temperature": result.temperature_used,
                    "word_count": result.summary.word_count,
                    "tokens_used": result.summary.tokens_used,
                    "compression_ratio": result.compression_ratio,
                    "summary_preview": result.summary.content[:100] + "..."
                }
            else:
                analysis["temperature_results"][temp_name] = {
                    "temperature": result.temperature_used,
                    "error": result.summary.error_message
                }
        
        # Generate observations
        successful_results = [r for r in experiments.results.values() if r.summary.success]
        
        if len(successful_results) >= 2:
            word_counts = [r.summary.word_count for r in successful_results]
            min_words = min(word_counts)
            max_words = max(word_counts)
            
            analysis["observations"].append(
                f"Summary lengths varied from {min_words} to {max_words} words"
            )
            
            # Compare deterministic vs creative
            if "deterministic" in experiments.results and "creative" in experiments.results:
                det_result = experiments.results["deterministic"]
                cre_result = experiments.results["creative"]
                
                if det_result.summary.success and cre_result.summary.success:
                    if det_result.summary.word_count < cre_result.summary.word_count:
                        analysis["observations"].append(
                            "Lower temperature (deterministic) produced more concise summaries"
                        )
                    elif det_result.summary.word_count > cre_result.summary.word_count:
                        analysis["observations"].append(
                            "Higher temperature (creative) produced more concise summaries"
                        )
        
        return analysis
    
    def compare_summaries(self, results: List[SummaryResult]) -> Dict:
        """
        Compare multiple summary results
        
        Args:
            results: List of summary results to compare
            
        Returns:
            Dictionary with comparison data
        """
        if not results:
            return {"error": "No results to compare"}
        
        successful_results = [r for r in results if r.summary.success]
        
        if not successful_results:
            return {"error": "No successful results to compare"}
        
        comparison = {
            "total_summaries": len(results),
            "successful_summaries": len(successful_results),
            "average_compression_ratio": sum(r.compression_ratio for r in successful_results) / len(successful_results),
            "average_word_count": sum(r.summary.word_count for r in successful_results) / len(successful_results),
            "total_tokens_used": sum(r.summary.tokens_used for r in successful_results),
            "temperature_range": {
                "min": min(r.temperature_used for r in successful_results),
                "max": max(r.temperature_used for r in successful_results)
            }
        }
        
        return comparison
    
    def generate_observations_report(self, experiments: ExperimentResults) -> str:
        """
        Generate human-readable observations report
        
        Args:
            experiments: Temperature experiment results
            
        Returns:
            Formatted observations report
        """
        analysis = self.analyze_temperature_effects(experiments)
        
        report = "# Temperature Experiment Observations\n\n"
        report += f"**Original Article**: {experiments.article.title}\n"
        report += f"**Original Length**: {analysis['original_word_count']} words\n\n"
        
        report += "## Results by Temperature\n\n"
        
        for temp_name, data in analysis["temperature_results"].items():
            if "error" in data:
                report += f"### {temp_name.title()} (Temperature: {data['temperature']})\n"
                report += f"**Status**: Error - {data['error']}\n\n"
            else:
                report += f"### {temp_name.title()} (Temperature: {data['temperature']})\n"
                report += f"**Length**: {data['word_count']} words\n"
                report += f"**Compression**: {data['compression_ratio']:.1f}x\n"
                report += f"**Tokens Used**: {data['tokens_used']}\n"
                report += f"**Preview**: {data['summary_preview']}\n\n"
        
        if analysis["observations"]:
            report += "## Key Observations\n\n"
            for obs in analysis["observations"]:
                report += f"- {obs}\n"
        
        return report
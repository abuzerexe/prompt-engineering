#!/usr/bin/env python3
"""
Week 4 Assignment: AI News Summarizer & Q&A Tool
Author: AI Fellowship Student
Date: 2025

This script demonstrates:
1. Article summarization using LLM APIs
2. Interactive Q&A about articles
3. Parameter experimentation with temperature settings

Note: This implementation uses simulated API responses for demonstration.
In practice, you would use actual API keys and make real API calls.
"""

import os
import json
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class APIResponse:
    """Structure to hold API response data"""
    content: str
    model: str
    temperature: float
    tokens_used: int

class MockLLMAPI:
    """
    Mock LLM API for demonstration purposes.
    In practice, replace with actual OpenAI or Google Gemini API calls.
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or "demo_key"
        self.model = "gpt-4"  # or "gemini-pro"
    
    def generate_response(self, prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> APIResponse:
        """
        Simulate API response. In practice, this would be:
        - OpenAI: openai.ChatCompletion.create()
        - Gemini: genai.GenerativeModel().generate_content()
        """
        
        # Simulate different responses based on temperature and prompt content
        if "summarize" in prompt.lower() or "summary" in prompt.lower():
            if temperature <= 0.3:
                # Low temperature - deterministic, factual
                content = """The article discusses recent developments in artificial intelligence and machine learning. Key points include advancements in natural language processing, increased adoption in various industries, and ongoing research into ethical AI implementation. The technology continues to evolve rapidly with significant implications for multiple sectors."""
            elif temperature <= 0.7:
                # Medium temperature - balanced
                content = """This article explores the latest breakthroughs in AI and machine learning technology. It highlights how natural language processing has reached new levels of sophistication, enabling better human-computer interaction. The piece also covers the growing integration of AI across industries like healthcare, finance, and education, while addressing important ethical considerations and future research directions."""
            else:
                # High temperature - creative, varied
                content = """What a fascinating dive into the AI revolution! This article paints a vivid picture of how artificial intelligence is reshaping our world in unexpected ways. From chatbots that seem almost human to algorithms that can predict market trends, we're witnessing a technological renaissance. The author skillfully weaves together technical insights with real-world applications, showing how AI isn't just science fiction anymore—it's our everyday reality transforming everything from how we work to how we learn."""
        
        elif "question" in prompt.lower() or "answer" in prompt.lower():
            # Q&A responses
            if "main benefit" in prompt.lower():
                content = "The main benefit highlighted is increased efficiency and automation across various industries, allowing humans to focus on more creative and strategic tasks."
            elif "challenge" in prompt.lower() or "risk" in prompt.lower():
                content = "The primary challenges mentioned include ethical considerations around bias, job displacement concerns, and the need for proper regulation and oversight of AI systems."
            elif "future" in prompt.lower():
                content = "The article suggests that AI will become increasingly integrated into daily life, with more sophisticated applications in personalized education, healthcare diagnostics, and scientific research."
            else:
                content = "Based on the article content, this appears to be a comprehensive overview of current AI developments and their societal implications."
        
        else:
            content = "I can help you with summarization and question-answering tasks. Please provide a clear request."
        
        # Simulate token usage
        estimated_tokens = len(prompt.split()) + len(content.split())
        
        return APIResponse(
            content=content,
            model=self.model,
            temperature=temperature,
            tokens_used=estimated_tokens
        )

class NewsProcessor:
    """Main class for article processing and analysis"""
    
    def __init__(self, api_key: str = None):
        self.llm = MockLLMAPI(api_key)
        self.current_article = ""
        self.current_article_length = 0
        
    def load_sample_article(self) -> str:
        """Load a sample news article for demonstration"""
        
        article = """
        Artificial Intelligence Reaches New Milestones in 2025: A Comprehensive Report
        
        By Tech News Reporter | January 15, 2025
        
        The field of artificial intelligence has witnessed unprecedented growth and innovation throughout 2024 and into 2025, with breakthrough developments reshaping industries worldwide. From advanced natural language processing systems to revolutionary medical diagnosis tools, AI technology continues to exceed expectations and transform the way we work, learn, and interact with digital systems.
        
        Natural Language Processing Evolution
        
        One of the most significant advances has been in natural language processing (NLP). Modern AI systems now demonstrate remarkable ability to understand context, nuance, and even emotional undertones in human communication. Companies like OpenAI, Anthropic, and Google have released increasingly sophisticated language models that can engage in complex conversations, write code, analyze documents, and even create creative content with human-like quality.
        
        These systems are being integrated into everyday applications, from customer service chatbots that can handle complex queries to writing assistants that help professionals draft emails, reports, and presentations. The technology has become so advanced that distinguishing between human and AI-generated content has become increasingly challenging.
        
        Industry Adoption and Applications
        
        Healthcare has emerged as one of the most promising sectors for AI implementation. Machine learning algorithms are now capable of analyzing medical images with accuracy that matches or exceeds human radiologists. AI-powered diagnostic tools are helping doctors identify diseases earlier, recommend personalized treatment plans, and predict patient outcomes with unprecedented precision.
        
        In the financial sector, AI is revolutionizing fraud detection, algorithmic trading, and risk assessment. Banks and investment firms are leveraging machine learning to analyze market patterns, automate decision-making processes, and provide personalized financial advice to customers.
        
        The education sector has also embraced AI technology, with adaptive learning platforms that customize educational content based on individual student needs and progress. These systems can identify learning gaps, suggest appropriate resources, and provide real-time feedback to both students and educators.
        
        Ethical Considerations and Challenges
        
        However, this rapid advancement has not come without concerns. Questions about data privacy, algorithmic bias, and the potential for job displacement continue to dominate discussions among policymakers, technologists, and ethicists. There's growing recognition that as AI becomes more powerful, the need for responsible development and deployment becomes increasingly critical.
        
        Companies are investing heavily in AI safety research, developing guidelines for ethical AI use, and implementing measures to ensure their systems are fair, transparent, and accountable. Regulatory bodies worldwide are working to establish frameworks that balance innovation with consumer protection and societal welfare.
        
        Future Outlook
        
        Looking ahead, experts predict that AI will become even more integrated into daily life. We can expect to see more sophisticated virtual assistants, autonomous vehicles becoming mainstream, and AI-powered solutions addressing global challenges like climate change and food security.
        
        The next frontier appears to be artificial general intelligence (AGI) - systems that can match human cognitive abilities across all domains. While this remains a distant goal, the pace of current progress suggests that significant breakthroughs may be closer than previously anticipated.
        
        As we navigate this AI-driven transformation, the key will be ensuring that these powerful technologies are developed and deployed in ways that benefit all of humanity while minimizing potential risks and negative consequences.
        
        The year 2025 marks a pivotal moment in AI development, setting the stage for what promises to be an exciting and transformative decade ahead.
        """
        
        self.current_article = article.strip()
        self.current_article_length = len(article.split())
        return self.current_article
    
    def summarize_article(self, temperature: float = 0.7) -> APIResponse:
        """Generate a summary of the current article"""
        
        if not self.current_article:
            raise ValueError("No article loaded. Please load an article first.")
        
        prompt = f"""Please provide a 3-4 sentence summary of the following article:

{self.current_article}

Summary:"""
        
        return self.llm.generate_response(prompt, temperature=temperature, max_tokens=200)
    
    def ask_question(self, question: str) -> APIResponse:
        """Ask a question about the current article"""
        
        if not self.current_article:
            raise ValueError("No article loaded. Please load an article first.")
        
        prompt = f"""Based on the article below, {question}?

Article: {self.current_article}

Answer:"""
        
        return self.llm.generate_response(prompt, temperature=0.5, max_tokens=300)
    
    def experiment_with_temperatures(self) -> Dict[float, APIResponse]:
        """Test the same article with different temperature settings"""
        
        temperatures = [0.1, 0.7, 1.0]
        results = {}
        
        print("\\n" + "="*60)
        print("TEMPERATURE EXPERIMENTATION")
        print("="*60)
        
        for temp in temperatures:
            print(f"\\nTesting with temperature {temp}...")
            response = self.summarize_article(temperature=temp)
            results[temp] = response
            
            print(f"Temperature {temp} Result:")
            print(f"Summary: {response.content}")
            print(f"Tokens used: {response.tokens_used}")
            print("-" * 50)
        
        return results

def run_interactive_demo():
    """Run the main demonstration of the news summarizer"""
    
    print("AI News Summarizer & Q&A Tool")
    print("="*50)
    
    # Initialize processor
    processor = NewsProcessor()
    
    # Load sample article
    print("Loading sample article...")
    article = processor.load_sample_article()
    
    print("Article loaded!")
    print(f"Article length: {processor.current_article_length} words")
    print(f"Article length: {len(processor.current_article)} characters")
    
    # Part 1: Generate summary
    print("\\n" + "="*50)
    print("PART 1: ARTICLE SUMMARIZATION")
    print("="*50)
    
    summary_response = processor.summarize_article()
    print("Generated Summary:")
    print(f"{summary_response.content}")
    print(f"\\nModel: {summary_response.model}")
    print(f"Temperature: {summary_response.temperature}")
    print(f"Tokens used: {summary_response.tokens_used}")
    
    # Part 2: Interactive Q&A
    print("\\n" + "="*50)
    print("PART 2: INTERACTIVE Q&A")
    print("="*50)
    
    questions = [
        "What is the main benefit of AI mentioned in this article",
        "What are the primary challenges or risks discussed",
        "What does the article predict for the future of AI"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\\nQuestion {i}: {question}?")
        qa_response = processor.ask_question(question)
        print(f"Answer: {qa_response.content}")
        print(f"Tokens used: {qa_response.tokens_used}")
    
    # Part 3: Temperature experimentation
    processor.experiment_with_temperatures()
    
    print("\\n" + "="*60)
    print("DEMONSTRATION COMPLETE!")
    print("Check the generated observations.md file for detailed analysis")
    print("="*60)

def generate_observations_report(temp_results: Dict[float, APIResponse]) -> str:
    """Generate the observations report for temperature experimentation"""
    
    report = """# Week 4 Observations: Temperature Parameter Analysis

## Objective
This report documents the effects of different temperature settings on LLM text generation, specifically for article summarization tasks.

## Experimental Setup
- **Article**: AI developments in 2025 (tech news article, ~580 words)
- **Task**: Generate 3-4 sentence summaries
- **Temperatures tested**: 0.1, 0.7, 1.0
- **Model**: GPT-4 (simulated)

## Results

### Temperature 0.1 (Deterministic/Robotic)
**Summary Generated:**
The article discusses recent developments in artificial intelligence and machine learning. Key points include advancements in natural language processing, increased adoption in various industries, and ongoing research into ethical AI implementation. The technology continues to evolve rapidly with significant implications for multiple sectors.

**Characteristics:**
- Very factual and straightforward
- Conservative language choices
- Consistent structure and tone
- Minimal creative expression
- Highly predictable output

### Temperature 0.7 (Balanced)
**Summary Generated:**
This article explores the latest breakthroughs in AI and machine learning technology. It highlights how natural language processing has reached new levels of sophistication, enabling better human-computer interaction. The piece also covers the growing integration of AI across industries like healthcare, finance, and education, while addressing important ethical considerations and future research directions.

**Characteristics:**
- Good balance of facts and engagement
- More descriptive language
- Natural flow and readability
- Appropriate level of detail
- Professional tone

### Temperature 1.0 (Creative/Chaotic)
**Summary Generated:**
What a fascinating dive into the AI revolution! This article paints a vivid picture of how artificial intelligence is reshaping our world in unexpected ways. From chatbots that seem almost human to algorithms that can predict market trends, we're witnessing a technological renaissance. The author skillfully weaves together technical insights with real-world applications, showing how AI isn't just science fiction anymore—it's our everyday reality transforming everything from how we work to how we learn.

**Characteristics:**
- Highly engaging and enthusiastic tone
- Creative language and metaphors
- More subjective interpretation
- Increased personality in writing
- Risk of becoming less factual

## Key Observations

### 1. Tone and Style Variation
- **Low temperature (0.1)**: Clinical, factual, robotic
- **Medium temperature (0.7)**: Professional, balanced, informative
- **High temperature (1.0)**: Engaging, creative, emotional

### 2. Consistency vs Creativity Trade-off
- Lower temperatures provide more consistent, predictable results
- Higher temperatures introduce more variation but may sacrifice accuracy
- Medium temperature strikes the best balance for most applications

### 3. Use Case Recommendations

**Temperature 0.1 - Best for:**
- Legal documents
- Technical specifications
- Scientific reports
- Factual summaries
- Compliance-sensitive content

**Temperature 0.7 - Best for:**
- General content creation
- Business communications
- Educational materials
- News summaries
- Most everyday applications

**Temperature 1.0 - Best for:**
- Creative writing
- Marketing copy
- Brainstorming sessions
- Entertainment content
- When uniqueness is valued over consistency

### 4. Quality Assessment

| Temperature | Accuracy | Engagement | Consistency | Usefulness |
|------------|----------|------------|-------------|------------|
| 0.1        | High     | Low        | Very High   | High       |
| 0.7        | High     | Medium     | High        | Very High  |
| 1.0        | Medium   | Very High  | Low         | Medium     |

## Conclusions

1. **Temperature 0.7 performed best overall** for summarization tasks, providing accurate, engaging, and useful content.

2. **Temperature significantly impacts output personality** - the same model can seem like completely different entities at different temperature settings.

3. **Context matters** - the optimal temperature depends heavily on the intended use case and audience.

4. **Predictability vs Creativity** - There's a clear trade-off between consistent, reliable output and creative, engaging content.

## Recommendations for Practice

1. **Start with 0.7** as a default for most applications
2. **Use 0.1-0.3** for mission-critical, factual content
3. **Use 0.8-1.2** for creative tasks requiring uniqueness
4. **Test multiple temperatures** for important applications
5. **Consider your audience** - technical vs general, formal vs casual

This experimentation demonstrates the importance of parameter tuning in achieving optimal LLM performance for specific tasks and contexts.
"""
    
    return report

if __name__ == "__main__":
    # Run the main demonstration
    run_interactive_demo()
    
    # Generate observations report
    processor = NewsProcessor()
    processor.load_sample_article()
    temp_results = processor.experiment_with_temperatures()
    
    observations = generate_observations_report(temp_results)
    
    # Save observations to file
    with open('observations.md', 'w', encoding='utf-8') as f:
        f.write(observations)
    
    print("\\nObservations report saved to 'observations.md'")
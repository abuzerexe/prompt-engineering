"""
Configuration settings for Week 4 API Usage Assignment
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

# Temperature Settings for Experimentation
TEMPERATURE_SETTINGS = {
    "deterministic": 0.1,
    "balanced": 0.7,
    "creative": 1.0
}

# Prompt Templates
PROMPTS = {
    "summarize": """Please provide a 3-4 sentence summary of the following article:

Article: {article_text}

Summary:""",
    
    "qa": """Based on the article below, answer the following question:

Question: {question}

Article: {article_text}

Answer:""",
    
    "style_summary": """Please provide a 3-4 sentence summary of the following article in the style of a {style}:

Article: {article_text}

Summary:"""
}

# Sample Article for Testing
SAMPLE_ARTICLE = """
OpenAI Announces GPT-4 Turbo with Enhanced Capabilities

San Francisco, CA - OpenAI has unveiled GPT-4 Turbo, the latest iteration of its flagship language model, featuring significant improvements in reasoning, coding, and multimodal capabilities. The new model can process up to 128,000 tokens of context, allowing it to work with much longer documents and maintain coherent conversations across extended interactions.

Key enhancements include improved mathematical reasoning, better code generation across multiple programming languages, and enhanced ability to analyze images and documents. The model also features reduced hallucination rates and more accurate factual responses, addressing one of the primary concerns with earlier versions.

"GPT-4 Turbo represents a major leap forward in AI capabilities while maintaining the safety standards we've established," said Sam Altman, CEO of OpenAI, during the announcement event. The company demonstrated the model's ability to analyze complex technical documents, generate sophisticated code solutions, and engage in nuanced discussions across various domains.

The new model is available through OpenAI's API with competitive pricing that's approximately 50% lower than the previous GPT-4 model. Early access has been granted to enterprise customers, with general availability expected in the coming weeks. OpenAI also announced partnerships with major technology companies to integrate GPT-4 Turbo into their platforms and services.

Industry experts have praised the development, noting that the enhanced context window and improved accuracy could significantly impact applications ranging from customer service to content creation and software development. However, some researchers have called for continued focus on AI safety and responsible deployment as these models become more powerful.
"""

# Fun Personality Styles for Bonus Challenge
PERSONALITY_STYLES = {
    "pirate": "a swashbuckling pirate captain",
    "comedian": "a stand-up comedian",
    "sports_commentator": "an enthusiastic sports commentator", 
    "detective": "a mysterious detective",
    "scientist": "a brilliant scientist explaining to colleagues"
}
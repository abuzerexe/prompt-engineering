# Week 4: AI News Summarizer & Q&A Tool

## Overview
A comprehensive news summarization and Q&A tool built with real LLM API integration. This modular implementation demonstrates temperature experimentation, interactive questioning, and multiple interaction modes.

## Features

### Core Functionality
- **Article Summarization**: Generate 3-4 sentence summaries using real LLM APIs
- **Interactive Q&A**: Ask questions about articles and get intelligent responses
- **Temperature Experiments**: Compare outputs with different creativity settings
- **Real API Integration**: Uses actual Gemini and OpenAI APIs (not mocks)

### Advanced Features
- **Personality Styles**: Generate summaries in fun styles (pirate, comedian, detective, etc.)
- **Web Article Extraction**: Extract content directly from URLs
- **Question Suggestions**: AI-generated relevant questions about articles
- **Session Management**: Track tokens, save results, comprehensive analytics
- **CLI Interface**: Both interactive and command-line modes

## File Structure

### Core Implementation
- `main.py` - Main application with interactive and CLI modes
- `api_client.py` - Unified API client for Gemini and OpenAI
- `summarizer_engine.py` - Article summarization with temperature experiments
- `qa_engine.py` - Q&A functionality and question suggestion
- `models.py` - Data models and structures
- `config.py` - Configuration and constants

### Advanced Tools
- `cli_tool.py` - Enhanced CLI with URL extraction and advanced features
- `.env` - API credentials (ignored by git)

### Generated Files
- `observations.md` - Temperature experiment observations (auto-generated)
- Session result files (user-specified)

## Setup

### Prerequisites
```bash
pip install python-dotenv openai google-genai requests
```

### API Credentials
Create a `.env` file with your API keys:
```
GEMINI_API_KEY="your_gemini_api_key"
OPEN_ROUTER_KEY="your_openrouter_api_key"
```

## Usage

### Interactive Mode (Recommended)
```bash
cd assignments_solutions/week-04-api-usage
python main.py
```

### Command Line Mode
```bash
# Basic summarization
python main.py --provider gemini --temperature 0.7

# Temperature experiments
python main.py --experiments --output-file results.md

# Style-based summary
python main.py --style pirate --temperature 0.8

# Q&A with specific questions
python main.py --batch-questions "What is the main topic?" "Who are the key people mentioned?"

# Custom article from file
python main.py --article-file my_article.txt --qa-only
```

### Advanced CLI Tool
```bash
python cli_tool.py
```
Features:
- URL article extraction
- Interactive menus
- Suggested questions
- Multiple personality styles
- Session management

## Supported Models
- **Gemini**: `gemini-2.5-flash` (default)
- **OpenAI**: `openai/gpt-4o` (via OpenRouter)

## Temperature Settings
- **Deterministic (0.1)**: Factual, consistent summaries
- **Balanced (0.7)**: Good mix of accuracy and creativity
- **Creative (1.0)**: More varied, potentially creative outputs

## Personality Styles
- **Pirate**: Swashbuckling captain style
- **Comedian**: Stand-up comedian humor
- **Sports Commentator**: Enthusiastic sports style
- **Detective**: Mysterious detective tone
- **Scientist**: Academic, technical explanations

## Example Session

```
AI News Summarizer & Q&A Tool
==============================
Available providers: gemini, openai
Using gemini (only available provider)

Testing gemini connection...
✓ Connection successful!

============================================================
ARTICLE: OpenAI Announces GPT-4 Turbo with Enhanced Capabilities
============================================================
Length: 286 words (1847 characters)

--- SUMMARIZATION ---
Generating summary (temperature: 0.7)...

Summary:
OpenAI has unveiled GPT-4 Turbo, featuring significant improvements in reasoning, coding, and multimodal capabilities with a 128,000 token context window. The model offers reduced hallucination rates, enhanced accuracy, and is available at 50% lower pricing than the previous GPT-4 model. Early access has been granted to enterprise customers, with general availability expected soon, as the company partners with major technology firms for platform integration.

Summary Stats:
- Length: 65 words
- Compression ratio: 4.4x
- Tokens used: 420
- Model: Gemini

--- Q&A SESSION ---
Starting interactive Q&A session for: OpenAI Announces GPT-4 Turbo with Enhanced Capabilities
Article length: 286 words

Type 'quit', 'exit', or 'done' to end the session.
--------------------------------------------------

Question 1: What are the key improvements in GPT-4 Turbo?

Answer: The key improvements in GPT-4 Turbo include enhanced reasoning capabilities, better code generation across multiple programming languages, improved mathematical reasoning, enhanced ability to analyze images and documents, and reduced hallucination rates with more accurate factual responses. Additionally, it features a significantly expanded context window of up to 128,000 tokens.
(Used 156 tokens)
```

## Architecture

### Modular Design
The application follows a clean modular architecture:

1. **API Layer** (`api_client.py`): Unified interface for different LLM providers
2. **Engine Layer** (`summarizer_engine.py`, `qa_engine.py`): Core business logic
3. **Model Layer** (`models.py`): Data structures and validation
4. **Interface Layer** (`main.py`, `cli_tool.py`): User interaction
5. **Configuration** (`config.py`): Settings and templates

### Error Handling
- Graceful API failure handling
- Token usage tracking
- Network timeout management
- Invalid input validation

### Extensibility
- Easy to add new LLM providers
- Configurable prompt templates
- Pluggable personality styles
- Modular analyzer components

## Performance Considerations

### Token Usage
- Average summary: 200-500 tokens
- Average Q&A: 100-300 tokens per question
- Temperature experiments: 600-1500 tokens total
- Style summaries: 300-600 tokens

### Cost Optimization
- Token usage tracking for all operations
- Configurable temperature settings
- Provider selection options
- Batch question processing

## Assignment Compliance

This implementation fulfills all Week 4 requirements:

✅ **Part 1: Summarization Engine**
- Real API integration (not simulated)
- 3-4 sentence summaries
- Original article length tracking
- Proper output formatting

✅ **Part 2: Interactive Q&A**
- Support for multiple questions
- Context-aware responses
- Question and answer display

✅ **Part 3: Parameter Experiments**
- Temperature testing (0.1, 0.7, 1.0)
- Detailed observations recording
- Comparative analysis

✅ **Bonus Challenges**
- Advanced CLI tool with URL support
- Fun personality modes
- Comprehensive session management
- Professional code structure

## Real API Integration

Unlike mock implementations, this version:
- Makes actual API calls to Gemini and OpenAI
- Tracks real token usage and costs
- Handles API errors and rate limits
- Provides authentic model responses
- Supports multiple providers with fallback

The modular architecture makes it easy to extend functionality while maintaining clean separation of concerns.
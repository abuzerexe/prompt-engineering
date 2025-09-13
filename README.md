# Week 3 Assignment: Advanced Prompting Strategies

## Overview
This implementation compares three prompting strategies (Zero-Shot, Few-Shot, Chain-of-Thought) using API calls to evaluate their effectiveness across different task types.

## Files Structure

### Core Implementation
- `main.py` - Main execution script and CLI interface
- `api_client.py` - API client wrapper for Gemini and OpenAI
- `prompt_strategies.py` - Implementation of different prompting strategies
- `evaluator.py` - Evaluation logic and scoring system
- `config.py` - Configuration and constants

### Data
- `datasets.py` - Task datasets and test cases

## Setup

### Prerequisites
```bash
pip install python-dotenv openai google-genai
```

### API Credentials
Create a `.env` file with your API keys:
```
GEMINI_API_KEY="your_gemini_key"
OPEN_ROUTER_KEY="your_openrouter_key"
```

## Usage
```bash
cd week-03-advance-prompting
python main.py
```

## Supported Models
- **Gemini**: `gemini-2.5-flash` (default)
- **OpenAI**: `openai/gpt-4o` (via OpenRouter)

## Features
- Real API integration with error handling
- Token usage tracking for cost analysis
- Modular architecture for easy extension
- Comprehensive evaluation framework
- Unicode-safe output for Windows compatibility
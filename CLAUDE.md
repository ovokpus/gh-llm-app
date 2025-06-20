# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Environment Setup
```bash
uv venv                           # Create virtual environment
source .venv/bin/activate         # Activate environment (macOS/Linux)
uv sync                          # Install dependencies from pyproject.toml
```

### Development Server
```bash
uv run chainlit run app.py -w     # Run with hot reload (default: http://localhost:8000)
```

### Docker Operations  
```bash
docker build -t llm-app .         # Build container image
docker run -p 7860:7860 llm-app   # Run on port 7860
```

### Environment Configuration
Create `.env` file in root directory:
```env
OPENAI_API_KEY=your-api-key-here
```

## Architecture Overview

### Core Application Structure
- **`app.py`** - Main Chainlit application with OpenAI streaming integration
- **Template System** - Uses system/user prompt templates for consistent AI behavior
- **Session Management** - Chainlit handles user sessions with configurable GPT-3.5 Turbo settings
- **Streaming Responses** - Real-time token streaming using AsyncOpenAI client

### Key Framework Integration
- **Chainlit Decorators**:
  - `@cl.on_chat_start` - Initialize chat sessions with model settings
  - `@cl.on_message` - Process user messages with streaming responses
- **OpenAI Configuration** - Fixed settings (temp=0, max_tokens=500) in session state
- **Prompt Engineering** - Structured templates with variable substitution

### Package Management
This project uses **uv** (modern Python package manager) instead of pip/requirements.txt:
- Dependencies defined in `pyproject.toml`
- Requires Python >=3.13
- Key dependencies: chainlit, openai, cohere, pydantic, python-dotenv

### Educational Components
- **`notebooks/`** - Jupyter notebooks for learning OpenAI API integration
- **Fine-tuning Tutorial** - Advanced QLoRA/LoRA techniques in LLME_Challenge.ipynb
- **API Examples** - Comprehensive OpenAI endpoint usage patterns

### Deployment Strategy
- **Local Development** - Chainlit dev server with hot reload
- **Docker Containerization** - Multi-stage build with security best practices
- **Production** - Deployed on Hugging Face Spaces (port 7860)
- **Security** - Environment-based API key management, non-root container user

### Model Configuration
Default GPT-3.5 Turbo settings stored in user session:
- Temperature: 0 (deterministic responses)
- Max tokens: 500
- System prompt: "helpful assistant who always speaks in a pleasant tone"
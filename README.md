# Huggingface LLM Application

A streamlined chatbot application built with Chainlit and OpenAI's GPT-3.5 Turbo, designed to provide helpful responses in a pleasant conversational tone.

## 🌟 Features

- Interactive chat interface powered by Chainlit
- Integration with OpenAI's GPT-3.5 Turbo model
- Real-time streaming responses
- Docker containerization support
- Environment variable configuration for secure API key management

## 🛠️ Tech Stack

- Python
- Chainlit (UI Framework)
- OpenAI API
- Docker
- uv (Package Manager)

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- OpenAI API key
- Docker (optional, for containerization)

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:

```bash
# Create virtual environment
uv venv

# Activate the environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate
```

3. Install dependencies:

```bash
uv sync
```

4. Create a `.env` file in the root directory and add your OpenAI API key:

```env
OPENAI_API_KEY=your-api-key-here
```

### Running the Application

#### Local Development

```bash
uv run chainlit run app.py -w
```

#### Using Docker

1. Build the Docker image:

```bash
docker build -t llm-app .
```

2. Run the container:

```bash
docker run -p 7860:7860 llm-app
```

Visit `http://localhost:7860` in your browser to access the application.

## 💡 Usage

Once the application is running:

1. Open the provided URL in your browser
2. Type your message in the chat interface
3. Receive responses from the AI assistant in real-time

## 🔧 Configuration

The application can be configured through the following settings in `app.py`:

- Model: gpt-3.5-turbo
- Temperature: 0 (for consistent responses)
- Max tokens: 500
- Other OpenAI parameters can be adjusted in the settings dictionary

## 🐳 Docker Support

The project includes a Dockerfile for containerization, making it easy to deploy in any environment. The container exposes port 7860 for the web interface.

## 🔒 Security

- API keys are managed through environment variables
- Never commit your `.env` file to version control
- Use secrets management when deploying to production environments

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

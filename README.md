# SwarmMind: Autonomous Multi-Agent AI System

An advanced AI orchestration system designed for Termux mobile terminals that coordinates multiple specialized AI agents to break down complex tasks, conduct deep research, and generate executable Python code. Features intelligent caching, rate limiting, multi-provider LLM support, and comprehensive logging.

## 🚀 Features

- **Multi-Agent Orchestration**: Manager, Researcher, and Writer agents with specialized roles
- **Multi-Provider LLM Support**: OpenAI, Anthropic, Google Gemini, and local Ollama
- **Intelligent Caching**: Response caching with configurable TTL to reduce API calls
- **Rate Limiting**: Per-provider rate limiting with exponential backoff retry logic
- **Structured Logging**: JSON and text format logging with file and console output
- **Safe Code Execution**: Validates generated code before execution with timeout controls
- **Termux-Optimized**: Lightweight, mobile-friendly with minimal dependencies
- **Configuration Management**: Centralized settings with validation
- **Error Handling**: Comprehensive error handling and recovery mechanisms

## 📋 Requirements

- Python 3.8+
- Termux (for mobile) or any Linux/macOS terminal
- At least one API key (OpenAI, Anthropic, or Gemini) OR local Ollama instance
- ~50MB disk space for dependencies

## 🛠️ Installation

### On Desktop / Linux / macOS

```bash
# Clone the repository
git clone https://github.com/aamanilcomps-ops/ai-agent-swarm.git
cd ai-agent-swarm

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
nano .env  # Add your API keys here
```

### On Termux (Mobile)

```bash
# Update package manager
pkg update && pkg upgrade

# Install Python and Git
pkg install python git

# Clone repository
git clone https://github.com/aamanilcomps-ops/ai-agent-swarm.git
cd ai-agent-swarm

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
nano .env  # Add your API keys
```

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# API Keys (choose at least one)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here

# Ollama Configuration (for local inference)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2

# Cache Settings
CACHE_ENABLED=true
CACHE_TTL_HOURS=24
CACHE_DIR=.cache

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=60
RATE_LIMIT_RETRY_ATTEMPTS=3

# Logging
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=json  # json or text
LOG_DIR=logs

# Execution
ENABLE_CODE_EXECUTION=true
TIMEOUT_SECONDS=300
MAX_RETRIES=3
```

### Agent Configuration (config/agents.yaml)

Customize agent roles, goals, and models:

```yaml
manager_agent:
  name: "Atlas"
  role: "Project Manager & Orchestrator"
  goal: "Break down complex user requests into discrete tasks"
  provider: "openai"
  model: "gpt-4o"

research_agent:
  name: "Argus"
  role: "Deep Research Specialist"
  goal: "Analyze data and extract core facts"
  provider: "gemini"
  model: "gemini-2.5-flash"

writer_agent:
  name: "Scribe"
  role: "Elite Technical Writer"
  goal: "Synthesize research into executable code"
  provider: "anthropic"
  model: "claude-3-5-sonnet"
```

## 🚀 Usage

### Basic Usage

```bash
python src/main.py
```

Then enter your request:
```
Enter what you want the AI swarm to build/analyze:
> Build me a Python script that calculates compound interest with user input
```

### Special Commands

While running, you can use:
- `status` - Show system status and agent information
- `cache_clear` - Clear all cached responses
- `quit` or `exit` - Exit the application

### Advanced Usage

```python
from src.main import initialize_agents, load_configuration
from src.config import get_settings
from src.tasks import run_autonomous_workflow

# Initialize
settings = get_settings()
config = load_configuration()
agents = initialize_agents(config, settings)

# Run workflow
result = run_autonomous_workflow(agents, "Your request here")
print(result)
```

## 📁 Project Structure

```
.env                      API keys and configuration
.env.example             Configuration template
requirements.txt         Python dependencies
config/
  agents.yaml            Agent definitions and models
src/
  main.py                Application entry point
  agents.py              AIAgent class with caching/rate limiting
  tasks.py               Workflow orchestration
  executor.py            Safe code execution
  config.py              Settings management with validation
  logger.py              Structured logging setup
  cache.py               Response caching with TTL
  rate_limiter.py        Rate limiting and retry logic
  llm_providers.py       LLM provider abstractions
logs/                    Application logs (auto-created)
generated_output/        Generated code output (auto-created)
```

## 🔧 Supported LLM Providers

### Cloud Providers

| Provider | Model | Requires | Cost |
|----------|-------|----------|------|
| OpenAI | gpt-4o, gpt-4-turbo | API Key | Pay-per-use |
| Anthropic | claude-3-5-sonnet | API Key | Pay-per-use |
| Google Gemini | gemini-2.5-flash | API Key | Pay-per-use |

### Local Provider

| Provider | Setup | Cost |
|----------|-------|------|
| Ollama | Install Ollama + model | Free |

## 💾 Caching System

SwarmMind includes intelligent response caching:

- **Automatic**: Responses are cached after first generation
- **TTL-based**: Configurable time-to-live (default 24 hours)
- **Hash-based**: Cache keys use SHA256 of agent/task/context
- **Transparent**: Automatically used without code changes
- **Manageable**: Clear cache with `cache_clear` command

Benefits:
- Reduced API costs (up to 90%)
- Faster response times
- Offline mode support (with cached data)

## 🛡️ Safety Features

- **Code Validation**: Generated code scanned for dangerous patterns
- **Timeout Protection**: Code execution timeout prevents hangs
- **Sandboxing**: Code runs in isolated subprocess
- **Error Isolation**: Errors don't crash the main application
- **Logging**: All execution logged for debugging

## 📊 Logging

Logs are automatically generated in structured format:

```bash
# View recent logs
tail -f logs/*.log

# Parse JSON logs (requires jq)
cat logs/*.log | jq '.level == "ERROR"'
```

## 🚨 Troubleshooting

### "No valid API keys configured"
- Ensure `.env` file exists
- Check API keys are not placeholder values
- Run `cp .env.example .env` and add real keys

### "Connection refused" (Ollama)
- Install Ollama: https://ollama.ai
- Run `ollama serve` in another terminal
- Verify `OLLAMA_HOST` in `.env`

### "Rate limit exceeded"
- Wait for rate limit reset (1 minute)
- Increase `RATE_LIMIT_REQUESTS_PER_MINUTE` in `.env`
- Enable caching to avoid duplicate requests

### "Timeout during code execution"
- Increase `TIMEOUT_SECONDS` in `.env`
- Check generated code for infinite loops
- Run code manually to debug

## 📚 Advanced Configuration

### Custom Agent

```python
from src.agents import AIAgent

custom_agent = AIAgent(
    name="CustomBot",
    role="Your role here",
    goal="Your goal here",
    provider="openai",
    model="gpt-4o",
    api_key="sk-..."
)

response = custom_agent.execute("Do something interesting")
```

### Using Different Cache Backend

```python
from src.cache import CacheManager

# Custom TTL
cache = CacheManager(cache_dir='.cache', ttl_hours=48)
```

### Fine-tuning Rate Limits

```python
from src.rate_limiter import RateLimiter

limiter = RateLimiter(requests_per_minute=30)  # More conservative
```

## 🔄 Workflow Pipeline

```
User Input
    ↓
[Manager Agent] - Plans decomposition
    ↓
[Research Agent] - Gathers insights
    ↓
[Writer Agent] - Generates code
    ↓
[Validation] - Checks code safety
    ↓
[Execution] - Runs code with timeout
    ↓
Output
```

## 🎯 Performance Tips

1. **Enable Caching**: Set `CACHE_ENABLED=true` (default)
2. **Use Lightweight Models**: Ollama llama2 is faster than GPT-4
3. **Batch Requests**: Process multiple tasks in one session
4. **Monitor Rate Limits**: Check logs for rate limit hits
5. **Adjust Timeouts**: Set appropriate `TIMEOUT_SECONDS`

## 📝 License

MIT License - See LICENSE file

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional LLM providers
- Web UI
- Database persistence
- Docker containerization
- Performance optimizations

## 📞 Support

For issues and questions:
- Check troubleshooting section above
- Review logs in `logs/` directory
- Visit GitHub issues page

## 🚀 Future Roadmap

- [ ] Web UI dashboard
- [ ] Database for response storage
- [ ] Multi-file code generation
- [ ] Real-time streaming responses
- [ ] Docker container support
- [ ] Kubernetes deployment
- [ ] Advanced analytics dashboard
- [ ] Plugin system for custom providers

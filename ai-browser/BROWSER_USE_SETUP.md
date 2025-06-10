# Browser-Use Agent Setup Guide

This guide will help you set up the powerful **browser-use** based agentic workflow for intelligent browser automation.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install browser-use and dependencies
pip install -r requirements_browser_use.txt

# Install Playwright browsers
playwright install chromium --with-deps --no-shell

# For memory functionality (optional)
pip install "browser-use[memory]"
```

### 2. Set Up Environment Variables

Create a `.env` file:

```bash
# .env
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Other AI providers
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
```

### 3. Run Examples

```bash
# Run the browser-use agent
python browser_use_agent.py
```

## 📚 Key Features

### 🧠 **Intelligent Memory System**
- **Persistent Form Data**: Remembers form fields and values across sessions
- **Context-Aware Recall**: Loads relevant data based on form context
- **Session Tracking**: Each task execution tracked with unique ID

### 🎯 **Smart Form Filling**
- **AI-Powered Field Detection**: Automatically maps form fields to data
- **Profile-Based Filling**: Uses user profile for consistent data
- **Custom Data Override**: Supports task-specific data

### 🔧 **Custom Actions**
- **save_form_data**: Saves form data to persistent memory
- **load_form_data**: Retrieves relevant form data from memory
- **read_profile**: Loads user profile data

## 🛠 Usage Examples

### Basic Form Filling

```python
from browser_use_agent import SmartBrowserAgent

agent = SmartBrowserAgent()

# Fill any form intelligently
result = await agent.smart_form_fill(
    url="https://example.com/contact",
    form_context="contact form",
    custom_data={
        "subject": "Business Inquiry",
        "message": "Hello, I'm interested in your services."
    }
)
```

### Job Application Workflow

```python
agent = SmartBrowserAgent()

job_urls = [
    "https://company1.com/jobs/engineer",
    "https://company2.com/careers/developer"
]

results = await agent.job_application_workflow(
    job_urls=job_urls,
    custom_cover_letter="Dear Hiring Manager, ..."
)
```

### Interactive Mode

```python
# Run in interactive mode for custom tasks
await run_interactive_mode()

# Example tasks you can enter:
# "Fill out the contact form at https://example.com with my details"
# "Apply to the job posting at https://jobs.company.com/engineer"
# "Extract pricing information from https://product-site.com"
```

## 🏗 Architecture

### SmartBrowserAgent Class

```python
class SmartBrowserAgent:
    def __init__(self, model_name="gpt-4o")
    async def smart_form_fill(url, form_context, custom_data)
    async def job_application_workflow(job_urls, cover_letter)
    def load_memory() -> Dict
    def save_memory(memory: Dict)
```

### Memory Structure

```json
{
  "session_20241201_143022": {
    "timestamp": "2024-12-01T14:30:22",
    "type": "form_data", 
    "context": "job_application",
    "data": {
      "firstName": "John",
      "email": "john@example.com"
    }
  }
}
```

### User Profile Format

```json
{
  "personal": {
    "firstName": "John",
    "lastName": "Doe", 
    "email": "john.doe@email.com",
    "phone": "555-123-4567",
    "address": "123 Main St, Anytown, USA"
  },
  "professional": {
    "experience": "5 years",
    "skills": ["Python", "JavaScript", "React"],
    "position": "Software Engineer",
    "linkedin": "https://linkedin.com/in/johndoe"
  }
}
```

## 🎮 Available Examples

Run `python browser_use_agent.py` and choose:

1. **Smart Form Filling** - Demonstrates intelligent form completion
2. **Job Applications** - Automated job application workflow  
3. **Interactive Mode** - Natural language task execution

## 🔧 Advanced Configuration

### Custom Actions

You can extend the agent with custom actions:

```python
@controller.action("Custom action description")
def my_custom_action(param1: str, param2: int):
    # Your custom logic here
    return f"Executed with {param1} and {param2}"
```

### Different AI Models

```python
# Use different models
agent = SmartBrowserAgent(model_name="gpt-4o-mini")  # Faster/cheaper
agent = SmartBrowserAgent(model_name="gpt-4")        # More powerful
```

### Memory Management

```python
# Access memory directly
memory = agent.load_memory()
print(f"Found {len(memory)} sessions")

# Clear memory
agent.save_memory({})
```

## 🔍 Comparison: Browser-Use vs Custom Playwright

| Feature | Browser-Use | Custom Playwright |
|---------|-------------|-------------------|
| **Setup Complexity** | ⭐⭐ Simple | ⭐⭐⭐⭐ Complex |
| **AI Integration** | ⭐⭐⭐⭐⭐ Native | ⭐⭐⭐ Custom |
| **Memory System** | ⭐⭐⭐⭐⭐ Advanced | ⭐⭐⭐ Basic |
| **Community Support** | ⭐⭐⭐⭐⭐ Active | ⭐⭐ Limited |
| **Documentation** | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐ Good |
| **Natural Language** | ⭐⭐⭐⭐⭐ Full Support | ⭐⭐ Limited |

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**
   ```bash
   # Make sure your .env file has the correct API key
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

2. **Browser Not Found**
   ```bash
   # Reinstall Playwright browsers
   playwright install chromium --force
   ```

3. **Memory Issues**
   ```bash
   # Clear memory if corrupted
   rm browser_agent_memory.json
   ```

4. **Form Field Detection**
   - Check that the target website is accessible
   - Verify form fields are not dynamic/JavaScript-heavy
   - Try with a simpler test form first

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Production Usage

### Security Best Practices

- Store API keys in environment variables
- Use headless mode for production
- Implement rate limiting between requests
- Monitor memory usage and clear old sessions

### Performance Optimization

- Use `gpt-4o-mini` for faster responses
- Implement parallel processing for multiple forms
- Cache user profiles to reduce API calls
- Set appropriate timeouts for page loads

### Error Handling

```python
try:
    result = await agent.smart_form_fill(url, context, data)
except Exception as e:
    logger.error(f"Form filling failed: {str(e)}")
    # Implement fallback or retry logic
```

## 🌟 Why Browser-Use is Superior

1. **🎯 Purpose-Built**: Designed specifically for AI browser automation
2. **🧠 Advanced Memory**: Sophisticated memory system with 100+ step capability  
3. **🤖 Native AI**: Seamless LLM integration with optimized prompts
4. **📦 Production-Ready**: Battle-tested with 62.6k+ GitHub stars
5. **🔧 Extensible**: Easy to add custom actions and behaviors
6. **📚 Rich Ecosystem**: Active community, examples, and documentation

This browser-use implementation provides a much more powerful and maintainable solution compared to custom Playwright automation! 
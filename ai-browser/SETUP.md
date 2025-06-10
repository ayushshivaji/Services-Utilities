# Agentic Browser Automation Setup Guide

This guide will help you set up and use the agentic browser automation workflow that can perform tasks like form filling, data extraction, and navigation with memory capabilities.

## 🚀 Quick Installation Steps

### 1. Install Python Dependencies

```bash
# Install the required Python packages
pip install -r requirements.txt

# Install Playwright browsers (required for browser automation)
playwright install

# Install Chromium browser specifically (most reliable)
playwright install chromium
```

### 2. Set Up Environment Variables (Optional but Recommended)

Create a `.env` file in your project directory:

```bash
# .env file
OPENAI_API_KEY=your_openai_api_key_here
```

If you don't have an OpenAI API key, the agent will still work but without AI-enhanced form field detection.

### 3. Verify Installation

Run the demo to make sure everything works:

```bash
python ai.py
```

This will open a browser and demonstrate basic form filling on a test website.

## 📋 Detailed Installation Guide

### Prerequisites

- **Python 3.8+** (Python 3.10+ recommended)
- **Operating System**: macOS, Linux, or Windows
- **Internet connection** for downloading browser binaries

### Step-by-Step Installation

#### 1. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### 2. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Alternative: Install packages individually
pip install playwright==1.40.0
pip install openai==1.3.0
pip install pydantic==2.5.0
pip install aiohttp==3.9.0
```

#### 3. Install Browser Binaries

```bash
# Install all Playwright browsers
playwright install

# Or install specific browsers only
playwright install chromium
playwright install firefox
playwright install webkit
```

#### 4. Verify Browser Installation

```bash
# Test browser installation
playwright --version

# List installed browsers
playwright list-browsers
```

## 🎯 Usage Examples

### Basic Form Filling

```python
import asyncio
from ai import BrowserAgent

async def fill_contact_form():
    agent = BrowserAgent(headless=False)  # Set True for headless mode
    
    # Define form data
    form_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello, this is an automated message!"
    }
    
    # Fill form with intelligent field detection
    result = await agent.intelligent_form_fill(
        url="https://example.com/contact",
        form_data=form_data
    )
    
    await agent.close_browser()
    return result

# Run the task
asyncio.run(fill_contact_form())
```

### Custom Task Configuration

```python
import asyncio
from ai import BrowserAgent

async def custom_automation_task():
    agent = BrowserAgent(headless=False)
    
    task_config = {
        "type": "custom_task",
        "steps": [
            {"action": "navigate", "params": {"url": "https://example.com"}},
            {"action": "wait", "params": {"timeout": 3000}},
            {"action": "click", "params": {"selector": ".login-button"}},
            {"action": "fill_form", "params": {
                "form_data": {
                    "username": "your_username",
                    "password": "your_password"
                }
            }},
            {"action": "click", "params": {"selector": "input[type='submit']"}},
            {"action": "wait", "params": {"selector": ".dashboard", "timeout": 10000}},
            {"action": "extract_data", "params": {
                "selectors": {
                    "welcome_message": ".welcome-text",
                    "user_stats": ".stats-container"
                }
            }}
        ]
    }
    
    result = await agent.execute_task(task_config)
    await agent.close_browser()
    return result

asyncio.run(custom_automation_task())
```

### Data Extraction Example

```python
import asyncio
from ai import BrowserAgent

async def extract_product_data():
    agent = BrowserAgent(headless=True)  # Run in background
    
    task_config = {
        "type": "data_extraction",
        "steps": [
            {"action": "navigate", "params": {"url": "https://example-store.com/products"}},
            {"action": "wait", "params": {"selector": ".product-grid", "timeout": 5000}},
            {"action": "extract_data", "params": {
                "selectors": {
                    "product_titles": ".product-title",
                    "prices": ".price",
                    "ratings": ".rating",
                    "availability": ".stock-status"
                }
            }}
        ]
    }
    
    result = await agent.execute_task(task_config)
    await agent.close_browser()
    
    # Access extracted data
    extracted_data = result.get('results', [])
    for step_result in extracted_data:
        if step_result.get('action') == 'extract_data':
            data = step_result.get('data', {})
            print(f"Extracted: {data}")
    
    return result

asyncio.run(extract_product_data())
```

## 🧠 Memory System

The agent automatically saves memory between sessions:

- **Session Memory**: Each task execution creates a session with unique ID
- **Form Data Memory**: Remembers form fields and values used
- **Navigation Memory**: Tracks visited URLs and successful navigation patterns
- **Action Memory**: Records all actions taken and their outcomes

Memory is saved in `agent_memory.json` and can be used to improve future task executions.

## 🛠 Available Actions

### Core Actions

1. **navigate** - Navigate to URLs
   ```python
   {"action": "navigate", "params": {"url": "https://example.com"}}
   ```

2. **fill_form** - Fill form fields intelligently
   ```python
   {"action": "fill_form", "params": {"form_data": {"field": "value"}}}
   ```

3. **click** - Click on elements
   ```python
   {"action": "click", "params": {"selector": ".button-class"}}
   ```

4. **wait** - Wait for elements or timeout
   ```python
   {"action": "wait", "params": {"selector": ".loading", "timeout": 5000}}
   ```

5. **extract_data** - Extract data from page
   ```python
   {"action": "extract_data", "params": {"selectors": {"name": ".selector"}}}
   ```

## 🔧 Configuration Options

### BrowserAgent Parameters

```python
agent = BrowserAgent(
    openai_api_key="your_key",  # Optional: For AI-enhanced field detection
    headless=False,             # True for background execution
)
```

### Browser Configuration

The agent uses Chromium by default with these settings:
- Viewport: 1920x1080
- User Agent: Modern Chrome user agent
- Security: Sandbox disabled for compatibility

## 🐛 Troubleshooting

### Common Issues

1. **Browser not found**
   ```bash
   # Reinstall browsers
   playwright install --force
   ```

2. **Permission denied (macOS/Linux)**
   ```bash
   # Fix permissions
   chmod +x venv/bin/playwright
   ```

3. **Timeout errors**
   - Increase timeout values in wait actions
   - Check internet connection
   - Verify selectors are correct

4. **Form fields not found**
   - Check field names and IDs on the target website
   - Use browser dev tools to inspect elements
   - Try different selector strategies

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🔐 Security Considerations

- **Headless Mode**: Use for production to avoid UI interference
- **Credentials**: Store sensitive data in environment variables
- **Rate Limiting**: Add delays between actions to avoid being blocked
- **User Agents**: The agent uses realistic user agents by default

## 📚 Advanced Features

### AI-Enhanced Form Detection

When OpenAI API key is provided, the agent can:
- Analyze page structure intelligently
- Suggest better field selectors
- Adapt to dynamic form layouts

### Memory-Based Learning

The agent learns from previous executions:
- Remembers successful field selectors
- Adapts to site changes over time
- Reuses successful navigation patterns

### Parallel Task Execution

Run multiple browser tasks simultaneously:

```python
import asyncio
from ai import BrowserAgent

async def run_parallel_tasks():
    tasks = []
    for url in ["https://site1.com", "https://site2.com"]:
        agent = BrowserAgent(headless=True)
        task = agent.execute_task({
            "type": "parallel_task",
            "steps": [{"action": "navigate", "params": {"url": url}}]
        })
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    return results
```

## 🤝 Contributing

Feel free to extend the agent with new actions:

1. Create a new action class inheriting from `BrowserAction`
2. Implement the `execute` method
3. Add to the `BrowserAgent.actions` dictionary

Example custom action:

```python
class ScrollAction(BrowserAction):
    async def execute(self, page: Page, direction: str = "down", pixels: int = 500, **kwargs):
        if direction == "down":
            await page.evaluate(f"window.scrollBy(0, {pixels})")
        else:
            await page.evaluate(f"window.scrollBy(0, -{pixels})")
        return {"action": "scroll", "direction": direction, "pixels": pixels}

# Add to agent
agent.actions['scroll'] = ScrollAction()
```

This setup provides a robust foundation for browser automation with memory capabilities! 
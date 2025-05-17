import json

from agno.memory.agent import AgentMemory
from dotenv import load_dotenv
from rich.console import Console

from agno.agent import Agent
from agno.memory.db.postgres import PgMemoryDb
from agno.models.groq import Groq
from agno.storage.agent.postgres import PostgresAgentStorage
from agno.tools import Toolkit

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
load_dotenv()


class MyCustomTools(Toolkit):
    def __init__(self):
        super().__init__(name="my_custom_tools")
        self.register(self.get_webpage_inputs)

    def get_webpage_inputs(self, url: str) -> str:
        """Open a webpage and extract all input fields.
        
        Args:
            url (str): The URL of the webpage to analyze
            
        Returns:
            str: Formatted string containing input field information
        """
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options

        # Set up headless Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        try:
            # Initialize the driver
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)

            # Find all input elements
            input_elements = driver.find_elements(By.TAG_NAME, "input")
            
            # Format the results as a string
            result = "Found the following input fields:\n\n"
            for element in input_elements:
                result += "Input Field:\n"
                result += f"- Name: {element.get_attribute('name')}\n"
                result += f"- Type: {element.get_attribute('type')}\n"
                result += f"- ID: {element.get_attribute('id')}\n"
                result += f"- Placeholder: {element.get_attribute('placeholder')}\n"
                result += "-" * 40 + "\n"

            return result if input_elements else "No input fields found on the page."

        except Exception as e:
            return f"Error occurred: {str(e)}"
            
        finally:
            driver.quit()  # Always close the browser

# Create tools instance
my_tools = MyCustomTools()

agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile",temperature=0),
    storage=PostgresAgentStorage(table_name="agent_sessions",db_url=db_url),
    add_history_to_messages=True,
    update_knowledge=True,
    read_chat_history=True,
    session_id="persisting_memory",
    memory=AgentMemory(
        db=PgMemoryDb(
            table_name="agent_memory",
            db_url=db_url
        ),
    ),
    tools=[my_tools],  # Add the tools to the agent
    description="You are a helpful assistant that always responds in a polite, upbeat and positive manner.",
)

agent.print_response("Get me the input fields from https://www.hashicorp.com/en/career/6630603", stream=True)

# agent.print_response("", stream=True)
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.website import WebsiteTools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from rich.console import Console
from rich.prompt import Prompt
from agno.storage.agent.postgres import PostgresAgentStorage
from agno.memory.db.postgres import PgMemoryDb
from agno.memory.agent import AgentMemory
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
load_dotenv()

class FormAnalyzerTools:
    def __init__(self):
        self.chrome_options = Options()
        # self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        
    def find_apply_button(self, url: str) -> tuple[bool, str]:
        """Search for an apply button on the webpage"""
        driver = webdriver.Chrome(options=self.chrome_options)
        wait = WebDriverWait(driver, 10)
        try:
            driver.get(url)
            
            # Find buttons with 'apply' text in button itself or any child elements
            # Find all buttons on the page
            buttons = driver.find_elements(By.TAG_NAME, "button")
            
            # Print information about each button
            for button in buttons:
                print(f"\nButton found:")
                print(f"Text: {button.text}")
                print(f"Tag name: {button.tag_name}")
                print(f"Class: {button.get_attribute('class')}")
                print(f"ID: {button.get_attribute('id')}")
                print("-" * 40)
            
            # Store buttons for later use
            apply_buttons = buttons
            
            # Store initial URL to detect changes
            initial_url = driver.current_url
            
            for button in apply_buttons:
                try:
                    # Wait for button to be clickable
                    wait.until(EC.element_to_be_clickable((By.XPATH, f"//{button.tag_name}[contains(translate(text(), 'APPLY', 'apply'), 'apply')]")))
                    
                    # Check for href if it's a link
                    href = button.get_attribute('href')
                    if href:
                        driver.get(href)
                        # Wait for page load and URL change
                        wait.until(lambda d: d.current_url != initial_url)
                        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                        return True, driver.current_url
                    else:
                        # Click the button
                        button.click()
                        # Wait for page load and URL change  
                        wait.until(lambda d: d.current_url != initial_url)
                        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                        return True, driver.current_url
                        
                except (TimeoutException, Exception):
                    continue
                    
            return False, ""
            
        except Exception as e:
            print(f"Error in find_apply_button: {str(e)}")
            return False, ""
        finally:
            driver.quit()
            
    def get_form_fields(self, url: str) -> dict:
        """Find all input fields on a webpage and return their details"""
        driver = webdriver.Chrome(options=self.chrome_options)
        try:
            driver.get(url)
            
            # Wait for page to load and input fields to be present
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
            
            input_elements = driver.find_elements(By.TAG_NAME, "input")
            
            form_fields = {}
            for element in input_elements:
                field_id = element.get_attribute('id') or element.get_attribute('name')
                if field_id:
                    form_fields[field_id] = {
                        'type': element.get_attribute('type'),
                        'placeholder': element.get_attribute('placeholder'),
                        'element': element
                    }
            return form_fields
            
        finally:
            driver.quit()

class FormTeam:
    def __init__(self):
        load_dotenv()
        self.console = Console()
        self.form_tools = FormAnalyzerTools()
        
        # Analyzer agent finds and analyzes form fields
        self.analyzer = Agent(
            model=Groq(id="llama-3.3-70b-versatile", temperature=0),
            description="You analyze form fields and suggest appropriate values based on field names and types",
            tools=[WebsiteTools()],
            debug_mode=True
        )
        
        # Filler agent suggests values for fields
        self.filler = Agent(
            model=Groq(id="llama-3.3-70b-versatile", temperature=0),
            description="You suggest appropriate values for form fields based on their purpose",
            tools=[WebsiteTools()],
            debug_mode=True,
            storage=PostgresAgentStorage(table_name="form_filler_sessions", db_url=db_url),
            memory=AgentMemory(
                db=PgMemoryDb(
                    table_name="form_filler_memory",
                    db_url=db_url
                ),
            ),
            add_history_to_messages=True,
            update_knowledge=True,
            read_chat_history=True,
            session_id="form_filler"
        )

    def process_form(self, url: str):
        self.console.print(f"\n[bold blue]Analyzing page at {url}...[/bold blue]")
        
        # First, look for an apply button
        found_button, new_url = self.form_tools.find_apply_button(url)
        
        if found_button:
            self.console.print(f"[green]Found apply button![/green]")
            if new_url != url:
                self.console.print(f"[yellow]Redirecting to application form: {new_url}[/yellow]")
                url = new_url
        else:
            self.console.print("[yellow]No apply button found. Looking for form fields directly...[/yellow]")
        
        # Get form fields
        form_fields = self.form_tools.get_form_fields(url)
        
        if not form_fields:
            self.console.print("[red]No form fields found![/red]")
            return
            
        # Process each field
        driver = webdriver.Chrome(options=self.form_tools.chrome_options)
        try:
            driver.get(url)
            
            for field_id, details in form_fields.items():
                field_type = details['type']
                placeholder = details['placeholder'] or "No placeholder"
                
                self.console.print(f"\n[yellow]Field found:[/yellow] {field_id}")
                self.console.print(f"Type: {field_type}")
                self.console.print(f"Placeholder: {placeholder}")
                
                # Get suggestion from filler agent with default values for common fields
                default_values = {
                    'email': 'test@example.com',
                    'text': 'John Doe',
                    'tel': '1234567890',
                    'number': '123',
                    'password': 'TestPassword123!'
                }
                
                # Use default value if available, otherwise ask AI
                if field_type in default_values:
                    suggestion = default_values[field_type]
                else:
                    suggestion_prompt = f"Suggest a value for form field '{field_id}' of type '{field_type}' with placeholder '{placeholder}'"
                    self.filler.print_response(suggestion_prompt, stream=True)
                    suggestion = "default_value"  # Fallback value
                
                # Get user input
                value = Prompt.ask(
                    f"Enter value for {field_id}",
                    default=str(suggestion)
                )
                
                # Fill the field
                try:
                    element = driver.find_element(By.ID, field_id)
                except:
                    try:
                        element = driver.find_element(By.NAME, field_id)
                    except:
                        self.console.print(f"[red]Could not find element with ID or name: {field_id}[/red]")
                        continue
                
                element.send_keys(value)
                
            self.console.print("\n[green]Form filling complete! Review the form before submitting.[/green]")
            
            # Wait for user to review
            Prompt.ask("\nPress Enter when ready to close", default="")
            
        finally:
            driver.quit()

# Example usage:
if __name__ == "__main__":
    form_team = FormTeam()
    form_team.process_form("https://www.hashicorp.com/en/career/6630603")

"""
Agentic Browser Automation with Browser-Use
==========================================
A powerful browser automation agent using the browser-use library
for intelligent form filling, data extraction, and task automation.
"""

import asyncio
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from dotenv import load_dotenv
from browser_use import Agent, Controller
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()


class SmartBrowserAgent:
    """Enhanced browser agent with memory and intelligent task handling"""
    
    def __init__(self, model_name: str = "gpt-4o"):
        """Initialize the browser agent"""
        self.model_name = model_name
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.1,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.controller = Controller()
        self.memory_file = Path("browser_agent_memory.json")
        
        # Setup custom actions
        self._setup_custom_actions()
    
    def _setup_custom_actions(self):
        """Setup custom actions for the controller"""
        
        @self.controller.action("Save form data to memory")
        def save_form_data(form_data: Dict[str, Any], context: str = ""):
            """Save form data to persistent memory"""
            memory = self.load_memory()
            
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            memory[session_id] = {
                "timestamp": datetime.now().isoformat(),
                "type": "form_data",
                "context": context,
                "data": form_data
            }
            
            self.save_memory(memory)
            return f"Form data saved to memory with session ID: {session_id}"
        
        @self.controller.action("Load previous form data from memory")
        def load_form_data(context: str = ""):
            """Load previous form data from memory"""
            memory = self.load_memory()
            
            # Find most recent matching context
            matching_sessions = []
            for session_id, data in memory.items():
                if data.get("type") == "form_data":
                    if not context or context.lower() in data.get("context", "").lower():
                        matching_sessions.append((session_id, data))
            
            if matching_sessions:
                # Sort by timestamp and get most recent
                matching_sessions.sort(key=lambda x: x[1]["timestamp"], reverse=True)
                latest_data = matching_sessions[0][1]["data"]
                return f"Found previous form data: {json.dumps(latest_data, indent=2)}"
            
            return "No matching form data found in memory"
        
        @self.controller.action("Read user profile data")
        def read_profile():
            """Read user profile data for form filling"""
            profile_file = Path("user_profile.json")
            if profile_file.exists():
                with open(profile_file, 'r') as f:
                    profile = json.load(f)
                return f"User profile loaded: {json.dumps(profile, indent=2)}"
            else:
                # Create default profile
                default_profile = {
                    "personal": {
                        "firstName": "John",
                        "lastName": "Doe",
                        "email": "john.doe@email.com",
                        "phone": "555-123-4567",
                        "address": "123 Main St, Anytown, USA"
                    },
                    "professional": {
                        "experience": "5 years",
                        "skills": ["Python", "JavaScript", "React", "Node.js"],
                        "position": "Software Engineer",
                        "linkedin": "https://linkedin.com/in/johndoe",
                        "github": "https://github.com/johndoe"
                    }
                }
                
                with open(profile_file, 'w') as f:
                    json.dump(default_profile, f, indent=2)
                
                return f"Created default profile: {json.dumps(default_profile, indent=2)}"
    
    def load_memory(self) -> Dict[str, Any]:
        """Load memory from file"""
        if self.memory_file.exists():
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_memory(self, memory: Dict[str, Any]):
        """Save memory to file"""
        with open(self.memory_file, 'w') as f:
            json.dump(memory, f, indent=2)
    
    async def smart_form_fill(self, url: str, form_context: str = "", custom_data: Dict[str, Any] = None):
        """Intelligently fill forms using AI and memory"""
        
        task_prompt = f"""
        Navigate to {url} and intelligently fill out the form.
        
        Context: {form_context}
        
        Instructions:
        1. First, read the user profile data to get personal and professional information
        2. Load any previous form data from memory that might be relevant to "{form_context}"
        3. Analyze the form fields and fill them with appropriate data
        4. Use intelligent field mapping (e.g., "first name" -> firstName, "email address" -> email)
        5. Save the filled form data to memory for future use
        6. If there are any issues or unclear fields, make reasonable assumptions
        
        Custom data to use: {json.dumps(custom_data or {}, indent=2)}
        
        Do not submit the form unless explicitly told to do so.
        """
        
        agent = Agent(
            task=task_prompt,
            llm=self.llm,
            controller=self.controller
        )
        
        result = await agent.run()
        return result
    
    async def job_application_workflow(self, job_urls: List[str], custom_cover_letter: str = None):
        """Automated job application workflow"""
        
        cover_letter = custom_cover_letter or """
        Dear Hiring Manager,
        
        I am excited to apply for this position. With my experience in software development 
        and passion for creating innovative solutions, I believe I would be a valuable 
        addition to your team.
        
        Best regards,
        John Doe
        """
        
        results = []
        
        for i, url in enumerate(job_urls, 1):
            print(f"🎯 Processing job application {i}/{len(job_urls)}: {url}")
            
            task_prompt = f"""
            Apply for a job at {url}
            
            Instructions:
            1. Read user profile data to get personal and professional information
            2. Navigate to the job application page
            3. Fill out the application form with appropriate information
            4. Use this cover letter: {cover_letter}
            5. Save the application data to memory with context "job_application"
            6. Do NOT submit the application - stop just before final submission
            
            Be thorough and professional.
            """
            
            agent = Agent(
                task=task_prompt,
                llm=self.llm,
                controller=self.controller
            )
            
            try:
                result = await agent.run()
                results.append({"url": url, "status": "completed", "result": result})
                print(f"✅ Job application {i} completed")
            except Exception as e:
                results.append({"url": url, "status": "failed", "error": str(e)})
                print(f"❌ Job application {i} failed: {str(e)}")
            
            # Small delay between applications
            if i < len(job_urls):
                await asyncio.sleep(3)
        
        return results


# Example usage functions
async def example_form_filling():
    """Example: Smart form filling with memory"""
    print("📝 Demonstrating smart form filling...")
    
    agent = SmartBrowserAgent()
    
    # Fill a contact form
    result = await agent.smart_form_fill(
        url="https://httpbin.org/forms/post",
        form_context="contact form",
        custom_data={
            "custname": "John Doe",
            "custemail": "john.doe@email.com",
            "custtel": "555-123-4567"
        }
    )
    
    print("✅ Contact form completed")
    return result


async def example_job_applications():
    """Example: Automated job applications"""
    print("🎯 Starting automated job application workflow...")
    
    agent = SmartBrowserAgent()
    
    # Example job URLs (replace with real ones)
    job_urls = [
        "https://httpbin.org/forms/post",  # Demo form for testing
    ]
    
    custom_cover_letter = """
    Dear Hiring Manager,
    
    I am writing to express my strong interest in the software engineering position 
    at your company. With 5 years of experience in full-stack development, I am 
    confident I can contribute significantly to your team.
    
    Thank you for your consideration.
    
    Best regards,
    John Doe
    """
    
    results = await agent.job_application_workflow(job_urls, custom_cover_letter)
    
    print(f"📊 Job applications completed: {len([r for r in results if r['status'] == 'completed'])}/{len(results)}")
    return results


async def run_interactive_mode():
    """Interactive mode for custom tasks"""
    print("🤖 Interactive Browser Agent Mode")
    print("Enter natural language tasks for the browser agent to execute.")
    print("Type 'quit' to stop.\n")
    
    agent = SmartBrowserAgent()
    
    while True:
        try:
            task = input("🎯 Enter task: ").strip()
            
            if task.lower() in ['quit', 'exit', 'q', '']:
                print("👋 Goodbye!")
                break
            
            print(f"🚀 Executing: {task}")
            
            browser_agent = Agent(
                task=task,
                llm=agent.llm,
                controller=agent.controller
            )
            
            result = await browser_agent.run()
            print("✅ Task completed!\n")
            
        except KeyboardInterrupt:
            print("\n👋 Interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")


async def main():
    """Main function with example selector"""
    print("🌐 Browser-Use Agent Examples")
    print("=" * 40)
    print("1. Smart Form Filling")
    print("2. Job Applications") 
    print("3. Interactive Mode")
    
    while True:
        try:
            choice = input("\nSelect example (1-3): ").strip()
            
            if choice == "1":
                await example_form_filling()
            elif choice == "2":
                await example_job_applications()
            elif choice == "3":
                await run_interactive_mode()
            else:
                print("❌ Invalid choice. Please select 1-3.")
                continue
            
            break
            
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    print("🤖 Browser-Use Agentic Automation")
    print("Make sure you have set up your OPENAI_API_KEY in .env file")
    
    asyncio.run(main()) 
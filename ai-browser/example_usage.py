"""
Example usage of the Agentic Browser Automation Workflow
=======================================================
This script demonstrates various use cases for the browser agent.
"""

import asyncio
import os
from ai import BrowserAgent


async def example_1_simple_form_filling():
    """Example 1: Fill a simple contact form"""
    print("🚀 Example 1: Simple Form Filling")
    
    agent = BrowserAgent(headless=False)
    
    # Simple form filling task
    task_config = {
        "type": "contact_form",
        "steps": [
            {"action": "navigate", "params": {"url": "https://httpbin.org/forms/post"}},
            {"action": "wait", "params": {"timeout": 2000}},
            {"action": "fill_form", "params": {
                "form_data": {
                    "custname": "Alice Johnson",
                    "custtel": "555-0123",
                    "custemail": "alice@example.com",
                    "size": "medium",
                    "topping": "cheese",
                    "delivery": "17:30"
                }
            }},
            {"action": "wait", "params": {"timeout": 2000}},
            # Uncomment the line below to actually submit the form
            # {"action": "click", "params": {"selector": "input[type='submit']"}}
        ]
    }
    
    result = await agent.execute_task(task_config)
    await agent.close_browser()
    
    print(f"✅ Task completed with session ID: {result['task_id']}")
    return result


async def example_2_job_application():
    """Example 2: Intelligent job application form filling"""
    print("🎯 Example 2: Job Application Form")
    
    # Set your OpenAI API key for enhanced form detection
    api_key = os.getenv('OPENAI_API_KEY')  # Set this in your environment
    agent = BrowserAgent(openai_api_key=api_key, headless=False)
    
    # Job application data
    job_application_data = {
        "firstName": "John",
        "lastName": "Doe", 
        "email": "john.doe@email.com",
        "phone": "555-123-4567",
        "linkedin": "https://linkedin.com/in/johndoe",
        "experience": "5",
        "position": "Software Engineer",
        "coverLetter": "Dear Hiring Manager,\n\nI am excited to apply for the Software Engineer position. With 5 years of experience in full-stack development, I believe I would be a great fit for your team.\n\nBest regards,\nJohn Doe"
    }
    
    # Use the intelligent form filling method
    result = await agent.intelligent_form_fill(
        url="https://httpbin.org/forms/post",  # Replace with actual job application URL
        form_data=job_application_data,
        form_hints={
            "firstName": "First name, given name, or name field",
            "lastName": "Last name, surname, or family name field", 
            "email": "Email address or contact email field",
            "phone": "Phone number, telephone, or mobile field",
            "linkedin": "LinkedIn profile, social media, or portfolio field",
            "experience": "Years of experience, work experience, or experience level",
            "position": "Desired position, job title, or role field",
            "coverLetter": "Cover letter, message, or additional information field"
        }
    )
    
    await agent.close_browser()
    print(f"✅ Job application completed with session ID: {result['task_id']}")
    return result


async def example_3_data_extraction():
    """Example 3: Extract data from a website"""
    print("📊 Example 3: Data Extraction")
    
    agent = BrowserAgent(headless=True)  # Run in background for data extraction
    
    task_config = {
        "type": "data_extraction",
        "steps": [
            {"action": "navigate", "params": {"url": "https://quotes.toscrape.com/"}},
            {"action": "wait", "params": {"selector": ".quote", "timeout": 5000}},
            {"action": "extract_data", "params": {
                "selectors": {
                    "quotes": ".text",
                    "authors": ".author",
                    "tags": ".tag"
                }
            }}
        ]
    }
    
    result = await agent.execute_task(task_config)
    await agent.close_browser()
    
    # Process extracted data
    for step_result in result.get('results', []):
        if step_result.get('action') == 'extract_data':
            data = step_result.get('data', {})
            print("📄 Extracted Data:")
            for key, value in data.items():
                if isinstance(value, str) and len(value) > 100:
                    print(f"  {key}: {value[:100]}...")
                else:
                    print(f"  {key}: {value}")
    
    return result


async def example_4_multi_step_workflow():
    """Example 4: Complex multi-step workflow"""
    print("🔄 Example 4: Multi-step Workflow")
    
    agent = BrowserAgent(headless=False)
    
    # Complex workflow: Navigate, search, extract, and interact
    task_config = {
        "type": "multi_step_workflow", 
        "steps": [
            # Step 1: Navigate to a search page
            {"action": "navigate", "params": {"url": "https://httpbin.org/"}},
            {"action": "wait", "params": {"timeout": 2000}},
            
            # Step 2: Navigate to forms page
            {"action": "click", "params": {"selector": "a[href='/forms/post']"}},
            {"action": "wait", "params": {"timeout": 2000}},
            
            # Step 3: Fill out form
            {"action": "fill_form", "params": {
                "form_data": {
                    "custname": "Workflow User",
                    "custemail": "workflow@example.com",
                    "size": "large"
                }
            }},
            
            # Step 4: Wait and then navigate to status page
            {"action": "wait", "params": {"timeout": 1000}},
            {"action": "navigate", "params": {"url": "https://httpbin.org/status/200"}},
            
            # Step 5: Extract page information
            {"action": "extract_data", "params": {
                "selectors": {
                    "title": "title",
                    "body": "body"
                }
            }}
        ]
    }
    
    result = await agent.execute_task(task_config)
    await agent.close_browser()
    
    print(f"✅ Multi-step workflow completed with {len(result.get('results', []))} steps")
    return result


async def example_5_form_with_memory():
    """Example 5: Demonstrate memory capabilities"""
    print("🧠 Example 5: Memory-Enhanced Form Filling")
    
    agent = BrowserAgent(headless=False)
    
    # First task - fill form and save to memory
    first_task = {
        "type": "recurring_form",  # Same type for memory matching
        "steps": [
            {"action": "navigate", "params": {"url": "https://httpbin.org/forms/post"}},
            {"action": "wait", "params": {"timeout": 2000}},
            {"action": "fill_form", "params": {
                "form_data": {
                    "custname": "Memory User",
                    "custemail": "memory@example.com",
                    "custtel": "555-MEMORY"
                }
            }}
        ]
    }
    
    print("📝 First execution - saving to memory...")
    result1 = await agent.execute_task(first_task)
    
    # Small delay to show memory persistence
    await asyncio.sleep(1)
    
    # Second task - agent should remember previous form data
    second_task = {
        "type": "recurring_form",  # Same type - should trigger memory recall
        "steps": [
            {"action": "navigate", "params": {"url": "https://httpbin.org/forms/post"}},
            {"action": "wait", "params": {"timeout": 2000}},
            {"action": "fill_form", "params": {
                "form_data": {
                    "custname": "Memory User Updated",  # Slightly different data
                    "size": "small"
                }
            }}
        ]
    }
    
    print("🔄 Second execution - should recall memory...")
    result2 = await agent.execute_task(second_task)
    
    await agent.close_browser()
    
    print(f"✅ Memory demo completed:")
    print(f"  Session 1: {result1['task_id']}")
    print(f"  Session 2: {result2['task_id']}")
    
    return {"first": result1, "second": result2}


async def run_all_examples():
    """Run all examples in sequence"""
    print("🤖 Running All Browser Agent Examples")
    print("=" * 50)
    
    examples = [
        example_1_simple_form_filling,
        example_2_job_application,
        example_3_data_extraction,
        example_4_multi_step_workflow,
        example_5_form_with_memory
    ]
    
    results = {}
    
    for i, example_func in enumerate(examples, 1):
        try:
            print(f"\n--- Running Example {i} ---")
            result = await example_func()
            results[f"example_{i}"] = result
            print(f"✅ Example {i} completed successfully")
        except Exception as e:
            print(f"❌ Example {i} failed: {str(e)}")
            results[f"example_{i}"] = {"error": str(e)}
        
        # Small delay between examples
        await asyncio.sleep(2)
    
    print("\n" + "=" * 50)
    print("🎉 All examples completed!")
    print(f"📊 Results summary: {len([r for r in results.values() if 'error' not in r])}/{len(examples)} successful")
    
    return results


if __name__ == "__main__":
    print("🚀 Browser Agent Example Script")
    print("Choose an example to run:")
    print("1. Simple Form Filling")
    print("2. Job Application (requires OpenAI API key)")
    print("3. Data Extraction")
    print("4. Multi-step Workflow")
    print("5. Memory-Enhanced Forms")
    print("6. Run All Examples")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    examples_map = {
        "1": example_1_simple_form_filling,
        "2": example_2_job_application,
        "3": example_3_data_extraction,
        "4": example_4_multi_step_workflow,
        "5": example_5_form_with_memory,
        "6": run_all_examples
    }
    
    if choice in examples_map:
        print(f"\n🎯 Running example {choice}...")
        result = asyncio.run(examples_map[choice]())
        print(f"\n✨ Example completed! Check 'agent_memory.json' for saved memory.")
    else:
        print("❌ Invalid choice. Please run the script again and choose 1-6.") 
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.website import WebsiteTools
from agno.knowledge.json import JSONKnowledgeBase
from agno.knowledge.text import TextKnowledgeBase
from agno.vectordb.pgvector import PgVector, SearchType

from knowledge_base import knowledge_base

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
job_url="https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/Israel-Yokneam/Senior-DevOps-Engineer_JR1985737?q=devops"

load_dotenv()

agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile",temperature=0),
    description="You are personal assistant helping me fill job applications",
    tools=[WebsiteTools(), DuckDuckGoTools()],      # Add DuckDuckGo tool to search the web
    knowledge=knowledge_base,
    add_context=True,
    search_knowledge=True,           # Search knowledge base for tool calls
    show_tool_calls=True,           # Shows tool calls in the response, set to False to hide
    debug_mode=True,
    markdown=True                   # Format responses in markdown
)

agent.knowledge.load(recreate=False)
text = f"Open {job_url} and find fields that I can fill up,find selenium selectors"
agent.print_response(text, stream=True)
agent.print_response("how can I make you fill forms", stream=True)

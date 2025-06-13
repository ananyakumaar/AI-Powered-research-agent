from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from wrapper import ChatGemini  # ✅ Ensure this file is named correctly
from my_tools import search, wiki, save  # ✅ Updated tool imports
import re
import json

# 🔑 Load API Key
load_dotenv()

# 🌟 Initialize LLM
llm = ChatGemini()

# 🏗️ Research Response Model
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]
    full_report: str  # New field for the full report

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# 🔍 Define Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Research the following question and generate a detailed research report. Return your answer as a JSON object with the following fields: topic, summary, sources, tools_used, and full_report (which should be a well-structured, multi-paragraph report). Use this format: {format_instructions}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}")
    ]
).partial(format_instructions=parser.get_format_instructions())

# 🛠️ Define and Bind Tools
tools = [search, wiki, save]  # ✅ Define first
llm.bind_tools(tools)  # ✅ Now bind them

# 🤖 Create LangChain Agent
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 🔎 Ask User for Research Query
query = input("What can I help you research? ")

# Invoke the agent and parse the output
raw_response = agent_executor.invoke({"query": query})

# 📝 Parse & Display Structured Output
try:
    raw_output = raw_response.get("output")
    if raw_output.startswith("```json"):
         json_str = re.sub(r"```json\n|\n```", "", raw_output).strip()
    else:
         fallback_json = { "topic": "Fallback Topic", "summary": "Fallback summary (agent did not return a JSON block.)", "sources": [], "tools_used": [], "full_report": "No report generated." }
         json_str = json.dumps(fallback_json)
    parsed_json = json.loads(json_str)
    raw_response["output"] = [{"text": json_str}]
    structured_response = parser.parse(raw_response.get("output")[0]["text"])
    print("\n📄 Structured Research Response:\n", structured_response)
    print("\n📝 Full Report:\n", structured_response.full_report)
except Exception as e:
    print("❌ Error parsing response:", e, "\nRaw Response:", raw_response)

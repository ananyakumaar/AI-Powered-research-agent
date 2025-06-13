# AI-Powered-research-agent

This project is a research report generator built using LangChain and a custom LLM wrapper (ChatGemini). It uses a tool-calling agent (with tools such as search, wiki, and save) to gather information and generate a detailed research report (in JSON format) on a given topic.

## Overview

- **Purpose:**  
  The script (`llm.py`) prompts the user for a research query, then uses a custom LLM (ChatGemini) and a tool-calling agent (using tools like search, wiki, and save) to generate a detailed report. The report is returned as a JSON object (with fields such as topic, summary, sources, tools used, and a full report) and is parsed using a Pydantic schema.

- **Key Components:**
  - **Custom LLM Wrapper:**  
    A wrapper (`wrapper.py`) for a Gemini-based LLM (ChatGemini) that is compatible with LangChain.
  - **Pydantic Schema:**  
    A `ResearchResponse` model (in `llm.py`) that defines the output structure (topic, summary, sources, tools used, and a full report).
  - **Prompt Template:**  
    A prompt instructing the agent to research a query and return a detailed report in JSON format.
  - **Tool-Calling Agent:**  
    An agent (created using `create_tool_calling_agent`) that uses custom tools (search, wiki, save) to gather information and generate the report.
  - **Output Parser:**  
    A Pydantic output parser that validates and parses the agent's output into a structured `ResearchResponse` object.

## Setup

1. **Clone the Repository:**  
   Clone (or download) this repository to your local machine.

2. **Install Dependencies:**  
   Ensure you have Python (3.8 or later) installed. Then, install the required packages (for example, using a virtual environment):

   ```bash
   pip install -r requirements.txt
   ```

   (If you do not have a `requirements.txt`, install the following packages manually:  
   – `python-dotenv` (for loading environment variables)  
   – `pydantic` (for data validation)  
   – `langchain` (for prompt templates, output parsers, and agents)  
   – (and any other dependencies used by your custom tools or LLM wrapper.)

3. **Set Up Environment Variables:**  
   Create a `.env` file in the project root (or in the same directory as `llm.py`) and add your API keys (for example, for your LLM or any external tools). For example:

   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   (Add any other API keys or secrets as needed.)
   ```

## Running the Script

- Open a terminal (or command prompt) and navigate to the project directory.
- Run the script using Python:

  ```bash
  python llm.py
  ```

- You will be prompted to enter a research query. The agent will then gather information (using the tools) and generate a detailed report (in JSON format) that is printed to the console.

## Code Explanation

- **`llm.py`:**  
  This is the main script. It loads environment variables, initializes the custom LLM (ChatGemini), defines a Pydantic schema (`ResearchResponse`), sets up a prompt template (with a system message instructing the agent to generate a detailed report), defines and binds custom tools (search, wiki, save), creates a tool-calling agent (using `create_tool_calling_agent`), and then invokes the agent. The agent's output (a JSON string) is parsed (using a Pydantic output parser) and printed (both the structured response and the full report).

- **`wrapper.py`:**  
  Contains a custom wrapper (`ChatGemini`) for a Gemini-based LLM so that it is compatible with LangChain (for example, it wraps the LLM's output in a `ChatGeneration` object).

- **`my_tools.py`:**  
  Contains custom tools (for example, a search tool, a wiki tool, and a save tool) that the agent can use to gather information.

- **`README.md`:**  
  (This file) Explains the project's purpose, setup, and usage.

## Troubleshooting

- **API Key Issues:**  
  Ensure that your `.env` file is correctly set up and that your API keys are valid.
- **Parsing Errors:**  
  If the agent's output is not a valid JSON block (or does not conform to the schema), a fallback JSON is used (with a "No report generated" message). Check the agent's prompt and tools if you see unexpected output.

## Further Customization

- **Modify the Prompt:**  
  You can update the prompt (in `llm.py`) to instruct the agent differently (for example, to generate a report in a different style or format).
- **Add or Modify Tools:**  
  You can add (or modify) custom tools in `my_tools.py` (or in a separate module) to gather additional information.
- **Extend the Output Schema:**  
  You can add more fields (or change the structure) in the `ResearchResponse` model (in `llm.py`) to suit your reporting needs.

---

Happy researching! 

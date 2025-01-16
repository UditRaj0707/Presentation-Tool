from tools import Presentationtools
from tools import use_presentation
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from load_dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
load_dotenv()

class PresentationAgent:
    def __init__(self, llm="llama"):
        self.presentationtools = Presentationtools()

        if llm == "llama":
            self.llm = ChatGroq(
                model="llama3-70b-8192", 
                temperature=0.1,
                api_key=os.environ["GROQ_API_KEY"]
            )
        else:
            self.llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash", 
                    temperature=0.1,
                    api_key=os.environ["GOOGLE_API_KEY"]
                )
        self.tools = self.presentationtools.get_tools()
        # print("Available Tools:", self.tools)

        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.system_prompt = """
        You are an Expert Presentation Maker Agent. You have access to specialized tools for creating PowerPoint slides. Based on the user's request, you can use one or more tools in sequence to build the presentation.

        ### Your Objective:
        - Understand the user’s query.
        - Choose the correct tool(s).
        - Execute them in the correct order.
        - Use multiple tools if the query requires.

        ### Available Tools:
        - add_text_with_image_slide
        - add_image_slide
        - add_bullet_slide
        - add_two_content_bullet_slide
        - add_table_slide
        - add_bar_chart
        - add_scatter_plot
        - add_area_chart
        - add_line_chart
        - add_pie_chart
        ---

        ### Examples:**

        **Example 1:**  
        **User Query:** *"Create a slide with a bar chart showing sales data and another slide with product features."*  
        **Step-by-Step Action:**  
        1. **Tool:** `add_single_column_chart`  
        - **Args:** `categories_str="Q1, Q2, Q3, Q4"`, `values_str="5000, 7000, 8000, 6500"`  
        2. **Tool:** `add_bullet_slide`  
        - **Args:** `title="Product Features"`, `content="High Performance; User-Friendly; Affordable"`

        ---

        **Example 2:**  
        **User Query:** *"Add a slide with a company logo and create a comparison table of competitors."*  
        **Step-by-Step Action:**  
        1. **Tool:** `add_image_slide`  
        - **Args:** `image_path="company_logo.png"`, `caption="Our Company Logo"`  
        2. **Tool:** `add_table_slide`  
        - **Args:** `table_data="Brand, Price, Features; Brand A, $500, Basic; Brand B, $700, Premium"`

        ---

        **Example 3:**  
        **User Query:** *"Create a summary slide with two columns: one for strengths and one for weaknesses."*  
        **Step-by-Step Action:**  
        1. **Tool:** `add_two_content_bullet_slide`  
        - **Args:**  
            - `title="SWOT Analysis"`  
            - `left_content="Strong Brand; Loyal Customers; Market Leader"`  
            - `right_content="High Costs; Limited Innovation; Market Saturation"`

        ---

        ### ** Instructions:**
        - Break down complex queries into steps. 
        - If data is not provided, use some random placeholder data. 
        - Use correct format of the arguments.
        - Use **multiple tools** if necessary.  
        - There may be multiple similar tools for a task. Choose the most appropriate one.
        - Maintain the correct execution order.  
        - Respond only after all tool calls are completed.

        """


    def process_query(self, query):
        messages = [SystemMessage(content=self.system_prompt), HumanMessage(content=query)]

        try:
            print("Sending Query to LLM...")
            response = self.llm_with_tools.invoke(messages)
            print("Tool invoked successfully.")
            print("Tool Calls:", response.tool_calls)

            tool_calls = response.additional_kwargs.get('tool_calls', [])
            if not tool_calls:
                print("No tool calls found.")
                return "Tool executed, but no tool calls were triggered."

            results = []

            # Process ALL tool calls in sequence
            for i, call in enumerate(tool_calls, start=1):
                print(f"Processing Tool Call {i}/{len(tool_calls)}: {call}")

                # Extract tool name and arguments
                tool_name = call.get('name') or call.get('function', {}).get('name')
                args = call.get('args') or call.get('function', {}).get('arguments')

                # Handle JSON string arguments
                if isinstance(args, str):
                    import json
                    args = json.loads(args)

                # Check if the tool exists
                if hasattr(self.presentationtools, tool_name):
                    tool_func = getattr(self.presentationtools, tool_name)
                    result = tool_func(**args)
                    print(f"Result from {tool_name}: {result}")
                    results.append(result)
                else:
                    print(f"Tool '{tool_name}' not found.")
                    results.append(f"Tool '{tool_name}' not found.")

            return results

        except Exception as e:
            print(f"Error invoking tool: {e}")
            return f"Error: {e}"



if __name__ == "__main__":
    ppt = Presentationtools()
    info_for_user = """Example Queries:
    1. Create a slide with a single column chart showing categories A, B, C, D and values 1, 2, 3, 4
    2. Create a slide with an image of a logo
    3. Create a slide with bullet points: First point, Second point, Third point
    4. Show to display the existing presentations to edit them
    5. Help to list all available tools
    6. Exit to end the program\n
[Presentation Agent] Enter your query: """
    agent = PresentationAgent()
    run = True
    while run:

        query = input(info_for_user)
        if query.strip().lower() == "exit":
            run = False
            break

        if query.strip().lower() == "help":
            available_tools = [tool.name for tool in agent.tools]
            print(f"Available tools: {', '.join(available_tools)}")
            continue

        if query.strip().lower() == "show":
            if os.path.exists("input"):
                files = os.listdir("input")
                ppt_files = [file for file in files if file.endswith(".pptx")]
                if ppt_files:
                    print("Select a file to edit:")
                    for i, file in enumerate(ppt_files, start=1):
                        print(f"{i}. {file}")
                    selected_file = int(input("Enter the number corresponding to the file: "))
                    if selected_file in range(1, len(ppt_files)+1):
                        print(f"Opening {ppt_files[selected_file-1]} for editing...")
                        use_presentation(folder_path="input", file_path=ppt_files[selected_file-1])
                    else:
                        print("Invalid selection.")
                else:
                    print("Currently there are no presentations to edit.")
            continue
        response = agent.process_query(query)
        
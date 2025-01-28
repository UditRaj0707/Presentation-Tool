from tools import Presentationtools
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from load_dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
load_dotenv()

class PresentationAgent:
    def __init__(self, llm="gemini", mode="normal"):
        if mode != "normal":
            self.presentationtools = Presentationtools(mode=mode)
        else:
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
        - add_waterfall_chart
        - add_title_slide
        ---

        ### **Examples**

        **Example 1: Single Tool Call**  
        **User Query:** *"Create a slide with a pie chart showing market share distribution."*  
        **Step-by-Step Action:**  
        1. **Tool:** `add_pie_chart`  
        - **Args:**  
            - `categories_str="Product A, Product B, Product C"`  
            - `values_str="40, 35, 25"`  
            - `title="Market Share Distribution"`  
            - `plot_name="Market Share"`  

        ---
        **Example 2: Single Tool Call with insertion**  
        **User Query:** *"Insert a slide with a pie chart showing market share distribution at 2nd index"*  
        **Step-by-Step Action:**  
        1. **Tool:** `add_pie_chart`  
        - **Args:**  
            - `categories_str="Product A, Product B, Product C"`  
            - `values_str="40, 35, 25"`  
            - `title="Market Share Distribution"`  
            - `plot_name="Market Share"`
            - `insert_at=2`  

        ---

        **Example 3: Two Tool Calls**  
        **User Query:** *"Add a slide with the company logo and create a bullet slide for core values."*  
        **Step-by-Step Action:**  
        1. **Tool:** `add_image_slide`  
        - **Args:**  
            - `image_path="company_logo.png"`  
            - `caption="Our Company Logo"`  
            - `title="Welcome to Our Company"

        2. **Tool:** `add_bullet_slide`  
        - **Args:**  
            - `title="Core Values"`  
            - `content="Integrity; Innovation; Customer Focus; Sustainability"`  

        ---

        **Example 4: Four Tool Calls**  
        **User Query:** *"Create a business report with a bar chart of sales, a line chart of profit trends, a table of regional performance, and a summary of strategic goals."*  
        **Step-by-Step Action:**  
        1. **Tool:** `add_bar_chart`  
        - **Args:**  
            - `categories_str="Q1, Q2, Q3, Q4"`  
            - `series_data_str="Sales: 5000, 7000, 8000, 6500"`  
            - `title="Quarterly Sales Overview"`  

        2. **Tool:** `add_line_chart`  
        - **Args:**  
            - `categories_str="Q1, Q2, Q3, Q4"`  
            - `series_data_str="Profit: 1500, 2000, 2500, 2300"`  
            - `title="Profit Trends"`  

        3. **Tool:** `add_table_slide`  
        - **Args:**  
            - `table_data="Region, Sales, Growth; North, 5000, 10%; South, 7000, 15%; East, 6000, 12%"`  
            - `title="Regional Performance"`  

        4. **Tool:** `add_two_content_bullet_slide`  
        - **Args:**  
            - `title="Strategic Goals"`  
            - `left_content="Expand Market Share; Launch New Products; Improve Customer Service"`  
            - `right_content="Reduce Costs; Optimize Supply Chain; Increase Automation"`  

        ---

        ### ** Instructions:**
        - Break down complex queries into steps. 
        - If data is not provided, use some random placeholder data. 
        - Use correct format of the arguments.
        - Use **multiple tools** if necessary.  
        - There may be multiple similar tools for a task. Choose the most appropriate one.
        - Maintain the correct execution order.  
        - Respond only after all tool calls are completed.
        - If user has not given file paths, do not use tools that require file paths.
        - Whenever terms like "insert at X index" are mentioned, use the `insert_at` parameter. Do not use it otherwise.
        - Always pass pass integer values for `insert_at` parameter.

        """


    def process_query(self, query, mode="normal"):
        messages = [SystemMessage(content=self.system_prompt), HumanMessage(content=query)]

        try:
            print("Sending Query to LLM...")
            response = self.llm_with_tools.invoke(messages)
            print("Tool invoked successfully.")
            print("Tool Calls:", response.tool_calls)

            tool_calls = response.additional_kwargs.get('tool_calls', [])
            if not tool_calls:
                print("No tool calls found.")
                tool_calls = response.tool_calls
                

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

            return results[-1]

        except Exception as e:
            print(f"Error invoking tool: {e}")
            return f"Error: {e}"


def main():
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
                        Presentationtools.use_presentation(folder_path="input", file_path=ppt_files[selected_file-1])
                    else:
                        print("Invalid selection.")
                else:
                    print("Currently there are no presentations to edit.")
            continue
        response = agent.process_query(query)


if __name__ == "__main__":
    main()
        
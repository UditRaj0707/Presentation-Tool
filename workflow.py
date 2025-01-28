from typing import TypeVar, Annotated
from langgraph.graph import StateGraph, Graph, START, END
from pydantic import BaseModel
from typing import Dict, List
from ppt_agent import PresentationAgent
from template_prompts import TEMPLATE_PROMPTS
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits.polygon.toolkit import PolygonToolkit
from langchain_community.utilities.polygon import PolygonAPIWrapper
import os
from load_dotenv import load_dotenv
load_dotenv()

class PolygonSearchAgent:
    def __init__(self, llm="gemini"):
        if llm.startswith("llama"):
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

    def search(self, query):
        pass

class WorkflowState(BaseModel):
    selected_template: str = ""
    extracted_data: Dict[str, str] = {}
    template_path: str = ""

class TemplateWorkflow:
    def __init__(self):
        pass
        

    def create_graph(self):
        self.workflow = StateGraph(WorkflowState)
        self.workflow.add_node("extract_data", self.extract_data)
        self.workflow.add_node("route_template", self.route_template)

        self.workflow.add_edge("extract_data", "route_template")
        self.workflow.add_edge("route_template", END)

        self.workflow.set_entry_point("extract_data")

        return self.workflow

    def extract_data(self, state):
        # Simulate data extraction
        state.extracted_data = {"key": "value"}
        return state

    def route_template(self, state):
        # Template routing logic
        prompts = TEMPLATE_PROMPTS[state.selected_template]
        for prompt in prompts:
            file_path = self.ppt.process_query(prompt)

        state.template_path = file_path

        return state

    def run(self, selected_template):

        self.ppt = PresentationAgent(mode=selected_template)

        workflow = self.create_graph()

        graph = workflow.compile()

        config = {
            "selected_template": selected_template
            }
        
        result = graph.invoke(config)
        
        return result



# workflow = StateGraph(WorkflowState)
# workflow.add_node("extract_data", extract_data)
# workflow.add_node("route_template", route_template)
# workflow.set_entry_point("extract_data")
# workflow.add_edge("extract_data", "route_template")

# app = workflow.compile()



def main():
    mapping = {
        1: "month_end_closing",
        2: "quarterly_business_review",
        3: "strategic_review"
    }
    workflow = TemplateWorkflow()

    info_for_user = """
    Available Templates:
    1. Month End Closing
    2. Quarterly Business Review
    3. Strategic Reviews
    
    Select the number corresponding to the template you want to use: """

    run = True
    while run:
        user_input = int(input(info_for_user))

        if user_input in mapping.keys():
            selected_template = mapping[user_input]
            run = False
        else:
            print("Invalid selection.")
    
    results = workflow.run(selected_template)
    print(f"{selected_template} presentation created at {results['template_path']}")
    



if __name__ == "__main__":
    main()
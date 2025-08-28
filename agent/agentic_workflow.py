from asyncio import graph
from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool


# Creating a Class for Graph Construction which will initialize the entire graph workflow:
class GraphBuilder():

    def __init__(self , model_provider:str):

        # create an instance of ModelLoader class , model_provider will be initialized in app.py:
        self.model_loader = ModelLoader(model_provider=model_provider)

        # Call the load_llm method wrt to the model_loader instance: will load and initialize the groq model:
        self.llm = self.model_loader.load_llm()

        # initializing the tools list:
        self.tools = []

        # initializing the individual tool class:
        self.weather_tools = WeatherInfoTool()
        self.place_search_tools = PlaceSearchTool()
        self.calculator_tools = CalculatorTool()
        self.currency_converter_tools = CurrencyConverterTool()

        # extending the tools list with all available tools(for each individual tool):
        self.tools.extend([* self.weather_tools.weather_tool_list, 
                           * self.place_search_tools.place_search_tool_list,
                           * self.calculator_tools.calculator_tool_list,
                           * self.currency_converter_tools.currency_converter_tool_list])

        # Binding the tools to the LLM:
        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)

        self.system_prompt = SYSTEM_PROMPT

        self.graph = None

    # defining the chat node:
    def agent_function(self , state:MessagesState):
        user_input = state["messages"]
        input_question = [self.system_prompt] + user_input
        response = self.llm_with_tools.invoke(input_question)
        return {"messages": [response]}

    # function to initialize , built and compile the graph:
    def build_graph(self):
        graph_builder = StateGraph(MessagesState)

        # adding nodes:
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))

        # adding edges:(defining the ReAct Agent workflow(graph))
        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges(
            "agent", condition=tools_condition
        )
        graph_builder.add_edge("tools", "agent")
        graph_builder.add_edge("agent", END)

        # compiling
        self.graph = graph_builder.compile()

        # return
        return self.graph
    
    def __call__(self, *args, **kwds):
        # calling the build_graph function which returns a compiled graph:
        return self.build_graph()
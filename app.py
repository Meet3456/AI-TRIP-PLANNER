from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from agent.agentic_workflow import GraphBuilder

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class InputQueryRequest(BaseModel):
    question: str


@app.post("/process_query")
async def process_query(query: InputQueryRequest):
    try:
        graph = GraphBuilder(model_provider="groq")
        compiled_graph = graph()
        input_query = {"messages":[query.question]}
        response = compiled_graph.invoke(input_query)
        
        if isinstance(response,dict) and "messages" in response:
            # extracting th AIMessage content:
            final_output = response["messages"][-1].content
        else:
            final_output = str(response)

        return {"response": final_output}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

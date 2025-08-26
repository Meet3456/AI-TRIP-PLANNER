import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq

load_dotenv()
# Class for ConfigLoader
class ConfigLoader:
    def __init__(self):
        # will call the load_config function which returns a dictionary of the config file:
        print("Loading configuration...")
        self.config = load_config()
    
    def __getitem__(self,key):
        return self.config.get(key)

# Class for ModelLoader
class ModelLoader(BaseModel):

    model_provider: Literal["groq", "openai"] = Field(
        default="groq", 
        description="LLM provider to use"
    )

    config : Optional[ConfigLoader] = Field(
        default=None,
        exclude=True
    )

    # model_post_init is a inbuilt method of Pydantic's BaseModel , which is used to perform actions after the model is initialized(__init__ method ke baad)
    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()

    # As we are passing a non-standard object like(ConfigLoader) to the config , pydantic will raise error so 
    # You’re telling Pydantic: “Allow arbitrary Python objects (like custom classes, DB clients, file handles, etc.) as field values, without trying to validate or coerce them.”
    # So config will accept the ConfigLoader() instance(object) without any issues.
    class Config:
        arbitrary_types_allowed = True

    def load_llm(self):
        print("LLM Loading.....")

        if self.model_provider == "groq":
            print("Loading Groq model...")
            groq_api_key = os.getenv("GROQ_API_KEY")
            model_name = self.config["llm"].get("groq", {}).get("model_name")
            # model_name = self.config.__getitem__("llm").get("groq", {}).get("model_name")
            llm = ChatGroq(
                model = model_name,
                api_key = groq_api_key
            )
        print("LLM Loaded Successfully")
        return llm

















# obj = ConfigLoader()
# llm = obj.__getitem__('llm')
# model_name = llm.get('groq', {}).get('model_name')
# print(model_name)
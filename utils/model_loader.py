import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq

# Class for ConfigLoader
class ConfigLoader:
    def __init__(self):
        # will call the load_config function which returns a dictionary of the config file:
        print("Loading configuration...")
        self.config = load_config()
    
    def __getitem__(self,key):
        return self.config.get(key)

# Class for ModelLoader
class ModelLoader:
    model_provider: Literal["groq", "openai"] = "groq"
    config = Optional[ConfigLoader] = Field(default=None,exclude=True)
    
    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
    class Config:
        arbitrary_types_allowed = True

    def load_llm(self):
        print("LLM Loading.....")

        if self.model_provider == "groq":
            print("Loading Groq model...")
            groq_api_key = os.getenv("GROQ_API_KEY")
            model_name = self.config["llm"]["groq"]["model_name"]
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
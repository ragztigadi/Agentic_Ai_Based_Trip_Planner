import os 
from multiprocessing import context 
from dotenv import load_dotenv 
from typing import Literal, Optional, Any 
from pydantic import BaseModel, Field 
from utils.config_loader import load_config 
from langchain_gorq import ChatGorq
from langchain_gemini import ChatGemini 

class ConfigLoader:
    def __init__(self):
        print(f"Loaded config.....")
        self.config = load_config()
    
    def __getitem__(self, key):
        return self.config[key]
    
class ModelLoader(BaseModel):
    model_provider: Literal['gorq', 'gemini'] = 'gemini'
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()

    class Config:
        arbitrary_types_allowed = True  

    def load_llm(self):
        """
        Load and return the LLM Model.
        """

        print("LLM Model is Loading.....")
        print(f"Loading model from provider : {self.model_provider} model.....")
        
        if self.model_provider == 'gorq':
            print("Loading LLM from Groq..............")
            gorq_api_key = os.getenv('GORQ_API_KEY')
            model_name = self.config["llm"]["gorq"]["model_name"]
            llm = ChatGorq(model=model_name, api_key=gorq_api_key)
        
        elif self.model_provider == 'gemini':
            print("Loading LLM from Google Gemini..............")
            gemini_api_key = os.getenv('GOOGLE_API_KEY')  
            model_name = self.config["llm"]["gemini"]["model_name"]
            llm = ChatGemini(model=model_name, api_key=gemini_api_key)
        
        else:
            print("Model provider not supported yet.")
        
        return llm
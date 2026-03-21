import os 
from multiprocessing import context 
from dotenv import load_dotenv 
from typing import Literal, Optional, Any 
from pydantic import BaseModel, Field 
from utils.config_loader import load_config 
from langchain_google_genai import ChatGoogleGenerativeAI

try:
    from langchain_groq import ChatGroq
except ImportError:
    ChatGroq = None

load_dotenv()

class ConfigLoader:
    def __init__(self):
        print(f"Loaded config.....")
        self.config = load_config()
    
    def __getitem__(self, key):
        return self.config[key]
    
class ModelLoader(BaseModel):
    model_provider: Literal['groq', 'gemini'] = 'gemini'
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
        
        if self.model_provider == 'groq':
            if ChatGroq is None:
                raise ImportError("langchain_groq is not installed. Run: pip install langchain-groq")
            print("Loading LLM from Groq..............")
            groq_api_key = os.getenv('GROQ_API_KEY')
            model_name = self.config["llm"]["groq"]["model_name"]
            llm = ChatGroq(model=model_name, api_key=groq_api_key)
        
        elif self.model_provider == 'gemini':
            print("Loading LLM from Google Gemini..............")
            gemini_api_key = os.getenv('GOOGLE_API_KEY')  
            model_name = self.config["llm"]["gemini"]["model_name"]
            llm = ChatGoogleGenerativeAI(model=model_name, google_api_key=gemini_api_key)
        
        else:
            raise ValueError(f"Model provider '{self.model_provider}' not supported yet.")
        
        return llm
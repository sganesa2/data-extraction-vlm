import os
from dataclasses import dataclass

import instructor
import google.generativeai as genai

from src.llm_clients.default import InstructorLLM

@dataclass
class GeminiInstructorLLM(InstructorLLM):

    @property
    def api_key(self)->str:
        return os.getenv("GEMINI_API_KEY")
    
    @property
    def client(self)->instructor.Instructor|instructor.AsyncInstructor:
        model_name = self.llm_call_kwargs.pop("model")
        return instructor.from_gemini(
            client=genai.GenerativeModel(model_name=model_name),
            mode = self.mode,
            use_async=False
        )
    
    def client_config_init(self)->None:
        genai.configure(api_key=self.api_key)
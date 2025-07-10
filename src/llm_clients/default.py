import json
import ast
import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from abc import ABC, abstractmethod

import instructor
from pydantic import BaseModel
from groq import Groq

@dataclass
class InstructorLLM(ABC):
    mode: instructor.Mode
    llm_call_kwargs: dict

    @property
    def api_key(self):
        return os.getenv("GROQ_API_KEY")
    
    @property
    def client(self)->instructor.Instructor|instructor.AsyncInstructor:
        return instructor.from_groq(
            client=Groq(api_key=self.api_key),
            mode=self.mode
        )
    
    @abstractmethod
    def client_config_init(self)->None:
        pass

    
    def _get_formatted_prompt_string(self, prompt_file_name:str, input_variables_dict:dict|None)->str:
        prompt_file_path = Path(__file__).parent.parent.joinpath("prompt_schemas", prompt_file_name)
        with open(prompt_file_path,'r') as file:
            prompt_string = file.read()
        if not input_variables_dict:
            return prompt_string
        formatted_prompt_string = prompt_string.format_map(input_variables_dict)
        return formatted_prompt_string

    def _get_formatted_prompt(self, prompt_file_name:str, input_variables_dict:dict)->str|dict:
        formatted_prompt_string = self._get_formatted_prompt_string(prompt_file_name, input_variables_dict)
        formatted_prompt = ast.literal_eval(formatted_prompt_string)
        return formatted_prompt
    
    def generate(self, response_format:BaseModel, messages: Optional[list[dict]] = None, prompt_file_name: Optional[str] = None, input_variables_dict:Optional[dict] = None)->dict:
        self.client_config_init()

        if prompt_file_name:
            if not isinstance(input_variables_dict,dict):
                raise TypeError("Input variables dict needs to be of type dict!")
            prompt = self._get_formatted_prompt(prompt_file_name, input_variables_dict)
        elif messages:
            prompt = messages
        else:
            raise Exception("Provide a prompt_file_name or messages!")
        
        completion = self.client.chat.completions.create(
            messages=prompt,
            response_model=response_format,
            **self.llm_call_kwargs
        )
        if isinstance(completion,BaseModel):
            response = json.loads(completion.model_dump_json())
            return response
        raise ValueError("Response format not followed!!")
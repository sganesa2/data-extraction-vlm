import io
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pydantic import BaseModel
from pathlib import Path
from typing import Optional

import weave

from src.llm_clients.default import InstructorLLM

from src.file_utils.default import DefaultFileUtils
from src.file_utils.gemini import GeminiFileUtils

@dataclass
class DataExtractor(ABC):
    client: InstructorLLM
    file_utils: DefaultFileUtils|GeminiFileUtils

    def _get_media(self, file_paths:Optional[str|Path|list[str]|list[Path]] = None, media:Optional[list[str]|list[io.TextIOWrapper]] = None)->list[str]|list[io.TextIOWrapper]:
        if not media:
            if not file_paths:
                raise Exception("No media to extract data from!")
            media = self.file_utils.convert_pdf_to_image_and_upload(file_paths)
        return media
    
    @abstractmethod
    def extract_data(self, response_format:BaseModel, file_paths:Optional[str|Path|list[str]|list[Path]] = None, media:Optional[list[str]|list[io.TextIOWrapper]] = None)->dict:
        pass

@dataclass
class NonSerializableDataExtractor(DataExtractor):
    
    def _create_messages(self, media:list[str]|list[io.TextIOWrapper])->list[dict]:
        return [
            {
                "role":"system",
                "content":"""You're an Document AI Assistant who is an expert in extracting structured data from images."""
            },
            {
                "role":"user",
                "content":[
                    """<Task>: Extract structured data from the given image.""",
                    *media
                ]
            }
        ]
    
    @weave.op()
    def extract_data(self, response_format:BaseModel, file_paths:Optional[str|Path|list[str]|list[Path]] = None, media:Optional[list[str]|list[io.TextIOWrapper]] = None)->dict:
        media = self._get_media(file_paths, media)
        messages = self._create_messages(media)
        extracted_data = self.client.generate(response_format, messages)
        return extracted_data

@dataclass
class SerializableDataExtractor(DataExtractor):

    @weave.op()
    def extract_data(self, response_format:BaseModel, file_paths:Optional[str|Path|list[str]|list[Path]] = None, media:Optional[list[str]|list[io.TextIOWrapper]] = None)->dict:
        media = self._get_media(file_paths, media)
        input_variables_dict = {}
        extracted_data = self.client.generate(response_format=response_format, prompt_file_name="prompt.txt", input_variables_dict=input_variables_dict)
        return extracted_data
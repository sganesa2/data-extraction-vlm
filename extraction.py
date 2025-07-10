import json
from dataclasses import dataclass

from src.enum_config import LLMClientName

from src.file_utils.addtl_utils.pdf_to_image import PDF2ImageConverter
from src.file_utils.addtl_utils.azure import BlobStorageUtils

from src.data_extractors import DataExtractor
from src.config import (
    LLM_CLIENT_CONFIG, 
    DATA_EXTRACTOR_CONFIG, 
    FILE_UTILS_CONFIG
)

from extraction_input_state import ExtractionInputState

@dataclass
class DataExtraction:
    input_state: ExtractionInputState

    def llm_client(self)->None:
        llm_client = LLM_CLIENT_CONFIG[self.input_state['llm_client_name']]
        self.input_state['llm_client'] = llm_client(
            self.input_state['mode'],
            self.input_state['llm_call_kwargs']
        )
    
    def pdf2image_converter(self)->None:
        self.input_state['pdf2image_converter'] = PDF2ImageConverter(
            self.input_state['output_file_path'],
            self.input_state['temp_storage_folder'],
            **self.input_state['pdf2image_converter_kwargs']
        )

    def blob_storage_utils(self)->None:
        self.input_state['blob_storage_utils'] = BlobStorageUtils(
            container_name=self.input_state.get('container_name'),
            account_name=self.input_state.get('account_name'),
            account_key=self.input_state.get('account_key'),
            connection_string=self.input_state.get('connection_string')
        )

    def file_utils(self)->None:
        file_utils = FILE_UTILS_CONFIG[self.input_state['llm_client_name']]
        if self.input_state['llm_client_name']==LLMClientName.GEMINI:
            self.input_state['file_utils'] = file_utils(
                self.input_state['pdf2image_converter']
            )
        elif self.input_state['llm_client_name']==LLMClientName.DEFAULT:
            self.input_state['file_utils'] = file_utils(
                self.input_state['blob_storage_utils'],
                self.input_state['pdf2image_converter']
            )
        else:
            raise TypeError("Unsupported MODEL!")
    
    def data_extractor(self)->DataExtractor:
        extractor = DATA_EXTRACTOR_CONFIG[self.input_state['data_extractor_type']]
        self.input_state['data_extractor'] = extractor(
            client= self.input_state['llm_client'],
            file_utils= self.input_state['file_utils']
        )
    def extract_data(self)->dict:

        self.llm_client()
        self.pdf2image_converter()
        self.blob_storage_utils()
        self.file_utils()
        self.data_extractor()

        response = self.input_state['data_extractor'].extract_data(
            response_format=self.input_state['response_format'],
            file_paths=self.input_state['pdf_paths']
        )
        with open(self.input_state['response_file_path'], 'w') as f:
            json.dump(response, f)
        return response
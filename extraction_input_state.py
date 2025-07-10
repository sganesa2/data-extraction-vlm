from typing import TypedDict, Optional
from pathlib import Path

import instructor
from pydantic import BaseModel

from src.file_utils.addtl_utils.pdf_to_image import PDF2ImageConverter
from src.file_utils.addtl_utils.azure import BlobStorageUtils

from src.llm_clients.default import InstructorLLM
from src.file_utils.default import DefaultFileUtils
from src.file_utils.gemini import GeminiFileUtils
from src.data_extractors import DataExtractor

from src.enum_config import LLMClientName, DataExtractorType

class ExtractionInputState(TypedDict):
    """config inputs"""
    llm_client_name: LLMClientName
    data_extractor_type: DataExtractorType

    """llm inputs"""
    mode: instructor.Mode
    llm_call_kwargs: dict
    response_format: BaseModel

    """file util inputs"""
    pdf_paths: list[Path]

    """pdf2image_converter_kwargs"""
    output_file_path:Path
    temp_storage_folder: Path
    pdf2image_converter_kwargs: Optional[dict]

    """blob storage inputs"""
    container_name:str
    connection_string: Optional[str] = None
    account_name:Optional[str] = None
    account_key:Optional[str] = None

    """response op file path"""
    response_file_path: Path

    """primary utlities: WILL BE CREATED"""
    llm_client: InstructorLLM
    pdf2image_converter: PDF2ImageConverter
    blob_storage_utils: Optional[BlobStorageUtils]
    file_utils: DefaultFileUtils|GeminiFileUtils
    data_extractor: DataExtractor


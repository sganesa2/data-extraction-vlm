from src.enum_config import LLMClientName, DataExtractorType

from src.llm_clients.default import InstructorLLM
from src.llm_clients.gemini import GeminiInstructorLLM

from src.file_utils.default import DefaultFileUtils
from src.file_utils.gemini import GeminiFileUtils

from src.data_extractors import SerializableDataExtractor, NonSerializableDataExtractor

LLM_CLIENT_CONFIG = {
    LLMClientName.DEFAULT: InstructorLLM,
    LLMClientName.GEMINI: GeminiInstructorLLM
}

FILE_UTILS_CONFIG = {
    LLMClientName.DEFAULT: DefaultFileUtils,
    LLMClientName.GEMINI: GeminiFileUtils
}

DATA_EXTRACTOR_CONFIG = {
    DataExtractorType.SERIALIZABLE: SerializableDataExtractor,
    DataExtractorType.NONSERIALIZABLE: NonSerializableDataExtractor
}
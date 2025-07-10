from enum import StrEnum

class LLMClientName(StrEnum):
    DEFAULT = "default"
    GEMINI = "gemini"
    GROQ = "groq"

class DataExtractorType(StrEnum):
    SERIALIZABLE = "serializable"
    NONSERIALIZABLE = "non_serializable"

class ExtractionDomain(StrEnum):
    WIRE = "wire"
    
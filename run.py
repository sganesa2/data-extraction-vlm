from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

import instructor
from json import dump

from src.prompt_utils.schemas.response_format import DataExtractionSchema
from src.enum_config import LLMClientName, DataExtractorType
from src.prompt_utils.dynamic_model_creation import DataExtractionPromptCreation

from extraction import DataExtraction
from extraction_input_state import ExtractionInputState


if __name__=="__main__":
    prompt_configs_heirarchy_dict={r'form_type_documents':True}
    dynamic_model = DataExtractionPromptCreation(
        prompt_configs_heirarchy_dict=prompt_configs_heirarchy_dict,
        add_base_fields=False
    ).create_dynamic_model()

    with open(r"./a.json", 'w') as f:
        dump(f,dynamic_model.model_dump_json())

    input_state = ExtractionInputState(
        llm_client_name = LLMClientName.GEMINI,
        data_extractor_type = DataExtractorType.NONSERIALIZABLE,
        mode= instructor.Mode.GEMINI_JSON,
        llm_call_kwargs= {"model":"gemini-1.5-pro-latest"},
        response_format= dynamic_model,
        pdf_paths= [Path(r'./src/documents/Barcodes - 300 Shop - Quote Only.pdf')],
        output_file_path= Path(r'./src/documents/concatenated_image.png'),
        temp_storage_folder= Path(r"./src/documents"),
        pdf2image_converter_kwargs = {"orientation":"horizontal"},
        # container_name:str
        # connection_string: Optional[str] = None
        # account_name:Optional[str] = None
        # account_key:Optional[str] = None
        response_file_path= Path(r'./src/documents/op2.json')
    )
    extraction_tool = DataExtraction(input_state=input_state)
    resp = extraction_tool.extract_data()

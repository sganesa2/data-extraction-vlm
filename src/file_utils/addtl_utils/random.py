import base64
from pathlib import Path

from pydantic import BaseModel

def encode_image_for_tgi(image_path:Path)->str:
    with open(image_path,'rb') as f:
        b64_image = base64.b64encode(f.read()).decode("utf-8")
    encoded_image = f"data:image/{image_path.suffix};base64,{b64_image}"
    return encoded_image

def create_json_schema(response_format:BaseModel, additional_properties:bool = False, strict:bool = True)->dict:
    schema = response_format.model_json_schema()
    response_type = "json"
    if strict:
        response_type = "json_object"
    return {
        "type": response_type,
        "value":{
            **schema,
            "additionalProperties":additional_properties
        }
    }
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from pydantic import BaseModel, create_model

@dataclass
class DataExtractionPromptCreation:
    prompt_configs_heirarchy_dict: dict[str,bool] = field(default_factory= lambda: {})
    add_base_fields: bool = field(default=True)
    prompt_config_dir: Path = field(default_factory= lambda: Path(r".\src\prompt_utils\configs"))
    po_fields_pattern: str = r"*po_fields.json"
    lineitem_fields_pattern: str = r"*lineitem_fields.json"
    type_mapping:dict = field(default_factory=lambda : {
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
            "dict": dict,
            "list": list,
            "list[str]": list[str]
    })

    def order_of_model_creation(self)->list[Callable[[Any], BaseModel]]:
        return [
            self._create_lineitem_fields_model,
            self._create_po_fields_model
        ]

    def prompt_configs_hreq_dict(self)->dict[Path, bool]:
        if not self.prompt_configs_heirarchy_dict:
            return {self.prompt_config_dir:False}

        configs_hreq_dict = {self.prompt_config_dir.joinpath(dir_name): heirarchy_req for dir_name, heirarchy_req in self.prompt_configs_heirarchy_dict.items()}
        if not self.add_base_fields:
            return configs_hreq_dict
        return {**configs_hreq_dict,self.prompt_config_dir:False}
    
    def _create_fields(self, pattern:str)->dict:
        configs_hreq_dict = self.prompt_configs_hreq_dict()

        fields = {}
        fields_config_paths = []
        for dir, heirarchy_req in configs_hreq_dict.items():
            if heirarchy_req:
                fields_config_paths.extend([*dir.rglob(pattern)])
            else:
                fields_config_paths.extend([*dir.glob(pattern)])

        for config_file in fields_config_paths:
            with open(config_file, 'r') as f:
                current_fields = json.load(f)['fields']
            fields.update(current_fields)

        return fields
    
    def _create_pydantic_fields(self, pattern:str)->dict:
        pydantic_fields = {}
        all_po_fields = self._create_fields(pattern)
        for field, value in all_po_fields.items():
            var_type, description = value['type'], value['description']
            if var_type not in self.type_mapping:
                raise Exception("1)You did not follow the model creation heirarchy! or 2) You have a wrong type name in your config file!")
            
            type_annotation = self.type_mapping[var_type]
            pydantic_fields.update({field: (type_annotation, description)})
        return pydantic_fields

    def _create_lineitem_fields_model(self)->None:
        lineitem_pydantic_fields = self._create_pydantic_fields(self.lineitem_fields_pattern)
        if not lineitem_pydantic_fields:
            raise Exception("No lineitem fields created!")
        lineitem_model = create_model("LineItem", **lineitem_pydantic_fields)
        self.type_mapping.update({
            "LineItem":lineitem_model,
            "list[LineItem]": list[lineitem_model]
        })

    def _create_po_fields_model(self)->None:
        po_pydantic_fields = self._create_pydantic_fields(self.po_fields_pattern)
        if not po_pydantic_fields:
            raise Exception("No po fields created!")
        po_model = create_model("PurchaseOrder", **po_pydantic_fields)
        self.type_mapping.update({
            "PurchaseOrder":po_model,
        })

    def create_dynamic_model(self)->BaseModel:
        list(map(lambda func: func(), self.order_of_model_creation()))
        return self.type_mapping['PurchaseOrder']

if __name__=="__main__":
    creator = DataExtractionPromptCreation(
        prompt_config_dir=Path(r'D:\d2r-explorations\data-extraction\src\prompt_utils\configs'),
        prompt_configs_heirarchy_dict={r"wire_domain":True},
        add_base_fields=True
    )
    model = creator.create_dynamic_model()
    print(model)
    with open(r"D:\d2r-explorations\data-extraction\src\prompt_utils\model_fields.json", 'w') as file:
        json.dump(model.model_json_schema(),file)
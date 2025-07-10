from dataclasses import dataclass
from typing import Optional
from pathlib import Path

from src.file_utils.addtl_utils.pdf_to_image import PDF2ImageConverter
from src.file_utils.addtl_utils.azure import BlobStorageUtils

@dataclass
class DefaultFileUtils:
    blob_storage_utils: BlobStorageUtils
    pdf2image_converter: Optional[PDF2ImageConverter] = None

    def _create_mapping_for_blob(self, fp:Path, temp_dir:str = "temp_dir")->dict:
        blob_path = "/".join([temp_dir,fp.name])
        with open(fp,'rb') as file:
            data = file.read()
        return {blob_path:data}
    
    def _upload_files(self, file_paths:Path|list[Path])->list[str]:
        blob_mapping = {}
        if isinstance(file_paths, list):
            for fp in file_paths:
                blob_mapping.update(self._create_mapping_for_blob(fp))
        else:
            blob_mapping.update(self._create_mapping_for_blob(file_paths))
        file_urls = self.blob_storage_utils.upload_blob_and_get_sas_urls(blob_mapping)
        return file_urls
    
    def convert_pdf_to_image_and_upload(self, pdf_paths:str|Path|list[str]|list[Path])->list[str]:
        if self.pdf2image_converter:
            self.pdf2image_converter.convert_pdfs_to_image(pdf_paths)
            file_urls = self._upload_files(self.pdf2image_converter.output_file_path)
            return file_urls
        return []
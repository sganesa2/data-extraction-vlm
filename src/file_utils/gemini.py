import io
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types.file import File

from src.file_utils.addtl_utils.pdf_to_image import PDF2ImageConverter

@dataclass
class GeminiFileUtils:
    pdf2image_converter: Optional[PDF2ImageConverter] = None

    def _upload_single_file(self, file_path:str|Path)->io.TextIOWrapper:
        file = genai.upload_file(file_path)

        # Wait for file to finish processing
        while file.state != File.State.ACTIVE:
            time.sleep(1)
            file = genai.get_file(file.name)
            print(f"File is still uploading, state: {file.state}")
        return file

    def _upload_files(self, file_paths:str|Path|list[str]|list[Path])->list[io.TextIOWrapper]:
        if isinstance(file_paths,list):
            files = list(map(self._upload_single_file,file_paths))
        elif isinstance(file_paths,str) or isinstance(file_paths,Path):
            files = [self._upload_single_file(file_paths)]
        else:
            raise TypeError("Pdf paths is of incorrect type!")
        return files
    
    def convert_pdf_to_image_and_upload(self, pdf_paths:str|Path|list[str]|list[Path])->list[io.TextIOWrapper]:
        if self.pdf2image_converter:
            self.pdf2image_converter.convert_pdfs_to_image(pdf_paths)
            files = self._upload_files(self.pdf2image_converter.output_file_path)
            return files
        return []
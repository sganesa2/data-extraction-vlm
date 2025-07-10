import fitz
from PIL import Image
from pathlib import Path
from functools import partial
from dataclasses import dataclass, field
from random import randint

@dataclass
class PDF2ImageConverter:
    output_file_path:Path
    temp_storage_folder: Path

    image_ext:str = field(default= ".png")
    zoom:int = field(default=4)
    orientation:str = field(default="vertical")
    _pattern_start: str = field(default="revalgo_")
    _all_file_patterns: list[str] = field(default_factory= lambda:[])

    @property
    def image_file_pattern(self)->str:
        return f"{self._pattern_start}{randint(10000,20000)}"
    
    def _image_pattern(self, pattern_start:str)->str:
        return f"{pattern_start}*{self.image_ext}"

    def _temp_save_image(self, doc:fitz.Document, matrix:fitz.Matrix, save_path:Path, page_index:int)->None:
        page = doc.load_page(page_index)
        pix = page.get_pixmap(matrix=matrix)
        pix.save(save_path)
    
    def _delete_temp_images(self)->None:
        for patt in self._all_file_patterns:
            files_matching_pattern = self.temp_storage_folder.glob(self._image_pattern(patt))
            list(map(lambda file: file.unlink(), files_matching_pattern))
            

    def _concatenate_images(self)->None:
        """Concatenates images vertically or horizontally using PIL."""
        images = []
        for patt in self._all_file_patterns:
            images_of_current_patt = self.temp_storage_folder.glob(self._image_pattern(patt))
            image_objs = list(map(lambda path: Image.open(path), images_of_current_patt))
            images.extend(image_objs)

        if not images:
            raise Exception("No image files to concatenate")

        widths, heights = zip(*(i.size for i in images))

        if self.orientation == "vertical":
            new_width = max(widths)
            new_height = sum(heights)
            new_image = Image.new('RGB', (new_width, new_height))
            y_offset = 0
            for image in images:
                new_image.paste(image, (int((new_width - image.size[0])/2), y_offset)) # center the images
                y_offset += image.size[1]
        elif self.orientation == "horizontal":
            new_width = sum(widths)
            new_height = max(heights)
            new_image = Image.new('RGB', (new_width, new_height))
            x_offset = 0
            for image in images:
                new_image.paste(image, (x_offset, int((new_height - image.size[1])/2))) # center the images
                x_offset += image.size[0]
        else:
            raise ValueError("Invalid orientation. Choose 'vertical' or 'horizontal'.")

        new_image.save(self.output_file_path)

    def _single_pdf_to_image(self, pdf_path:str|Path, matrix:fitz.Matrix)->None:
        doc = fitz.open(pdf_path)
        current_pattern = self.image_file_pattern
        self._all_file_patterns.append(current_pattern)
        for i in range(doc.page_count):
            self._temp_save_image(doc,matrix, self.temp_storage_folder.joinpath(f"{current_pattern}_{i+1}{self.image_ext}"),i)
        doc.close()
    
    def _multiple_pdfs_to_image(self, pdf_paths:list[str]|list[Path], matrix:fitz.Matrix)->None:
        list(map(partial(self._single_pdf_to_image,matrix=matrix), pdf_paths))

    def convert_pdfs_to_image(self, pdf_paths:str|Path|list[str]|list[Path])->None:
        matrix = fitz.Matrix(self.zoom, self.zoom)

        if not self.temp_storage_folder.exists():
            self.output_file_path.mkdir()

        if isinstance(pdf_paths, str) or isinstance(pdf_paths,Path):
            self._single_pdf_to_image(pdf_paths, matrix)
        elif isinstance(pdf_paths, list):
            self._multiple_pdfs_to_image(pdf_paths, matrix)
        else:
            raise TypeError("Invalid type for pdf paths!")
        
        self._concatenate_images()
        self._delete_temp_images()
        self._all_file_patterns= []
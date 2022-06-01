import io
import os
import re

import fitz
from docx import Document
from google.cloud import vision
from loguru import logger

FILE_TYPE_MAP = {".pdf": "pdf", ".docx": "docx", ".txt": "txt"}


class TextExtractor:
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.file_type = ""
        self.text = ""

        self.extractor = {
            "pdf": self._pdf_extract,
            "docx": self._docx_extract,
            "image": self._image_extract,
            "txt": self._txt_extract,
        }

        self._file_type_validate()

    def _file_type_validate(self):
        logger.info("checking file type")
        self.file_type = FILE_TYPE_MAP.get(os.path.splitext(self.file_path)[-1], "image")

    def extract(self):
        self.extractor.get(self.file_type)()
        return self.text

    def _image_extract(self):
        logger.info("image parsing")
        image = io.open(self.file_path, "rb").read()
        image = vision.Image(content=image)
        client = vision.ImageAnnotatorClient()
        text = client.document_text_detection(image=image)
        texts = []
        for t in text.text_annotations:
            temp = {}
            temp["text"] = t.description
            temp["x0"] = t.bounding_poly.vertices[0].x
            temp["y0"] = t.bounding_poly.vertices[0].y
            texts.append(temp)
        texts = sorted(texts,key=lambda i:(i["y0"],i["x0"]))
        texts = [i.get("text") for i in texts]
        self.text = " ".join(texts)
        
    def _pdf_extract(self):
        logger.info("pdf parsing")
        doc = fitz.open(self.file_path)
        text = []
        for page in doc:
            text_details = page.get_text("words")
            page_text = self._extract_text(text_details)
            text.append(page_text)
        self.text = "\n".join(text)

    def _docx_extract(self):
        logger.info("docx parsing")
        document = Document(self.file_path)
        for p in document.paragraphs:
            self.text += f" {p.text}"

    def _txt_extract(self):
        logger.info("text parsing")
        with open(self.file_path, "r") as f:
            self.text = f.read()
        self.text = re.sub(r"\n", " ", str(self.text))

    def _extract_text(self, text_details, index=4):
        page_text = []
        for word_detail in text_details:
            page_text.append(word_detail[index])
        page_text = " ".join(page_text)
        return page_text

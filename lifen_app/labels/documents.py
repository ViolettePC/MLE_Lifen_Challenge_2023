from enum import Enum


class NeedsOCRCase(Enum):
    NO_OCR = "no_ocr"
    OCR = "ocr"


class KeywordsInNamesEnvironment(Enum):
    PATIENT = "patient"
    MONSIEUR = "monsieur"
    MADAME = "madame"

import pytest
import json
from lifen_app.models.document_input import DocumentInputSchema
from tests.conftest import TEST_DOCUMENTS_FILENAMES


@pytest.fixture()
def document_test_dict() -> dict:
    filename = TEST_DOCUMENTS_FILENAMES["document_test_0.json"]
    with open(filename) as f:
        document_dict = json.load(f)

    return document_dict


def test_raise_document_page_inconsistency(document_test_dict):
    document_test_dict["original_page_count"] = 2
    with pytest.raises(ValueError, match=r"Page number inconsistency"):
        _ = DocumentInputSchema(**document_test_dict)


def test_document_input_schema_ok(document_test_dict):
    _ = DocumentInputSchema(**document_test_dict)

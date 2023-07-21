from pathlib import Path
from glob import glob
import pytest
import json

TEST_DOCUMENTS_FILENAMES = {
    Path(f).name: f for f in glob(str(Path(__file__).parent / "documents" / "*.json"))
}


@pytest.fixture()
def document_test_dict() -> dict:
    filename = TEST_DOCUMENTS_FILENAMES["document_test_0.json"]
    with open(filename) as f:
        document_dict = json.load(f)

    return document_dict


@pytest.fixture()
def expected_response() -> dict:
    return {"first_name": "Jean", "last_name": "DUPONT"}

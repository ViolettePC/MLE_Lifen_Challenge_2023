from lifen_app.algo.patient_name_extractor import PatientNameExtractor


def test_extract_patient_name(document_test_dict, expected_response):
    detector = PatientNameExtractor(document_test_dict)
    patient_name = detector.extract_patient_name_by_keyword()

    assert patient_name.first_name == expected_response["first_name"]
    assert patient_name.last_name == expected_response["last_name"]


# TODO(Violette) Improve test by creating an hedge cases dict to parametrize.

from fastapi import APIRouter, status
from lifen_app.models.patient_info import PatientName
from lifen_app.algo.patient_name_extractor import PatientNameExtractor

__all__ = ["router"]

router = APIRouter()


@router.post(
    "/patient_name_detection",
    status_code=status.HTTP_200_OK,
    response_model=PatientName,
    tags=["Lifen App V0"],
)
async def post_patient_name_detected(request: dict):
    return PatientNameExtractor(request).extract_patient_name_by_keyword()

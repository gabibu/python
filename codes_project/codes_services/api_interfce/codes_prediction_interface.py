from singleton_decorator import singleton

from codes_services.services.codes_models.code_model import CodeModel
from codes_services.services.patient_services.patient_service import IPatientService
from codes_services.services.codes_models.entities.codes_model_predcition_request import CodesStatPredictionRequest
from codes_services.api_interfce.entities.codes_prediction_response import CodesPredictionResponse


@singleton
class CodesPredictionInterface:
    INSTANCE = None

    def __init__(self, codes_model: CodeModel, patient_service: IPatientService):
        self._codes_model = codes_model
        self._patient_service = patient_service
        CodesPredictionInterface.INSTANCE = self

    def predict_codes(self, patient_id: str, text: str) -> CodesPredictionResponse:
        prediction_request = CodesStatPredictionRequest(text=text)

        prediction_result = self._codes_model.predict(prediction_request)
        is_new_patient_response = self._patient_service.check_if_new_patient_and_insert_if_not(patient_id)

        return CodesPredictionResponse(patient_id=patient_id, text=text,
                                       code=prediction_result.code,
                                       is_new_patient=is_new_patient_response.is_new_patient)

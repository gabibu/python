from abc import ABC, abstractmethod
from codes_services.services.codes_models.entities.codes_model_prediction_result import CodeModelsPredictionResult
from codes_services.services.codes_models.entities.codes_model_predcition_request import CodesStatPredictionRequest


class CodeModel(ABC):

    @abstractmethod
    def predict(self, request: CodesStatPredictionRequest) -> CodeModelsPredictionResult:
        pass

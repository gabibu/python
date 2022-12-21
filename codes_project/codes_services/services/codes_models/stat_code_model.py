import numpy as np
from typing import Dict

from codes_services.services.codes_models.code_model import CodeModel
from codes_services.services.codes_models.entities.codes_model_prediction_result import CodeModelsPredictionResult
from codes_services.services.codes_models.entities.codes_model_predcition_request import CodesStatPredictionRequest


class StatCodeModel(CodeModel):

    def __init__(self, code_to_weight: Dict[str, float]):
        codes_weights_pairs = [(code, weight) for (code, weight) in code_to_weight.items()]

        self._codes = [code for (code, _) in codes_weights_pairs]
        self._weights = [weight for (_, weight) in codes_weights_pairs]

    def predict(self, request: CodesStatPredictionRequest) -> CodeModelsPredictionResult:
        predicted_code = np.random.choice(self._codes, size=1, p=self._weights)[0]

        return CodeModelsPredictionResult(code=predicted_code)

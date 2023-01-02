class CodesPredictionResponse:

    def __init__(self, patient_id: str, text: str, code: str, is_new_patient: bool):
        self.patient_id = patient_id
        self.text = text
        self.code = code
        self.is_new_patient = is_new_patient

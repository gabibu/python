class IsNewPatientResponse:

    def __init__(self, patient_id: str, is_new_patient: bool):
        self.patient_id = patient_id
        self.is_new_patient = is_new_patient

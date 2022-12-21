from abc import ABC, abstractmethod


class PatientDataFetcher(ABC):

    @abstractmethod
    def is_existing_patient(self, patient_id: str) -> bool:
        pass

    def insert_new_patient(self, patient_id: str):
        pass

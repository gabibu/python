from codes_services.services.patient_services.entities.is_new_patient_response import IsNewPatientResponse
from typing import List, Optional
import logging
from codes_services.services.patient_services.patient_data_fetcher import PatientDataFetcher
from abc import ABC, abstractmethod


class IPatientService(ABC):

    @abstractmethod
    def check_if_new_patient_and_insert_if_not(self, patient_id: str) -> IsNewPatientResponse:
        pass


class PatientService(IPatientService):

    def __init__(self, patient_service: PatientDataFetcher):
        self._patient_service = patient_service

    def check_if_new_patient_and_insert_if_not(self, patient_id: str) -> IsNewPatientResponse:

        if patient_id is None:
            raise Exception('patient_id cant be null')

        is_existing_patient = self._patient_service.is_existing_patient(patient_id)

        if not is_existing_patient:
            self._patient_service.insert_new_patient(patient_id)

        return IsNewPatientResponse(patient_id, not is_existing_patient)

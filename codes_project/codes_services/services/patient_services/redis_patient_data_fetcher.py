from codes_services.services.patient_services.patient_data_fetcher import PatientDataFetcher
import redis
from typing import Optional
import logging


class RedisPatientDataFetcher(PatientDataFetcher):
    PATIENT_KEY_FORMAT = 'patient_data_{}'

    def __init__(self, host: str, port: int, db: int):
        pool = redis.ConnectionPool(host=host, port=port, db=db)
        self._redis_client = redis.Redis(connection_pool=pool)

    def _pateint_data_key(self, patient_id: str) -> str:
        return RedisPatientDataFetcher.PATIENT_KEY_FORMAT.format(patient_id)

    def is_valid_patient_id(self, patient_id: str, raise_exception=True) -> Optional[bool]:

        if patient_id is None:
            if raise_exception:
                raise Exception('patient_id cant be null or empty')
            else:
                return False

        return True

    def is_existing_patient(self, patient_id: str) -> bool:

        self.is_valid_patient_id(patient_id)

        key = self._pateint_data_key(patient_id)

        return self._redis_client.exists(key)

    def insert_new_patient(self, patient_id: str):

        try:

            self.is_valid_patient_id(patient_id)

            key = self._pateint_data_key(patient_id)

            self._redis_client.set(key, str(True))

        except Exception as e:
            logging.exception('error inserting patient {}'.format(patient_id))
            raise e

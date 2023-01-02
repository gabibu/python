from abc import ABC
import logging
import pandas as pd

import yaml
from typing import Dict
from codes_services.services.patient_services.redis_patient_data_fetcher import RedisPatientDataFetcher
from codes_services.service_config import config_keys as CONFIG_KEYS
from codes_services.services.patient_services.patient_data_fetcher import PatientDataFetcher
from codes_services.api_interfce.codes_prediction_interface import CodesPredictionInterface
from codes_services.services.patient_services.patient_service import IPatientService, PatientService
from codes_services.services.codes_models.entities.code_model_type import CodeModelType
from codes_services.services.codes_models.stat_code_model import StatCodeModel
from codes_services.services.codes_models.code_model import CodeModel


class CodesPredictionServiceFactory(ABC):
    REDIS = 'REDIS'

    @staticmethod
    def _init_patient_data_fetcher(config: Dict) -> PatientDataFetcher:

        if config[CONFIG_KEYS.PATIENT_DATA_FETCHER_TYPE] == CodesPredictionServiceFactory.REDIS:
            redis_config = config[CONFIG_KEYS.REDIS]
            return RedisPatientDataFetcher(**redis_config)
        else:
            raise Exception(
                'PATIENT_DATA_FETCHER_TYPE {} is not valid'.format(config[CONFIG_KEYS.PATIENT_DATA_FETCHER_TYPE]))

    @staticmethod
    def _init_patient_service(config: Dict) -> IPatientService:
        return PatientService(patient_service=CodesPredictionServiceFactory._init_patient_data_fetcher(config))

    @staticmethod
    def init_codes_model(config: Dict) -> CodeModel:

        code_model_type = CodeModelType[config[CONFIG_KEYS.CODES_MODEL_TYPE]]

        logging.info('code_model_type {}'.format(code_model_type))

        if code_model_type == CodeModelType.STAT:
            codes_weights_df = pd.read_csv(config[CONFIG_KEYS.CODES_WEIGHTS_FILE_NAME])
            code_to_weight = dict(zip(codes_weights_df.code, codes_weights_df.weight))

            return StatCodeModel(code_to_weight)
        else:
            raise Exception('code_model_type {} is not valid'.format(code_model_type))

    @staticmethod
    def create_codes_prediction_service(config: Dict) -> CodesPredictionInterface:
        if config is None:
            raise Exception('config cant be null')

        patient_service = CodesPredictionServiceFactory._init_patient_service(config)

        return CodesPredictionInterface(CodesPredictionServiceFactory.init_codes_model(config), patient_service)

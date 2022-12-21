from flask import Flask, request, abort
from flask import jsonify
import argparse
import logging
import yaml
from codes_services.utils.logging import init_logger
from http import HTTPStatus
from codes_services.api_interfce.codes_prediction_interface_factory import \
    CodesPredictionServiceFactory
from codes_services.web_api_interfce.entities.codes_prediction_response import \
    CodesPredictionResponse
from codes_services.api_interfce.codes_prediction_interface import CodesPredictionInterface

init_logger()
codes_prediction_interface = None

app = Flask(__name__)


@app.route('/')
def index():
    return 'Code Model Server Is Running!'


@app.route('/predict', methods=['GET'])
def predict():
    try:
        logging.info('xxx')
        text = request.args.get('text', default=None, type=str)
        patient_id = request.args.get('patient_id', default=None, type=str)

        if text is None or patient_id is None:
            logging.error('text {} or patient_id {} are missing'.format(text, patient_id))
            abort(HTTPStatus.BAD_REQUEST)

        codes_prediction_response = CodesPredictionInterface.INSTANCE.predict_codes(patient_id, text)

        response = CodesPredictionResponse(patient_id=codes_prediction_response.patient_id,
                                           text=codes_prediction_response.text,
                                           code=codes_prediction_response.code,
                                           is_new_patient=codes_prediction_response.is_new_patient)

        return jsonify(response.__dict__)
    except:
        logging.exception('error in predict')
        abort(HTTPStatus.INTERNAL_SERVER_ERROR)


def main():
    global codes_prediction_interface

    parser = argparse.ArgumentParser(description='codes_models_interface')
    parser.add_argument('--config_file', type=str, required=True)
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()

    config_file_name = args.config_file
    port = args.port


    logging.info('initialize codes_prediction_service from config {} on port {}'.format(config_file_name, port))

    with open(config_file_name, 'r') as stream:
        config = yaml.safe_load(stream)

    codes_prediction_interface = CodesPredictionServiceFactory.create_codes_prediction_service(config)

    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()

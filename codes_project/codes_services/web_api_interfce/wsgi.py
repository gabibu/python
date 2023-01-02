from codes_services.web_api_interfce.codes_models_interface import app, main
from codes_services.utils.logging import init_logger

init_logger()
import logging

if __name__ == "__main__":
    logging.info('gabi')

    print('main')
    main()
    print('main')
    app.run()

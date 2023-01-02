import logging

LOG_FORMAT_MINIMAL = '%(asctime)s %(levelname)-7s %(message)s'


def init_logger(log_verbosity=logging.INFO, log_file=None, log_format=LOG_FORMAT_MINIMAL):
    formatter = logging.Formatter(log_format)

    base_logger = logging.getLogger()
    if not any(isinstance(handler, logging.StreamHandler) for handler in base_logger.handlers):
        output_handler = logging.StreamHandler()
        base_logger.addHandler(output_handler)

    if log_file is not None:
        file_handler = logging.FileHandler(log_file)
        base_logger.addHandler(file_handler)

    for handler in base_logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            handler.setFormatter(formatter)
    base_logger.setLevel(log_verbosity)

    logging.getLogger('azure').setLevel(logging.WARNING)

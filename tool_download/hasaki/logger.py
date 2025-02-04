import logging


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='hasaki_automation.log'
    )
    return logging.getLogger(__name__)
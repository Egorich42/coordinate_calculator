import logging

logging.basicConfig(format='%(asctime)s -[%(filename)s:%(lineno)d]   %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
import logging
import os
from datetime import datetime


def _LOGGER():

    Log_file=f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"
    Logs_path=os.path.join(os.getcwd(),"logs")
    os.makedirs(Logs_path,exist_ok=True)
    Log_file_path = os.path.join(Logs_path,Log_file)

    logger=logging.getLogger(__name__)
    Handler=logging.FileHandler(Log_file_path)
    Format=logging.Formatter('[%(asctime)s] :: %(levelname)s :: %(message)s',datefmt='%d/%m/%Y  %I:%M:%S %p')
    Handler.setFormatter(Format)
    Handler.setLevel(logging.INFO)
    logger.addHandler(Handler)
    logger.setLevel(logging.INFO)

    return logger

logger = _LOGGER()
import logging
import os
from datetime import datetime

class SingletoneType(type):
    def __call__(cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(SingletoneType, cls).__call__(*args, **kwargs)
            return cls.__instance

class Logger(object):
    __metaclass__ = SingletoneType
    _logger = None

    def __init__(self):
        self._logger = logging.getLogger("APP")
        self._logger.setLevel(logging.INFO)
        formatter = logging.Formatter("[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s")


        dirname = "./logs"

        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        fileHandler = logging.FileHandler(dirname + f"/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log")
        fileHandler.setFormatter(formatter)

        self._logger.addHandler(streamHandler)
        self._logger.addHandler(fileHandler)

    def get_logger(self):
        return self._logger
    
logger = Logger.__call__().get_logger()
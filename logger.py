import logging
import os

class SingletoneType(type):
    def __call__(cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(SingletoneType, cls).__call__(*args, **kwargs)
            return cls.__instance

class Logger(object):
    __metaclass = SingletoneType
    _logger = None

    def __init__(self):
        self._logger = logging.getLogger("APP")
        self._logger.setLevel(logging.INFO)
        formatter = logging.Formatter("[%(levelname)s|%(filename)s:%(linename)s] %(asctime)s > %(message)s")


        dirname = "./logs"

        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        # on devloping..
        # now, define and add handlers
        pass

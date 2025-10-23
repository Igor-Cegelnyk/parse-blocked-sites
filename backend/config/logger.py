import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
import os
import inspect
import pytz

KIEV_TZ = pytz.timezone("Europe/Kiev")


class Logger:
    def __init__(self):
        caller_frame = inspect.stack()[1]
        caller_path = self.caller_dir(caller_frame)
        caller_dir_name = os.path.basename(caller_path)

        self.log_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "log",
            caller_dir_name,
        )
        self.log_filename = os.path.join(self.log_dir, "log")
        self.logger = logging.getLogger(caller_dir_name)
        self.logger.setLevel(logging.INFO)
        self._setup_handler()

    def _setup_handler(self):
        os.makedirs(self.log_dir, exist_ok=True)
        log_file_path = os.path.join(self.log_dir, self.log_filename)
        handler = TimedRotatingFileHandler(
            filename=log_file_path,
            when="midnight",
            interval=1,
            backupCount=5,
        )

        stream_handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d - %(module)s - %(funcName)s - %(levelname)s - %(message)s"
        )
        formatter.converter = lambda ts: datetime.fromtimestamp(ts, KIEV_TZ).timetuple()
        handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.addHandler(stream_handler)

    @staticmethod
    def caller_dir(caller_frame: inspect.FrameInfo):
        caller_module = inspect.getmodule(caller_frame[0])
        caller_file_path = os.path.abspath(caller_module.__file__)
        caller_dir = os.path.dirname(caller_file_path)
        return caller_dir

    def get_logger(self) -> logging.Logger:
        return self.logger

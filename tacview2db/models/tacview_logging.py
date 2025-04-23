import logging
from logging import StreamHandler


class TacviewLogger:
    def __init__(self, log_file="app.log"):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Create a file handler
        file_handler = logging.FileHandler(log_file)

        # Create a console handler
        console_handler = logging.StreamHandler()

        # Set the log format
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


class TVLogger(StreamHandler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

        format = "%(asctime)s %(levelname)s %(message)s"
        datefmt = "%Y-%m-%d %H:%M:%S"

        formatter = logging.Formatter(format, datefmt)

        self.setFormatter(formatter)
        self.setFormatter()

    def emit(self, record):
        try:
            msg = self.format(record)
            self.text_widget.configure(state="normal")
            self.text_widget.insert("end", msg + "\n")
            self.text_widget.configure(state="disabled")
            self.text_widget.see("end")
        except Exception:
            self.handleError(record)

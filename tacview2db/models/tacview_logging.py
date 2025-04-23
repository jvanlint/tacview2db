import logging
from logging import StreamHandler


class TacviewLogger:
    """
    A custom logger wrapper for the Tacview application that provides
    both file and console logging capabilities.
    """

    def __init__(self, log_file="app.log"):
        """
        Initialize the logger with both file and console handlers.

        Args:
            log_file: Path to the log file (defaults to 'app.log')
        """
        # Get a logger instance using the module name
        self.logger = logging.getLogger(__name__)
        # Set the logging level to DEBUG to capture all log messages
        self.logger.setLevel(logging.DEBUG)

        # Create a file handler to write logs to the specified file
        file_handler = logging.FileHandler(log_file)

        # Create a console handler to display logs in the terminal
        console_handler = logging.StreamHandler()

        # Define the format for log messages (timestamp - level - message)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        # Apply the formatter to both handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add both handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, message):
        """Log a DEBUG level message."""
        self.logger.debug(message)

    def info(self, message):
        """Log an INFO level message."""
        self.logger.info(message)

    def warning(self, message):
        """Log a WARNING level message."""
        self.logger.warning(message)

    def error(self, message):
        """Log an ERROR level message."""
        self.logger.error(message)

    def critical(self, message):
        """Log a CRITICAL level message."""
        self.logger.critical(message)


class TVLogger(StreamHandler):
    """
    A custom StreamHandler that redirects log messages to a GUI text widget.
    Inherits from StreamHandler to handle log messages in a GUI context.
    """

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

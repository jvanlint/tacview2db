import argparse
import os
import time
import sys
import logging
from art import tprint
from colorama import Fore, Style
from services.tacview_engine import process_all_tacview_files
from views.tacview_gui_grid import TacviewGUIGrid
from models.database import Database

from config import DATABASE_NAME


def parse_command_line_args():
    parser = argparse.ArgumentParser(
        description="Process TacView XML into a SQLite3 database."
    )
    parser.add_argument(
        "files", action="store", nargs="*", help="The XML filename(s) to process."
    )
    parser.add_argument(
        "-c",
        "--cleardb",
        action="store_true",
        help="Clear the database before processing data file(s).",
    )
    # Add argument for verbose logging
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",  # Flag argument, will be True if specified
        help="Enable verbose logging to console.",
    )
    return parser.parse_args()


def setup_logging(verbose_logging):
    """
    Configure the logging system for the application

    Args:
        verbose_logging: Boolean flag to determine if logs should also be output to console

    This function sets up:
    1. File logging (always enabled, writes to app.log)
    2. Console logging (only when verbose_logging is True)
    """
    # Set up logging configuration with a file handler by default
    # Level DEBUG ensures all log messages are captured
    # The 'w' mode overwrites previous log files on each run
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler("app.log", mode="w"),
            # logging.StreamHandler(),  # Commented out to prevent duplicate logs
        ],
    )

    # Only add console logging if verbose flag was set
    if verbose_logging:
        # Create a handler for console output
        console = logging.StreamHandler()
        # Define the format for console messages
        formatter = logging.Formatter("%(asctime)s -  %(levelname)s - %(message)s")
        console.setFormatter(formatter)
        # Add the console handler to the root logger
        logging.getLogger("").addHandler(console)


def main(argv):
    """
    Main entry point for the application

    Args:
        argv: Command line arguments passed to the script

    Handles:
    1. Command-line argument parsing
    2. Logging setup
    3. Database initialization
    4. Choosing between CLI or GUI mode based on arguments
    """
    # Parse command-line arguments
    args = parse_command_line_args()

    # Configure the logging based on verbose flag
    setup_logging(args.verbose)

    # Set up database path relative to script location
    # This ensures database is properly located regardless of where script is called from
    current_dir = os.path.dirname(os.path.abspath(__file__))
    database_file = DATABASE_NAME  # Imported from config module
    database_path = os.path.join(current_dir, database_file)

    # Create a database connection
    db = Database(database_path)

    # Set start time of processing to calculate total time taken.
    start = time.perf_counter()

    # This code is for determining if the user wants to launch UI or command line.
    # Providing no arguments assumes the UI is required.
    if args.files:
        tprint("tacview2db", font="tarty1")
        # Files provided through command-line arguments
        stats = process_all_tacview_files(db, args.cleardb, args.files)
        end = time.perf_counter()

        print("-" * 80)
        print(f"{Fore.GREEN}*** Export to database complete! ***")
        print(
            f"Processed {Fore.YELLOW}{stats[0]}{Fore.GREEN} of {Fore.YELLOW}{stats[1]}{Fore.GREEN} files in {Fore.YELLOW}{end - start:.3f}{Fore.GREEN} seconds.{Style.RESET_ALL} "
        )
        print(
            f"{Fore.MAGENTA}Please refer to app.log file for more detailed information.{Style.RESET_ALL}"
        )
    else:
        # No files provided, run the UI
        gui = TacviewGUIGrid(db)
        gui.run()

    db.close_connection


if __name__ == "__main__":
    main(sys.argv[1:])

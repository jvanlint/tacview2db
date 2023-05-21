import argparse, os, time, sys, logging
from dotenv import load_dotenv
from colorama import Fore, Back, Style
from tacview_engine import process_all_tacview_files
from ui.tacview_gui import TacviewGUI


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
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging to console.",
    )
    return parser.parse_args()


def setup_logging(verbose_logging):
    # Set up logging configuration
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler("app.log", mode="w"),
            # logging.StreamHandler(),
        ],
    )

    if verbose_logging:
        console = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s -  %(levelname)s - %(message)s")
        console.setFormatter(formatter)
        logging.getLogger("").addHandler(console)


def main(argv):
    # Parse command-line arguments.
    args = parse_command_line_args()

    # Set up logging
    setup_logging(args.verbose)

    # Read environment variables
    load_dotenv()
    database_file = os.getenv("DATABASE_NAME")

    # Set start time of processing to calculate total time taken.
    start = time.time()

    # This code is for determining UI or command line
    if args.files:
        # Files provided through command-line arguments
        process_all_tacview_files(database_file, args.cleardb, args.files)

        print("-" * 80)
        print(f"{Fore.GREEN}*** Export to database complete! ***{Style.RESET_ALL}")
        print(f"The script took {time.time() - start:.3f} seconds to finish.")
        print(
            f"{Fore.MAGENTA}Please refer to app.log file for more detailed information.{Style.RESET_ALL}"
        )
    else:
        # No files provided, run the UI
        gui = TacviewGUI()
        gui.run()


if __name__ == "__main__":
    main(sys.argv[1:])

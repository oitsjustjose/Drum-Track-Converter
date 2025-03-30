import sys
from argparse import ArgumentParser, RawTextHelpFormatter

from colorama import Fore

from src.messaging import CliOutput
from src.music_file import MODEL_CHOICES
from src.processor import FolderProcessor


def __get_parser() -> ArgumentParser:
    """Creates an arg parser for the program. Abstracted away because it's ugly like always

    Returns:
        ArgumentParser: The created and configured arg parser.
    """

    model_choices = "\n  • ".join(
        # Padding in the array so the first entry starts on a newline with bullet
        [""]
        + [
            f"{Fore.GREEN}{MODEL_CHOICES[desc]}{Fore.RESET} - {desc}"
            for desc in MODEL_CHOICES
        ]
    )

    parser = ArgumentParser(
        prog="Drum Track Converter",
        description="Removes the drum tracks from [almost] any song using Demucs",
        formatter_class=RawTextHelpFormatter,
    )

    parser.add_argument(
        "input_dir", help="The directory to scan for files. Scans recursively."
    )

    parser.add_argument(
        "output_dir",
        help="The directory to output drumless tracks to. Folder structure is preserved from the input.",
    )

    parser.add_argument(
        "-m",
        "--model",
        help=f"What model to use. Options include: {model_choices}",
        default=list(MODEL_CHOICES.values())[0],
    )

    parser.add_argument(
        "-v",
        "--verbose",
        help="Show verbose print statements",
        action="store_true",
        default=False,
    )

    return parser


if __name__ == "__main__":
    logger = CliOutput()
    args = __get_parser().parse_args()

    try:
        processor = FolderProcessor.from_args(args, logger)
        processor.process_directory()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.error(e)

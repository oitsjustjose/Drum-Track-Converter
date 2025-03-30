import sys

from src.messaging import CliOutput
from src.processor import FolderProcessor
from src.music_file import MODEL_CHOICES

if __name__ == "__main__":
    output = CliOutput()

    if len(sys.argv) >= 3:
        ## TODO: CLI argparse -- this is getting messy...
        model_name = (
            sys.argv[3] if len(sys.argv) >= 4 else list(MODEL_CHOICES.values())[0]
        )

        processor = FolderProcessor(
            sys.argv[1],
            sys.argv[2],
            output,
        )
        processor.process_directory()
    else:
        warning_str = [
            "The CLI utility requires exactly two parameters:",
            " • input [str] -- The directory to scan through",
            " • output [str] -- The directory to output through, keeping the input directory's file structure.",
            "  (This directory will be made if necessary)",
        ]
        output.error("\n".join(warning_str))

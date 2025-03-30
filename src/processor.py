import os
import shutil
import subprocess
from pathlib import Path
from argparse import Namespace as argset

import eyed3
from eyed3.id3 import ID3_V2_4, Tag

from src.messaging import MessageInterface, NoPrintStatements
from src.music_file import SUPPORTED_EXTS, MODEL_CHOICES, MusicFile


class FolderProcessor:
    def __init__(
        self,
        input_dir: str,
        output_dir: str,
        model_name: str,
        msg_interface: MessageInterface,
        verbose: bool = False,
    ):
        """
        Args:
            input_dir (str): The source directory to traverse and convert
            output_dir (str): The destination directory which will mirror the source, but with tracks that have no drums
            model_name (str): The name of the Demucs model to use for splitting tracks
            msg_interface (MessageInterface): The handler for displaying output to the user
        """
        self.input_dir: str = input_dir
        self.output_dir: str = output_dir
        self.msg_interface: MessageInterface = msg_interface
        self.model_name = model_name
        self.verbose: bool = verbose

    @classmethod
    def from_args(self, args: argset, msg_interface: MessageInterface):
        """Creates a FolderProcessor instance using an argparse argument set

        Args:
            args (argset): Arguments from the CLI
            msg_interface (MessageInterface): The handler for displaying output to the user
        """
        return FolderProcessor(
            args.input_dir, args.output_dir, args.model, msg_interface, args.verbose
        )

    def _is_ffmpeg_present(self) -> bool:
        """Determines if ffmpeg is installed and accessible

        Returns:
            bool: True if ffmpeg is installed and accessible, false otherwise.
                When returning false, no processing should be permitted.
        """
        try:
            exit_code = subprocess.call(
                ["ffmpeg"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            return exit_code == 1
        except FileNotFoundError:
            return False

    def process_directory(self) -> None:
        """
        Traverses all files in the provided source directory, replicating the directory format in \
            the destination directory and moving the converted file to match suit.
        
        Also ensures that metadata is copied from the old file to the new one to provide the best user experience in the end
        """

        if not self._is_ffmpeg_present():
            raise Exception(
                "FFMpeg is not installed! Please install it from here: https://www.ffmpeg.org/download.html"
            )

        src: Path = Path(self.input_dir)
        dest: Path = Path(self.output_dir)
        cur_dir: Path = Path(".").resolve()  # Used just for logging

        if not src.exists():
            raise Exception("Input directory does not exist!")

        for root, _, files in os.walk(src):
            for file in files:
                original_path = Path(root).joinpath(file)
                if original_path.suffix not in SUPPORTED_EXTS:
                    self.msg_interface.warning(
                        f"File {original_path.name} has an unsupported extension and will be skipped!"
                    )
                    continue
                # Create a "MusicFile" from the full path of the original file
                original_file = MusicFile(original_path, self.model_name)

                self.msg_interface.info(
                    f"Splitting drum tracks from {original_path.name} using {list(MODEL_CHOICES.keys())[list(MODEL_CHOICES.values()).index(self.model_name)]}:"
                )

                with NoPrintStatements(self.verbose):
                    no_drums_path = original_file.separate()

                # If metadata cloning fails, skip the file.
                if not self.__copy_metadata(original_file, no_drums_path):
                    continue

                # Replace the input destination with the output destination
                file_output_root = root.replace(str(src), str(dest))
                file_output_root = Path(file_output_root).resolve()
                # We also need to replace the original {file} extension with .mp3
                filename_with_mp3_ext = f"{Path(file).stem}.mp3"
                file_dest = file_output_root.joinpath(filename_with_mp3_ext)
                # Make the output subdir(s) and move the no-drums file from the temp output to the final destination
                os.makedirs(file_output_root, exist_ok=True)
                shutil.move(no_drums_path, file_dest)

                self.msg_interface.info(
                    f"Done processing {original_path.name} and relocated it to {file_dest.relative_to(cur_dir)}!"
                )

        # Remove the model output since we don't need it anymore
        if os.path.exists(self.model_name):
            shutil.rmtree(self.model_name)

    def __copy_metadata(self, original_file: MusicFile, no_drums_path: Path) -> bool:
        """
        Copies the metadata from the original music file to the new drumless track

        Args:
            original_file (MusicFile): The MusicFile instance for the original, unmodified/unsplit son
            no_drums_path (Path): The path to the drumless output file after splitting

        Returns:
            bool: True if the process succeeds, False if get_tag raises an exception
        """
        try:
            self.msg_interface.info(
                f"Copying Metadata from {original_file.file_path.name} to {no_drums_path.name}"
            )

            original_tag: Tag = original_file.get_tag()

            no_drums_audiofile = eyed3.load(str(no_drums_path))
            no_drums_audiofile.tag = original_tag
            no_drums_audiofile.tag.title = f"{original_tag.title} (No Drums)"
            no_drums_audiofile.tag.save(version=ID3_V2_4)
        except Exception:
            self.msg_interface.warning(
                f"Failed to get the tag for {no_drums_path.name} - skipping!"
            )
            no_drums_path.unlink()
            return False
        return True

import os
import shutil
from pathlib import Path

import eyed3
from eyed3.id3 import ID3_V2_4, Tag

from src.music_file import MODEL_NAME, SUPPORTED_EXTS, MusicFile
from src.messaging import MessageInterface, NoPrintStatements


class FolderProcessor:
    def __init__(
        self, input_dir: str, output_dir: str, msg_interface: MessageInterface
    ):
        """_summary_

        Args:
            input_dir (str): The source directory to traverse and convert
            output_dir (str): The destination directory which will mirror the source, but with tracks that have no drums
            msg_interface (MessageInterface): The handler for displaying output to the user
        """
        self.input_dir: str = input_dir
        self.output_dir: str = output_dir
        self.msg_interface: MessageInterface = msg_interface
        self.should_stop = False

    def quit(self) -> None:
        """Tells the ongoing process to quit on next iteration"""
        self.should_stop = True

    def process_directory(self) -> None:
        """
        Traverses all files in the provided source directory, replicating the directory format in \
            the destination directory and moving the converted file to match suit.
        
        Also ensures that metadata is copied from the old file to the new one to provide the best user experience in the end
        """

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
                original_file = MusicFile(original_path)

                self.msg_interface.info(
                    f"Splitting drum tracks from {original_path.name}:"
                )

                # Get the output file of drumless music
                with NoPrintStatements():  # Prevent print statements from demucs
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

                if self.should_stop:
                    break
            if self.should_stop:
                break

        # Remove the model output since we don't need it anymore
        if os.path.exists(MODEL_NAME):
            shutil.rmtree(MODEL_NAME)

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

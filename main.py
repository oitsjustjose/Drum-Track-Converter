import os
import shutil
import sys
from pathlib import Path

import eyed3
from eyed3.id3 import ID3_V2_4, Tag

from music_file import MusicFile, MODEL_NAME

SUPPORTED_EXTS = [".mp3", ".m4a", ".wav"]


def copy_metadata(original_file: MusicFile, no_drums_path: Path) -> bool:
    """
    Copies the metadata from the original music file to the new drumless track

    Args:
        original_file (MusicFile): The MusicFile instance for the original, unmodified/unsplit son
        no_drums_path (Path): The path to the drumless output file after splitting

    Returns:
        bool: True if the process succeeds, False if get_tag raises an exception
    """
    try:
        original_tag: Tag = original_file.get_tag()

        no_drums_audiofile = eyed3.load(str(no_drums_path))
        no_drums_audiofile.tag = original_tag
        no_drums_audiofile.tag.title = f"{original_tag.title} (No Drums)"
        no_drums_audiofile.tag.save(version=ID3_V2_4)
    except Exception:
        print(f"Failed to get the tag for {no_drums_path} - skipping!")
        no_drums_path.unlink()
        return False
    return True


def main(src_in: str, dest_in: str) -> None:
    """
    Traverses all files in the provided source directory, replicating the directory format in \
        the destination directory and moving the converted file to match suit.
    
    Also ensures that metadata is copied from the old file to the new one to provide the best user experience in the end

    Args:
        src_in (str): The source directory to traverse and convert
        dest_in (str): The destination directory which will mirror the source, but with tracks that have no drums
    """

    src: Path = Path(src_in)
    dest: Path = Path(dest_in)

    if not src.exists():
        raise Exception("Input directory does not exist!")

    for root, _, files in os.walk(src):
        for file in files:
            original_path = Path(root).joinpath(file)
            if original_path.suffix not in SUPPORTED_EXTS:
                print(f"File {file} has an unsupported extension.")
                continue
            # Create a "MusicFile" from the full path of the original file
            original_file = MusicFile(original_path)
            # Gets the output file of drumless music
            no_drums_path = original_file.separate()
            # If metadata cloning fails, skip the file.
            if not copy_metadata(original_file, no_drums_path):
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

    # Remove the model output since we don't need it anymore
    if os.path.exists(MODEL_NAME):
        shutil.rmtree(MODEL_NAME)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])

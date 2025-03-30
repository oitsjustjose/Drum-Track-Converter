"""
@author: Jose Stovall | github.com/oitsjustjose | bsky||@oitsjustjose.com
"""

import os
from pathlib import Path

import eyed3
from demucs.separate import main as Separate
from eyed3.id3 import ID3_V2_4, Tag
from tinytag import TinyTag
from wavinfo import WavInfoReader

SUPPORTED_EXTS = [".mp3", ".m4a", ".wav"]
MODEL_CHOICES = {
    "Hybrid Transformer Demucs (Fine-Tuned)": "htdemucs_ft",
    "Hybrid Transformer Demucs": "htdemucs",
    "Hybrid Transformer Demucs v3": "hdemucs_mmi",
    "Model Trained with MusDB HQ": "mdx",
    "Model Trained with MusDB HQ & Extra Training Data": "mdx_extra",
    "Model Trained with MusDB HQ (Quantized)": "mdx_q",
    "Model Trained with MusDB HQ (Extra Quantized)": "mdx_extra_q",
}


class MusicFile:
    def __init__(self, path: Path, model_name: str):
        """A music file wrapper for most containers

        Args:
            path (Path): The path of the music file
        """
        self.file_path = path
        self.model_name = model_name

    def separate(self) -> Path:
        """_summary_

        Returns:
            Path: _description_
        """
        Separate(
            [
                "--mp3",  # Saves the output file to MP3 format
                "--two-stems",  # Defines two stems, {stem}.mp3 and no_{stem}.mp3
                "drums",  # {stem} as declared above
                "--jobs",  # Multitasking where possible
                f"{os.cpu_count() or 2}",  # Try to get it dynamically, fall back to 2
                "--out",  # Sets the subfolder to save stems to ({ModelName}/{--out}/{stem}.mp3)
                "",  # Fix it to empty string for easier automation
                "--filename",  # Set the file format for easier automation
                "{stem}.{ext}",  # Again, easier to automate "drums.mp3" than others..
                "--name",  # Model Name -- including this prevents output spam and removes unpredictability
                self.model_name,
                f"{str(self.file_path.resolve())}",
            ]
        )

        just_drums = Path(self.model_name).joinpath("drums.mp3")
        no_drums = Path(self.model_name).joinpath("no_drums.mp3")

        if os.path.exists(just_drums):
            os.unlink(just_drums)

        return no_drums.resolve()

    def get_tag(self) -> Tag:
        """Attempts to get the ID3 V2.4 Tag from the music file

        Raises:
            Exception: Thrown if the container for the file is not supported

        Returns:
            Tag: The ID3 V2.4 metadata tag from the music file contained
        """
        if self.file_path.suffix == ".mp3":
            return self.__get_mp3_tag()
        if self.file_path.suffix == ".m4a":
            return self.__get_m4a_tag()
        if self.file_path.suffix == ".wav":
            return self.__get_wav_tag()
        raise Exception(f"Failed to determine tag type for {self.file_path}")

    def __get_m4a_tag(self) -> Tag:
        """
        Creates a new eyed3 Tag object from an m4a tag which is not natively supported
        This implementation is based off of TinyTag's m4a support
        """
        tag = TinyTag.get(str(self.file_path))

        ret = Tag(version=ID3_V2_4)

        disc: int = int(tag.disc or 0)
        disc_total: int = int(tag.disc_total or 0)
        track: int = int(tag.track or 0)
        track_total: int = int(tag.track_total or 0)

        ret.album = tag.album
        ret.album_artist = tag.albumartist
        ret.artist = tag.artist
        ret.composer = tag.composer
        ret.disc_num = (disc, disc_total)
        ret.genre = tag.genre
        ret.title = tag.title
        ret.track_num = (track, track_total)
        ret.release_date = tag.year

        return ret

    def __get_wav_tag(self) -> Tag:
        """Gets the tag for a wav file based off of WavInfo's impl"""
        tag = WavInfoReader(str(self.file_path))

        ret = Tag(version=ID3_V2_4)
        ret.album = tag.info.album
        ret.album_artist = tag.info.artist
        ret.artist = tag.info.artist
        ret.genre = tag.info.genre
        ret.title = tag.info.title
        ret.release_date = tag.info.created_date

        return ret

    def __get_mp3_tag(self) -> Tag:
        """
        Gets or creates a tag from the given file path. If the tag fails to be created,
            an empty tag is made and returned
        """
        audio_file = eyed3.load(str(self.file_path))
        if not audio_file:
            print(
                f"Failed to load tag from file {self.file_path} -- returning empty tag"
            )
            return Tag(version=ID3_V2_4)
        return audio_file.tag

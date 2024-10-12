import eyed3
import sys
from pathlib import Path
import shutil
from eyed3.id3 import ID3_V2_4


def main(original_dir_path: str):
    """No u"""
    resolved_root = Path(original_dir_path).resolve()

    for filename in resolved_root.iterdir():
        orig_path = resolved_root.joinpath(filename)
        without_drums_path = (
            Path("./separated/htdemucs")
            .resolve()
            .joinpath(orig_path.stem)
            .joinpath("no_drums.mp3")
        )
        just_drums_path = (
            Path("./separated/htdemucs")
            .resolve()
            .joinpath(orig_path.stem)
            .joinpath("drums.mp3")
        )

        orig_afile = eyed3.load(str(orig_path))

        # Copy over the metadata from the original song to the one without drums
        without_drums_afile = eyed3.load(str(without_drums_path))
        without_drums_afile.tag = orig_afile.tag
        without_drums_afile.tag.title = f"{orig_afile.tag.title} (No Drums)"
        without_drums_afile.tag.save(version=ID3_V2_4)

        # Reload the original audio file to make sure we revert any changes to the tag
        del orig_afile
        orig_afile = eyed3.load(str(orig_path))

        # Same for the one that's _JUST_ drums
        just_drums_afile = eyed3.load(str(just_drums_path))
        just_drums_afile.tag = orig_afile.tag
        just_drums_afile.tag.title = f"{orig_afile.tag.title} (Just Drums)"
        just_drums_afile.tag.save(version=ID3_V2_4)

        # Now we want to move the files to a version

        shutil.move(
            without_drums_path,
            without_drums_path.joinpath("..")
            .joinpath(f"{without_drums_afile.tag.title}.mp3")
            .resolve(),
        )
        shutil.move(
            just_drums_path,
            just_drums_path.joinpath("..")
            .joinpath(f"{just_drums_afile.tag.title}.mp3")
            .resolve(),
        )


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])

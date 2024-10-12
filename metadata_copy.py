import eyed3
import sys
from pathlib import Path
import shutil
from eyed3.id3 import ID3_V2_4
from eyed3.id3 import Tag
from tinytag import TinyTag

def get_m4a_tag(orig_path: Path) -> Tag:
    """
    Creates a new eyed3 Tag object from an m4a tag which is not natively supported
    This implementation is based off of TinyTag's m4a support
    """
    tag = TinyTag.get(orig_path)
    
    ret = Tag(version=ID3_V2_4)

    ret.album =  tag.album
    ret.album_artist = tag.albumartist
    ret.artist = tag.artist
    ret.composer = tag.composer
    ret.disc_num = (int(tag.disc), int(tag.disc_total)) 
    ret.genre = tag.genre
    ret.title = tag.title
    ret.track_num = (int(tag.track), int(tag.track_total))
    ret.release_date = tag.year
    
    return ret
    

def main(root: str):
    """
    Iterates over all files in 'root' and copies the ID3 tags from the original
        files to the new files now that the drum parts have been split so that
        the metadata propagates correctly in foobar/iTunes/iPods everywhere
    Meant to be run **AFTER** running 'run_folder.sh' and
        is intended to be used with the same argument as that script.
    """
    resolved_root = Path(root).resolve()

    for filename in resolved_root.iterdir():
        orig_path = resolved_root.joinpath(filename)
        if not orig_path.exists():
            print(f"No orig_path {orig_path} exists, skipping")
            continue

        without_drums_path = (
            Path("./separated/htdemucs")
            .resolve()
            .joinpath(orig_path.stem)
            .joinpath("no_drums.mp3")
        )

        if not without_drums_path.exists():
            print(f"No without_drums_path {without_drums_path} exists, skipping")
            continue

        just_drums_path = (
            Path("./separated/htdemucs")
            .resolve()
            .joinpath(orig_path.stem)
            .joinpath("drums.mp3")
        )

        if not just_drums_path.exists():
            print(f"No just_drums_path {just_drums_path} exists, skipping")
            continue

        # orig_afile = eyed3.load(str(orig_path))
        original_tag: Tag = eyed3.load(str(orig_path)).tag if not orig_path.suffix.endswith('m4a') else get_m4a_tag(orig_path)

        # Copy over the metadata from the original song to the one without drums
        without_drums_afile = eyed3.load(str(without_drums_path))
        without_drums_afile.tag = original_tag
        without_drums_afile.tag.title = f"{original_tag.title} (No Drums)"
        without_drums_afile.tag.save(version=ID3_V2_4)

        # Reload the original audio file to make sure we revert any changes to the tag
        original_tag: Tag = eyed3.load(str(orig_path)).tag if not orig_path.suffix.endswith('m4a') else get_m4a_tag(orig_path)

        # Same for the one that's _JUST_ drums
        just_drums_afile = eyed3.load(str(just_drums_path))
        just_drums_afile.tag = original_tag
        just_drums_afile.tag.title = f"{original_tag.title} (Just Drums)"
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

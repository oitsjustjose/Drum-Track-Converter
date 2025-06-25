from pathlib import Path
from typing import List
from uuid import uuid4
from os import makedirs

import streamlit as st

from common import SUPPORTED_EXTS, MODEL_CHOICES
from music_file import MusicFile
from dataclasses import dataclass


@dataclass
class ConvertedFile:
    name: str
    path: Path


st.set_page_config(page_title="Drum Track Converter", page_icon="🥁", layout="centered")

st.header("Drum Track Converter")
st.subheader("Take any audio file and strip the drums out of it for drum practice!")

model_name = st.selectbox("DEMUCS Model", MODEL_CHOICES)
files = st.file_uploader(
    type=SUPPORTED_EXTS,
    accept_multiple_files=True,
    label="Select your music files you'd like to convert",
)

converted_files: List[ConvertedFile] = []

if files:
    job_id = str(uuid4())
    prog = st.progress(value=0, text="Working on it..")
    for idx, file in enumerate(files):
        makedirs(f"./.tmp/{job_id}")
        file_name = Path(f"./.tmp/{job_id}/{file.name}").resolve()
        with open(file_name, "wb") as fh:
            fh.write(file.read())

        music_file = MusicFile(file_name, MODEL_CHOICES[model_name])
        converted_files.append(ConvertedFile(name=file.name, path=music_file.separate()))
        prog.progress(idx + 1)

    prog.empty()

    for conv in converted_files:
        st.download_button(conv.name, conv.path.read_bytes())

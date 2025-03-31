# oitsjustjose's Drum Track Converter

This is a tool that utilizes Facebook's [`demucs`](https://github.com/facebookresearch/demucs) library to separate the drum track from an entire song!

I'm not entirely sure if this application _requires_ an Nvidia GPU or not, I actually have no way to test... my only machines all have Nvidia GPUs of some variety, so I have no way to test. Dropping an issue would be appreciated if you find out one way or another!

# ⚠️ FFmpeg Is Required! ⚠️

As `demucs` has a dependency on FFmpeg, so does this project. Installation is easy and lightweight. You can install FFMpeg for your operating system of choice from the [official site](https://ffmpeg.org/download.html).

# ℹ️ Using Your Nvidia GPU ℹ️

If you wish to use your Nvidia GPU, be sure to install the Cuda Toolkit version 11.8 from [here](https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_522.06_windows.exe) before proceeding.

## ℹ️ Additional Features

### 💽 Metadata Replication

As I intended to load the drumless tracks to my iPod Classic to drum along to, I realized it would be critical to ensure that the metadata from the original file be preserved. To do this I use a variety of tools to attempt to grab as much of the original metadata as possible and apply it to the new, drumless MP3 output.

This should mean that Album Art, Artists, Albums, Track Names, etc.. should continue to work as expected. To avoid confusion, the resulting file name and Track Name in the metadata has the string ` (No Drums)` appended to the end so you'll always know without having to listen to the song and find out.

### 📁 Preserved Folder Structure

I intended to use this with my existing, well-organized music library. To make it easy to keep my organization entact, the output directory's structure will match the input directory's structure! This means that any subfolders and their names will be preserved from input to output.

### 🎶 Support for multiple audio formats

Metadata handling required manual support for a variety of different audio wrappers, so currently `.mp3`, `.m4a` and `.wav` are the only supported file formats. Additional file formats can be added in the future upon request, but I haven't had a need so far..

### 🪟 Applications for Windows (and macOS soon?)

Using [PyQT6](https://pypi.org/project/PyQt6/) and [Nuitka](https://nuitka.net/), a native Windows binary with a GUI has been created for ease of use! This offers the same logging output as the CLI approach but is considerably more user-friendly.

macOS support may come soon - I don't daily drive macOS so it may pose additional problems going forward. For now I recommend the CLI approach listed below.

#### ‼️ Please Note ‼️

Windows Defender or Smartscreen may flag the executable as malware. This is because the executable is not signed, as getting it signed by Microsoft is a considerable expense and time-sink. I have no plans of getting this code signed at any point, but the entire project is FOSS so feel free to explore to your heart's delight.

### ⌨️ CLI for all operating systems

For those using the CLI, the installation and usage is:

```powershell
# Installation
pip install -r requirements.txt
# Usage
python -m src.cli {input_path} {output_path}
```

Additional per-file processing progress is also available through this method if you so desire.

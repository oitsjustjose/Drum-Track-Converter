#!/bin/bash

SOURCE_PATH="$(realpath $1)" 
echo "Working through files in $SOURCE_PATH"

for filename in "$SOURCE_PATH"/*; do
    sudo python3 -m demucs --mp3 --two-stems=drums "$filename";
done

sudo chown "$USER" -R ./separated 

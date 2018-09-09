# albumSplitter
Python script to split albums stored in singles files with corresponding cueFile.

## Dependencies
To use albumSplitter.py, you need pydub:

    pip install pydub

and deflacue:

    pip install deflacue

You'll also need ffmpeg:

    apt-get install ffmpeg

And flac:

    apt-get install flac

## Quickstart
To use albumSplitter.py, simply call it following this example:

    albumSplitter.py input.flac input.cue outDir albumCover.jpg

The script will automatically read the info stored in the .cue file, split the album with one file for each song, apply tags (only 'artist', 'album', 'year', 'title' and 'track' are applied) and add cover to song files.

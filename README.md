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
# Donate
This project is given for free ! If you want me to get some draft beers on you, help yourself and donate some coins:
btc: 1GYpPSEykq7NJ2UL3LhPCCV98CRW6DpKZD
eth: 0xd1024c3f422EbBbCf1a71A662a78471b4cB9dbCc
xmr: 43G1L2SEuzrUL4fDVVCxydPUeH167YE4A5F3u7rzuLf6T6vi1uoijmUN1XVA3ympPPj1XD3Nnm1nHJs34iBSd4NeFf9omJm
stak: SRksUon6nsJRuM3FaUbR9HRfSUAnrFDeJ5

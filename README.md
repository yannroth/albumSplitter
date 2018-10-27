# albumSplitter
Python script to split albums stored in singles files with corresponding cueFile.

## Dependencies
To use albumSplitter.py, you need pydub:

    pip3 install pydub

and deflacue:

    pip3 install deflacue

You'll also need ffmpeg:

    apt-get install ffmpeg

And flac:

    apt-get install flac

## Quickstart
To use albumSplitter.py, simply call it following this example:

    albumSplitter.py input.flac input.cue -d outDir -c albumCover.jpg -f flac -s '%track% - %title%'

The script will automatically read the info stored in the .cue file, split the album with one file for each song, apply tags (only 'artist', 'album', 'year', 'title', 'track' and 'genre' are applied) and add cover to song files.

Here is the full help message with parameters description:
```
positional arguments:
  album                 Input audio file of the album to split
  cue                   Input cue sheet defining tracks of album

optional arguments:
  -h, --help            show this help message and exit
  -d DEST, --dest DEST  Destination directory where track files will be
                        written. Default: current directory
  -c COVER, --cover COVER
                        Cover image file
  -f FORMAT, --format FORMAT
                        Output audio format, can be whatever ffmpeg is
                        compatible with: http://www.ffmpeg.org/general.html
                        #Audio-Codecs. Default: flac
  -s STRING, --string STRING
                        Formatting string for the output. Supported items are:
                        %artist%, %year%, %album%, %track%, %title% and
                        %genre%. Default: %artist%/%year% - %album%/%track% -
                        %title%
```
# Donate
This project is given for free ! If you want me to get some draft beers on you, help yourself and donate some coins:\
btc: 1GYpPSEykq7NJ2UL3LhPCCV98CRW6DpKZD\
eth: 0xd1024c3f422EbBbCf1a71A662a78471b4cB9dbCc\
xmr: 43G1L2SEuzrUL4fDVVCxydPUeH167YE4A5F3u7rzuLf6T6vi1uoijmUN1XVA3ympPPj1XD3Nnm1nHJs34iBSd4NeFf9omJm\
stak: SRksUon6nsJRuM3FaUbR9HRfSUAnrFDeJ5

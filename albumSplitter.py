#!/usr/bin/python

from pydub import AudioSegment as aud
from deflacue import deflacue as cue
import sys
import os
import subprocess
import argparse

version = "1.2.0"

def yes_or_no(question):
    while "the answer is invalid":
        reply = str(raw_input(question+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False

def existing_file(string):
    if not os.path.isfile(string):
        raise argparse.ArgumentTypeError(repr(string) + " not found.")
    return string

def create_dir(string):
    if os.path.exists(string) and not os.path.isdir(string):
        raise argparse.ArgumentTypeError(repr(string) + " exist but is not a directory.")
    if not os.path.exists(string):
        os.makedirs(string)
    return string

parser = argparse.ArgumentParser(description='Splits albums files described with a cue sheet')
parser.add_argument('album', type=existing_file, help='Input audio file of the album to split')
parser.add_argument('cue', type=existing_file, help='Input cue sheet defining tracks of album')
parser.add_argument('-d', '--dest', type=create_dir, default='.', help='Destination directory where track files will be written. Default: current directory')
parser.add_argument('-c', '--cover', type=str, help='Cover image file')
parser.add_argument('-f', '--format', type=str, default='flac', help='Output audio format, can be whatever ffmpeg is compatible with: http://www.ffmpeg.org/general.html#Audio-Codecs. Default: %(default)s')
parser.add_argument('-s', '--string', type=str, default='%artist%/%year% - %album%/%track% - %title%', help='Formatting string for the output. Supported items are: %%artist%%, %%year%%, %%album%%, %%track%%, %%title%% and %%genre%%. Default: %(default)s')
args = parser.parse_args()

# Load
print "Loading metadata..."
metadata = cue.CueParser(args.cue, encoding="iso-8859-1").get_data_tracks()
extension = os.path.splitext(args.album)[1][1:]

gArtist = metadata[0]['PERFORMER']
if not gArtist or not yes_or_no("Artist is: '" + gArtist + "', is it ok?"):
    gArtist = raw_input("Enter artist manually: ")

gYear = metadata[0]['DATE']
if not gYear or not yes_or_no("Year is: '" + gYear + "', is it ok?"):
    gYear = raw_input("Enter year manually: ")

gAlbum = metadata[0]['ALBUM']
if not gAlbum or not yes_or_no("Album is: '" + gAlbum + "', is it ok?"):
    gAlbum = raw_input("Enter album manually: ")

gGenre = metadata[0]['GENRE']
if not gGenre or not yes_or_no("Genre is: '" + gGenre + "', is it ok?"):
    gGenre = raw_input("Enter genre manually: ")

gArtist = gArtist.encode('utf-8')
gYear = gYear.encode('utf-8')
gAlbum = gAlbum.encode('utf-8')
gGenre = gGenre.encode('utf-8')

print gArtist + " - " + gGenre +" - " + gYear + " - " + gAlbum

print "Loading media file..."
toSplit = aud.from_file(args.album, extension)

print "Exporting songs..."
for song in metadata:
    startTime = song['POS_START_SAMPLES'] // (toSplit.frame_rate / 1000.)
    try:
        endTime = song['POS_END_SAMPLES'] // (toSplit.frame_rate / 1000.)
    except TypeError:
        endTime = None

    artist = gArtist
    year = gYear
    album = gAlbum
    genre = gGenre
    track = '%02d' % song['TRACK_NUM']
    title = song['TITLE'].encode('utf-8')

    #Parse format string to generate filename:
    filename = args.string
    filename = filename.replace('%artist%', artist)
    filename = filename.replace('%year%', year)
    filename = filename.replace('%album%', album)
    filename = filename.replace('%track%', track)
    filename = filename.replace('%title%', title)
    filename = filename.replace('%genre%', genre)
    filename = os.path.join(args.dest, filename + '.' + args.format.lower())

    fulldir = os.path.dirname(filename)
    if not os.path.isdir(fulldir):
        os.makedirs(fulldir)

    tmp = toSplit[startTime:endTime]
    sys.stdout.write(filename)
    sys.stdout.flush()
    try:
        tmp.export(filename,
                format=args.format,
                tags={'artist': artist, 'album_artist': artist, 'year': year, 'album': album, 'track': track, 'title': title, 'genre': genre})
        if args.cover != None:
            if subprocess.call(["metaflac", "--import-picture-from=" + args.cover, fileName]):
                raise BlockingIOError("Couldn't add cover")
        sys.stdout.write(" : DONE\n")
    except:
        sys.stdout.write(" : FAILED\n")
        sys.exit(1)

sys.exit(0)

#!/usr/bin/python

from pydub import AudioSegment as aud
from deflacue import deflacue as cue
import sys
import os
import subprocess
import argparse

version = "1.1.0"

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
parser.add_argument('-d', '--dest', type=create_dir, default='.', help='Destination directory where track files will be written')
parser.add_argument('-c', '--cover', type=str, help='Cover image file')
parser.add_argument('-f', '--format', type=str, default='flac', help='Output format, can be whatever ffmpeg is compatible with: http://www.ffmpeg.org/general.html#Audio-Codecs')
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

gArtist = gArtist.encode('utf-8')
gYear = gYear.encode('utf-8')
gAlbum = gAlbum.encode('utf-8')

print gArtist + " - " + gYear + " - " + gAlbum

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
    #artist = song['PERFORMER']
    #if artist != gArtist:

    year = gYear
    #year = song['DATE']
    album = gAlbum
    #album = song['ALBUM']
    track = '%02d' % song['TRACK_NUM']
    title = song['TITLE'].encode('utf-8')
    fileName = os.path.join(args.dest, track + " - " + title + "." + args.format.lower())
    tmp = toSplit[startTime:endTime]
    sys.stdout.write(fileName)
    sys.stdout.flush()
    try:
        tmp.export(fileName,
                format=args.format,
                tags={'artist': artist, 'album_artist': artist, 'year': year, 'album': album, 'track': track, 'title': title})
        if args.cover != None:
            if subprocess.call(["metaflac", "--import-picture-from=" + args.cover, fileName]):
                raise BlockingIOError("Couldn't add cover")
        sys.stdout.write(" : DONE\n")
    except:
        sys.stdout.write(" : FAILED\n")
        sys.exit(1)

sys.exit(0)

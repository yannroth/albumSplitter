#!/usr/bin/python3

from pydub import AudioSegment as aud
from deflacue import deflacue as cue
import sys
import os
import subprocess
import argparse

version = "1.3.0"

def yes_or_no(question):
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
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

def slugify(string):
    ilegals = [':', '"', '/', '\\', '|']
    ilegalsInv = ['<', '>', '?', '*']
    for i in ilegals:
        string = string.replace(i, '-')
    for i in ilegalsInv:
        string = string.replace(i, '')
    return string

parser = argparse.ArgumentParser(description='Splits albums files described with a cue sheet')
parser.add_argument('album', type=existing_file, help='Input audio file of the album to split')
parser.add_argument('cue', type=existing_file, help='Input cue sheet defining tracks of album')
parser.add_argument('-d', '--dest', type=create_dir, default='.', help='Destination directory where track files will be written. Default: current directory')
parser.add_argument('-c', '--cover', type=str, help='Cover image file')
parser.add_argument('-f', '--format', type=str, default='flac', help='Output audio format, can be whatever ffmpeg is compatible with: http://www.ffmpeg.org/general.html#Audio-Codecs. Default: %(default)s')
parser.add_argument('-s', '--string', type=str, default='%artist%/%year% - %album%/%track% - %title%', help='Formatting string for the output. Supported items are: %%artist%%, %%year%%, %%album%%, %%track%%, %%title%% and %%genre%%. Default: %(default)s')
parser.add_argument('-v', '--version', action='store_true', default=False, help='Print version and quit')
parser.add_argument('-V', '--verbose', action='store_true', default=False, help ='Make it more verbose')
parser.add_argument('-bd', '--bitdepth', type=str, default='s16', help='Configure bitdepth of output files, accept ffmpeg bitdepth argument, use "ffmpeg -sample-fmts" to see available bit depths. Default: %(default)s')
parser.add_argument('-sr', '--samplerate', type=str, default='44100', help='Configure sample rate of outpute files. Default: %(default)s')
args = parser.parse_args()

if args.version:
    print (version)
    sys.exit(0)
# Load
print("Loading metadata...")
metadata = cue.CueParser(args.cue, encoding="utf-8").get_data_tracks()
extension = os.path.splitext(args.album)[1][1:]

gArtist = metadata[0]['PERFORMER']
if not gArtist or not yes_or_no("Artist is: '" + gArtist + "', is it ok?"):
    gArtist = input("Enter artist manually: ")

gYear = metadata[0]['DATE']
if not gYear or not yes_or_no("Year is: '" + gYear + "', is it ok?"):
    gYear = input("Enter year manually: ")

gAlbum = metadata[0]['ALBUM']
if not gAlbum or not yes_or_no("Album is: '" + gAlbum + "', is it ok?"):
    gAlbum = input("Enter album manually: ")

gGenre = metadata[0]['GENRE']
if not gGenre or not yes_or_no("Genre is: '" + gGenre + "', is it ok?"):
    gGenre = input("Enter genre manually: ")

gArtist = gArtist.encode('utf-8')
gYear = gYear.encode('utf-8')
gAlbum = gAlbum.encode('utf-8')
gGenre = gGenre.encode('utf-8')

gArtist = gArtist.decode('utf-8')
gYear = gYear.decode('utf-8')
gAlbum = gAlbum.decode('utf-8')
gGenre = gGenre.decode('utf-8')

print(gArtist + " - " + gGenre +" - " + gYear + " - " + gAlbum)

print("Loading media file...")
toSplit = aud.from_file(args.album, extension)

print("Exporting songs...")
for song in metadata:
    startTime = song['POS_START_SAMPLES'] // (44100 / 1000.) # Don't use actual sample rate of file because deflacue can't know it and uses 44100 to output samples
    try:
        endTime = song['POS_END_SAMPLES'] // (44100 / 1000.)
    except TypeError:
        endTime = None

    artist = gArtist
    year = gYear
    album = gAlbum
    genre = gGenre
    track = '%02d' % song['TRACK_NUM']
    title = song['TITLE'].encode('utf-8')
    title = title.decode('utf-8')

    #Parse format string to generate filename:
    filename = args.string
    filename = filename.replace('%artist%', slugify(artist))
    filename = filename.replace('%year%', slugify(year))
    filename = filename.replace('%album%', slugify(album))
    filename = filename.replace('%track%', slugify(track))
    filename = filename.replace('%title%', slugify(title))
    filename = filename.replace('%genre%', slugify(genre))
    filename = os.path.join(args.dest, filename + '.' + args.format.lower())

    fulldir = os.path.dirname(filename)
    if not os.path.isdir(fulldir):
        os.makedirs(fulldir)

    tmp = toSplit[startTime:endTime]
    sys.stdout.write(filename)
    if args.verbose:
        sys.stdout.write(' ' + str(startTime) + ' - ' + str(endTime))

    sys.stdout.flush()
    try:
        tmp.export(filename,
                format=args.format,
                parameters=['-sample_fmt', args.bitdepth, '-ar', args.samplerate],
                tags={'artist': artist, 'album_artist': artist, 'year': year, 'album': album, 'track': track, 'title': title, 'genre': genre})
        if args.cover != None:
            if subprocess.call(["metaflac", "--import-picture-from='" + args.cover + "'", fileName]):
                raise BlockingIOError("Couldn't add cover")
        sys.stdout.write(" : DONE\n")
    except:
        sys.stdout.write(" : FAILED\n")
        sys.exit(1)

sys.exit(0)

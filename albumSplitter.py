#!/usr/bin/python

from pydub import AudioSegment as aud
from deflacue import deflacue as cue
import sys
import os
import subprocess

def yes_or_no(question):
    while "the answer is invalid":
        reply = str(raw_input(question+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False


if (len(sys.argv) != 3) and (len(sys.argv) != 4) and (len(sys.argv) != 5):
    print("Wrong number of argument.")
    print("usage: sys.argv[0] audioFile cueFile [destination: currentFolder] [cover: None]")

inFile = sys.argv[1]
cueFile = sys.argv[2]

outFolder = "."
if len(sys.argv) >= 4:
    outFolder = sys.argv[3]

cover = None
if len(sys.argv) >= 5:
    cover = sys.argv[4]

if not os.path.exists(outFolder):
    os.makedirs(outFolder)

# Load
print "Loading metadata..."
metadata = cue.CueParser(cueFile, encoding="iso-8859-1").get_data_tracks()
extension = os.path.splitext(inFile)[1][1:]

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
toSplit = aud.from_file(inFile, extension)

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
    fileName = os.path.join(outFolder, track + " - " + title + "." + extension.lower())
    tmp = toSplit[startTime:endTime]
    sys.stdout.write(fileName)
    sys.stdout.flush()
    tmp.export(fileName, 
                format=extension, 
                tags={'artist': artist, 'album_artist': artist, 'year': year, 'album': album, 'track': track, 'title': title})
    error = 0
    if cover != None:
        error = subprocess.call(["metaflac", "--import-picture-from=" + cover, fileName])
    if error != 0:
        sys.stdout.write(" : Image upload failed\n")
    else:
        sys.stdout.write(" : DONE\n")

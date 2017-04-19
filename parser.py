import re, argparse
import sys
from matplotlib import pyplot
import plistlib
import numpy as np


def findDuplicates(fileName):
    print('Finding duplicate tracks in &s...' + fileName)
    plist = plistlib.readPlist(fileName)
    tracks = plist['Tracks']

    trackNames = {}

    for trackId, track in tracks.items():
        print(track)
        try:
            name = track['Name']

            duration = track['Total Time']
            if name in trackNames:
                if duration//1000 == trackNames[name][0]//1000:
                    count = trackNames[name][1]
                    trackNames[name] = (duration, count+1)
            else:
                trackNames[name] = (duration, 1)
        except:
            #ignore
            pass

def findCommonTracks(fileNames):
    trackNameSets = []
    for fileName in fileNames:
        trackNames = set()
        plist = plistlib.readPlist(fileName)
        tracks = plist['Tracks']
        for trackId, track in tracks.items():
            try:
                trackNames.add(track['Name'])
            except:
                #ignore
                pass
        trackNameSets.append(trackNames)
    commonTracks = set.intersection(*trackNameSets)
    if len(commonTracks) > 0:
        f = open("common.txt", "w")
        for val in commonTracks:
            s = "%s\n" % val
            f.write(str(s.encode("UTF-8")))
        f.close()
        print("%d common tracks found. "
              "Track names written to common.txt" %len(commonTracks))
    else:
        print("No common tracks!")

def plotStats(fileName):
    plist = plistlib.readPlist(fileName)
    tracks = plist['Tracks']
    ratings = []
    durations = []
    for trackId, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
        except:
            #ignore
            pass
    if ratings == [] or durations == []:
        print("No valid Album Rating/Total Time data in %s." % fileName)
        return
    x = np.array(durations, np.int32)
    x = x/60000.0
    y = np.array(ratings, np.int32)
    pyplot.subplot(2,1,1)
    pyplot.plot(x,y,'o')
    pyplot.axis([0,1.05*np.max(x), -1,110])
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Track rating')

    pyplot.subplot(2,1,2)
    pyplot.hist(x, bins=20)
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Count')

    pyplot.show()

def main():
    file = "D:\Python\playlistparser\mymusic.xml"
    descStr = """desc
    """
    parser = argparse.ArgumentParser(description=descStr)
    group = parser.add_mutually_exclusive_group()

    group.add_argument('--common', nargs='*', dest='plFiles', required=False)
    group.add_argument('--stats', dest='plFile', required=False)
    group.add_argument('--dup', dest='plFileD', required=False)

    args = parser.parse_args()

    if args.plFiles:
        findCommonTracks(args.plFiles)
    elif args.plFile:
        plotStats(args.plFile)
    elif args.plFileD:
        findDuplicates(args.plFileD)
    else:
        print("No tracks")


if __name__ == '__main__':
    main();
#!/home/ziriusph/anaconda3/bin/python
# -*- coding: utf-8 -*-

import argparse
import re
import codecs
import subprocess

PLAYLIST_FILE = "playlist.txt"
YOUTUBE_PLAYLIST_REGEX = re.compile("[&|\?]list=([a-zA-Z0-9_-]+)")
PLAYLIST_DOWNLOAD_DIR = "/var/www/html/downloads/pl"
YOUTUBE_DL_COMMAND = "youtube-dl --download-archive downloaded.txt --no-post-overwrites -c -i -o '%(playlist_uploader)s-%(playlist_title)s/%(upload_date)s-%(title)s--id=%(id)s.%(ext)s' --restrict-filenames -f 22/18"


def app():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add-playlist', type=unescaped_str, help='url(s) to download', nargs="+")
    parser.add_argument('-d', '--remove-playlist', type=unescaped_str, help='url(s) to remove from playlist', nargs="+")
    parser.add_argument('-s', '--start', action='store_true', help='start the download')
    args = vars(parser.parse_args())
    # print(args)

    if args["start"]:
        startDownload()
    elif args["add_playlist"]:
        addToPlaylist(args['add_playlist'])


def startDownload():
    if not _readPlaylist():
        print("Nothing to download.")
        return False

    shell_command_builder = ""
    shell_command_builder += 'cd "'+PLAYLIST_DOWNLOAD_DIR+'" && \n'
    for u in _readPlaylist():
        playlist_cmd = " "
        playlist_cmd += YOUTUBE_DL_COMMAND + " " + "\""+u+"\" && \n"
        shell_command_builder += playlist_cmd
    shell_command_builder = shell_command_builder[:-4]
    print(shell_command_builder)
    subprocess.run(shell_command_builder, shell=True, check=True)

def addToPlaylist(urls=[]):
    for url in urls:
        url = url.__str__()
        if _checkIfAlreadyInPlaylist(url) is None and _buildRealPlaylistUrl(url):
            _writeToPlaylist(_buildRealPlaylistUrl(url))


def _writeToPlaylist(string):
    with open(PLAYLIST_FILE, "a") as fp:
        fp.write(string+"\n")


def _readPlaylist():
    playlists = []
    with open(PLAYLIST_FILE) as fp:
        for line in fp:
            if line[0] != "#":
                playlists.append(line.strip().__str__())
    return playlists


def _checkIfAlreadyInPlaylist(url):
    in_the_playlist = None
    # print("- Checking if {} is already in the playlist".format(url))
    real_url = _buildRealPlaylistUrl(url)
    if real_url:
        if real_url in _readPlaylist():
            # print("\"{}\" is in the playlist.".format(real_url))
            in_the_playlist = True
        else:
            # print("\"{}\" is NOT in the playlist.".format(real_url))
            in_the_playlist = None
    else:
        print("Cannot determine Youtube Playlist URL for \"{}\".". format(url))
        in_the_playlist = False
    return in_the_playlist


def _getPlaylistUrl(url):
    if YOUTUBE_PLAYLIST_REGEX.search(url):
        return YOUTUBE_PLAYLIST_REGEX.search(url).groups()[0]
    else:
        return False


def _buildRealPlaylistUrl(url):
    if _getPlaylistUrl(url):
        return "https://www.youtube.com/playlist?list="+_getPlaylistUrl(url)
    else:
        return None


def unescaped_str(arg_str):
    return codecs.decode(str(arg_str), 'unicode_escape')


if __name__ == "__main__":
    app()


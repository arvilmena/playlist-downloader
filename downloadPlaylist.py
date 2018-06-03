import argparse

PLAYLIST_FILE = "playlist.txt"

def app():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
    parser.add_argument('--sum',
                        dest='accumulate',
                        action='store_const',
                        const=sum,
                        default=max,
                        help='sum the integers (default: find the max)'
                        )
def readTextFile():
    with open(PLAYLIST_FILE) as fp:
        for line in fp:
            print(line)

if __name__ == "__main__":
    app()
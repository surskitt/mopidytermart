#!/usr/bin/env python

import os
import sys
import time
import argparse

import ueberzug.lib.v0 as ueberzug
import mpd
import mopidyartfetch


def get_opts():
    parser = argparse.ArgumentParser(description='mopidy album art in console')

    parser.add_argument('--width', '-w', type=int, required=True)
    parser.add_argument('--timeout', '-t', type=int, default=30)
    parser.add_argument('--music-dir', '-m')
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', '-p', type=int, default=6600)

    return parser.parse_args()


def get_client(timeout, host, port):
    client = mpd.MPDClient()
    for t in range(timeout):
        try:
            client.connect(host, port)
            return client
        except (ConnectionRefusedError, mpd.base.ConnectionError):
            time.sleep(1)
            if t == timeout - 1:
                print('connection failed', file=sys.stderr)
                sys.exit(1)


def placement_gen(name, width):
    with ueberzug.Canvas() as c:
        placement = c.create_placement(name, x=0, y=0)

    placement.path = mopidyartfetch.get_fn('blank')
    placement.max_height = os.get_terminal_size().lines - 1
    placement.max_width = width
    placement.visibility = ueberzug.Visibility.VISIBLE

    return placement


def get_uri(song):
    for i in ['x-albumuri', 'file']:
        uri = song.get(i)
        if uri:
            return uri


def main():
    opts = get_opts()
    client = get_client(opts.timeout, opts.host, opts.port)
    placement = placement_gen('placement', opts.width)

    while True:
        song = client.currentsong()
        uri = get_uri(song)
        art_fn = mopidyartfetch.get_fn(uri, root=opts.music_dir)

        if not os.path.exists(art_fn):
            img = mopidyartfetch.get_image(uri, song.get('x-albumimage'))

            if img:
                try:
                    os.makedirs(os.path.dirname(art_fn))
                except FileExistsError:
                    pass
                with open(art_fn, 'wb') as f:
                    f.write(img)
            else:
                art_fn = mopidyartfetch.get_fn('blank')

        placement.path = art_fn

        try:
            client.idle('player')
        except mpd.base.ConnectionError:
            client = get_client(opts.timeout, opts.host, opts.port)


if __name__ == '__main__':
    main()

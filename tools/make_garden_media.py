"""Prepare the Garden Door footage for the web.

The four clips were generated with Higgsfield (Seedance 2.5, 720x1280, 24 fps, 5 s):
  open      door.png -> garden.png        the doors swing open, the camera glides in
  garden    garden.png -> garden.png      ambient loop
  walk      garden.png -> pavilion.png    dolly down the pool (played by the scroll)
  pavilion  pavilion.png -> pavilion.png  ambient loop

usage: python3 tools/make_garden_media.py RAW_DIR FFMPEG
RAW_DIR holds open_raw.mp4, garden_raw.mp4, walk_raw.mp4, pavilion_raw.mp4.
Writes garden/media/{open,garden,pavilion}.mp4, the matching posters (each video's own first
frame, so swapping a poster for its video never jumps) and garden/media/walk/001-060.jpg.
"""
import pathlib
import subprocess
import sys

RAW, FF = pathlib.Path(sys.argv[1]), sys.argv[2]
OUT = pathlib.Path(__file__).resolve().parent.parent / 'garden' / 'media'
WALK_FRAMES = 60


def ff(*args):
    subprocess.run([FF, '-hide_banner', '-loglevel', 'error', '-y', *args], check=True)


# Small H.264 files that start playing before they finish downloading (faststart), no sound track.
H264 = ['-c:v', 'libx264', '-preset', 'slow', '-profile:v', 'high', '-pix_fmt', 'yuv420p',
        '-movflags', '+faststart', '-an']
for name, crf in (('open', 25), ('garden', 27), ('pavilion', 27)):
    ff('-i', str(RAW / f'{name}_raw.mp4'), *H264, '-crf', str(crf), str(OUT / f'{name}.mp4'))

# Posters: the first frame of each video (the door is the opening film's first frame).
for poster, clip in (('door', 'open'), ('garden', 'garden'), ('pavilion', 'pavilion')):
    ff('-i', str(OUT / f'{clip}.mp4'), '-frames:v', '1', '-q:v', '3', str(OUT / f'{poster}.jpg'))

# The walk: evenly spaced frames, small enough to fetch quickly on a phone.
walk = OUT / 'walk'
walk.mkdir(exist_ok=True)
for f in walk.glob('*.jpg'):
    f.unlink()
ff('-i', str(RAW / 'walk_raw.mp4'), '-vf', f'fps={WALK_FRAMES}/5.04,scale=540:960:flags=lanczos',
   '-frames:v', str(WALK_FRAMES), '-q:v', '5', str(walk / '%03d.jpg'))

total = sum(f.stat().st_size for f in OUT.rglob('*') if f.is_file())
print(f'{len(list(walk.glob("*.jpg")))} walk frames; media total {total / 1e6:.1f} MB')
for f in sorted(OUT.glob('*')):
    if f.is_file():
        print(f'  {f.name}: {f.stat().st_size // 1024} KB')

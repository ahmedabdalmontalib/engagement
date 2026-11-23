# Making the invitation videos

Phone-size videos (1080 × 1920, 30 fps, with the invitation's music) of the invitation playing by itself.
Needs the preview server (`python3 tools/serve.py 8791`), Playwright with Chromium and `imageio-ffmpeg`.

```bash
python3 tools/video/record.py http://localhost:8791 ar rec_ar 2.5      # frames of the Arabic version
python3 tools/video/music_render.py rec_ar music_ar.wav                 # the melody, starting at the tap
```

Then join the frames (`rec_ar/list.txt`, made from `rec_ar/times.json`) and the music with ffmpeg:
`-f concat -i list.txt -i music.wav`, `fps=30`, full-to-TV colour range, `yuv420p`, H.264 CRF 21, AAC 160 kb/s,
`+faststart`, a 0.6 s fade in and a 1.4 s fade out. Use `en` for the English version.
The finished videos go in `video/` (kept out of Git).

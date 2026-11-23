"""Record the invitation playing by itself (opening + auto-scroll) as timestamped frames.
usage: record.py BASE lang OUTDIR scale
  scale 2.5 → 1080x1920 frames (viewport 432x768)"""
import base64
import json
import pathlib
import sys
import time
from playwright.sync_api import sync_playwright

base, lang, out, scale = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3]), float(sys.argv[4])
out.mkdir(parents=True, exist_ok=True)
for f in out.glob('*.jpg'):
    f.unlink()
# A clean picture for a video: no buttons, notes or the skip link.
CLEAN = """.topbar,.toast,.skip,.sound-pref,.intro-lang,.dots,.btn-row,.cal{display:none!important}"""
frames = []
with sync_playwright() as pw:
    # A real window at phone size and scale: the capture then has full phone resolution.
    b = pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required', '--mute-audio', f'--force-device-scale-factor={scale}', '--window-size=432,768'])
    ctx = b.new_context(no_viewport=True)
    p = ctx.new_page()
    p.goto(f'{base}/?lang={lang}&v=video', wait_until='load')
    p.add_style_tag(content=CLEAN)
    p.wait_for_function("() => !document.querySelector('#loader')", timeout=20000)
    p.wait_for_timeout(1500)
    cdp = ctx.new_cdp_session(p)
    t0 = None

    def on_frame(ev):
        global t0
        ts = ev['metadata']['timestamp']
        if t0 is None:
            t0 = ts
        n = len(frames)
        (out / f'{n:05d}.jpg').write_bytes(base64.b64decode(ev['data']))
        frames.append(ts - t0)
        cdp.send('Page.screencastFrameAck', {'sessionId': ev['sessionId']})
    cdp.on('Page.screencastFrame', on_frame)
    cdp.send('Page.startScreencast', {'format': 'jpeg', 'quality': 90, 'everyNthFrame': 1, 'maxWidth': round(432 * scale), 'maxHeight': round(768 * scale)})
    p.wait_for_timeout(2600)                                   # the opening screen
    tap_wall = time.time()
    p.locator('.begin-star').click(force=True)
    tap = frames[-1] if frames else 0.0
    # Wait until auto-scroll has reached the end, then hold on the closing scene.
    p.wait_for_function("() => document.body.classList.contains('formed')", timeout=30000)
    p.wait_for_timeout(9000)
    p.wait_for_function("() => !document.querySelector('.auto-btn').classList.contains('on') && scrollY >= document.documentElement.scrollHeight - innerHeight - 4", timeout=150000, polling=500)
    p.wait_for_timeout(5000)
    cdp.send('Page.stopScreencast')
    p.wait_for_timeout(300)
    b.close()
(out / 'times.json').write_text(json.dumps({'times': frames, 'tap': tap}))
dur = frames[-1]
print(f'{len(frames)} frames over {dur:.1f}s ({len(frames) / dur:.1f} fps); tap at {tap:.2f}s')

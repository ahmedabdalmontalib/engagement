"""Pack the invitation into one file that opens without internet.

Reads index.html, downloads its Google Fonts (only the Latin and Arabic parts) and puts them
inside the page, and puts the calendar entry (engagement.ics) inside it too. The result can be
sent as a file (for example on WhatsApp) and opened on a phone with no connection. Only the live
map and the Google Calendar / directions links still need internet.

usage: python3 tools/make_offline.py        (needs internet while building)
writes offline/Ahmed-Amira-Engagement.html
"""
import base64
import json
import pathlib
import re
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'offline' / 'Ahmed-Amira-Engagement.html'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
KEEP = {'latin', 'arabic'}          # subsets the page uses


def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


page = (ROOT / 'index.html').read_text()
link = re.search(r'<link rel="stylesheet" href="(https://fonts\.googleapis\.com/css2\?[^"]+)">', page)
css = get(link.group(1).replace('&amp;', '&')).decode()

# Google's CSS is a list of "/* subset */ @font-face {...}" blocks.
faces, total = [], 0
for subset, block in re.findall(r'/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{[^}]+\})', css):
    if subset not in KEEP:
        continue
    url = re.search(r'url\((https://[^)]+)\)', block).group(1)
    data = get(url)
    total += len(data)
    faces.append(block.replace(url, 'data:font/woff2;base64,' + base64.b64encode(data).decode()))
fonts = '<style>\n/* Fonts packed into the file (Latin and Arabic) */\n' + '\n'.join(faces) + '\n</style>'

page = re.sub(r'<link rel="preconnect"[^>]*>\n', '', page)
page = page.replace(link.group(0), fonts)
ics = (ROOT / 'engagement.ics').read_text()
page = page.replace('<script>\n(() => {', '<script>window.__ICS = ' + json.dumps(ics) + ';</script>\n<script>\n(() => {', 1)

assert 'fonts.googleapis' not in page and 'window.__ICS' in page
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(page)
print(f'{len(faces)} font files ({total / 1024:.0f} KB) packed; {OUT.relative_to(ROOT)}: {OUT.stat().st_size / 1024:.0f} KB')

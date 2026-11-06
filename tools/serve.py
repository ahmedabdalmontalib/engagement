"""Local preview server for the invitation.

Serves the invitation folder and accepts POST /save-og (a JPEG body) from
tools/og.html, writing it to og-image.jpg next to index.html.
"""
import http.server
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8791


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_POST(self):
        if self.path != '/save-og':
            self.send_error(404)
            return
        body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
        if not body.startswith(b'\xff\xd8'):
            self.send_error(400, 'expected a JPEG')
            return
        (ROOT / 'og-image.jpg').write_bytes(body)
        self.send_response(204)
        self.end_headers()


http.server.ThreadingHTTPServer(('127.0.0.1', PORT), Handler).serve_forever()

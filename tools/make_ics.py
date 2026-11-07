"""Write engagement.ics, the calendar file every design links to.

A real file (instead of a generated data: link) is what iPhones and the
WhatsApp in-app browser need to show their "Add to Calendar" sheet.
Run again if the date, time or venue changes:

    python3 tools/make_ics.py
"""
import datetime as dt
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

START = dt.datetime(2026, 11, 26, 19, 0, tzinfo=dt.timezone(dt.timedelta(hours=2)))  # Cairo, +02:00
HOURS = 4
TITLE = 'Ahmed & Amira — Engagement · خطوبة أحمد وأميرة'
LOCATION = '4G Hall, Medical Professions Club, New Minya · قاعة 4G، نادي المهن الطبية، المنيا الجديدة'
DESCRIPTION = 'With love, Ahmed & Amira invite you to celebrate their engagement.\\nبكل الحب، يتشرف أحمد وأميرة بدعوتكم لحضور حفل خطوبتهما.'


def stamp(t):
    return t.astimezone(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')


def esc(s):
    return s.replace(',', '\\,').replace(';', '\\;')


def fold(line):
    """iCalendar lines longer than 75 octets continue on the next line after a space."""
    out, cur = [], b''
    for ch in line:
        b = ch.encode()
        if len(cur) + len(b) > 74:
            out.append(cur.decode())
            cur = b' '
        cur += b
    out.append(cur.decode())
    return '\r\n'.join(out)


lines = [
    'BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Ahmed & Amira//Engagement Invitation//EN',
    'CALSCALE:GREGORIAN', 'METHOD:PUBLISH',
    'BEGIN:VEVENT',
    f'UID:{stamp(START)}-AhmedAmira@invitation',
    f'DTSTAMP:{stamp(dt.datetime.now(dt.timezone.utc))}',
    f'DTSTART:{stamp(START)}',
    f'DTEND:{stamp(START + dt.timedelta(hours=HOURS))}',
    f'SUMMARY:{esc(TITLE)}',
    f'LOCATION:{esc(LOCATION)}',
    f'DESCRIPTION:{esc(DESCRIPTION)}',
    'BEGIN:VALARM', 'TRIGGER:-P1D', 'ACTION:DISPLAY', f'DESCRIPTION:{esc(TITLE)}', 'END:VALARM',
    'END:VEVENT', 'END:VCALENDAR',
]
(ROOT / 'engagement.ics').write_bytes(('\r\n'.join(fold(l) for l in lines) + '\r\n').encode())
print('wrote engagement.ics')

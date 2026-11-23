# Ahmed & Amira — Engagement Invitation

A digital engagement invitation, made to be opened from a WhatsApp link on a phone.

**Thursday, 26 November 2026 · 7:00 PM**
**4G Hall, Medical Professions Club, New Minya**

Online at <https://ahmedabdalmontalib.github.io/engagement/>

## What guests see

1. A night sky with بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ and the guest's name. The guest touches a star, the sky warps, a blue star and a rose star spiral together, and their stardust writes the names. "By the grace of Allah" (بفضل الله) appears above them.
2. Surah Ar-Rum 30:21 in Quran script (﴿وَمِنْ آيَاتِهِ أَنْ خَلَقَ لَكُم مِّنْ أَنفُسِكُمْ أَزْوَاجًا…﴾), with an English translation on the English page.
3. A short story drawn as a heart-shaped constellation as the page scrolls ("…until Allah brought them together").
4. The date in an orbiting ring with "Add to calendar", a live countdown in four light rings, and the venue with a map and directions.
5. A closing scene: two stars orbiting an infinity sign, and buttons to replay the opening or share the invitation.

After the opening, the invitation scrolls by itself like a film, resting on each part long enough to read it (about a minute in all). Any touch stops it, and the ▶ button in the top bar continues. Set `CONFIG.autoScroll` to `false` to turn this off.

There is no music. Instead there is a soft night ambience made in the page itself (a breeze and crickets, a whoosh when the sky warps, a deep soft glow when the two stars meet), with no instruments; it starts when the guest touches the star, can be turned off on the opening screen (بدون صوت) or with the speaker button in the top bar, and works in the offline file too. The whole invitation is available in **English and Arabic**. It opens in **Arabic**; the EN / عربي button switches at any time, and a link ending in `?lang=en` opens it in English.

## Files

| File | What it is |
| --- | --- |
| `index.html` | The complete invitation: page, styles and script in one file. |
| `og-image.jpg` | The picture WhatsApp shows when the link is shared (1200 × 630). |
| `engagement.ics` | The calendar file for Apple and Outlook (made by `tools/make_ics.py`; run it again if the date, time or venue changes). |
| `stars/`, `issue/`, `lanterns/`, `garden/` | Small pages that forward older links to the invitation. |
| `tools/serve.py` | A small local server for previewing the invitation and saving a new preview picture. |
| `tools/og-stars.html` | Draws `og-image.jpg`. Open it through `serve.py` and it saves the picture next to `index.html`. |

Earlier designs (the envelope, The Engagement Issue, Golden Hour, The Garden Door) were removed from the site on 23 November 2026. They remain in the Git history.

## Sending personal links

Add these to the end of the link:

| Add | Effect |
| --- | --- |
| `?to=The%20Hassan%20Family` | Writes the guest's name on the opening screen. Spaces become `%20`. |
| `?lang=ar` or `?lang=en` | Opens the invitation in that language, whatever the phone's language. |
| `?to=Mona&lang=ar` | Both together. |

Send each link as its own WhatsApp message: WhatsApp shows the picture only for the first link in a message.

## Sending it as a file (works without internet)

```bash
python3 tools/make_offline.py
```

This writes `offline/Ahmed-Amira-Engagement.html`: the whole invitation in one file (about 1 MB) with its fonts and calendar entry inside, so it opens on a phone with no connection after it has been received. Only the live map and the Google Calendar / directions links need internet; without it the map says so. If a phone shows the file with scripts turned off (some previews do), it shows a still version with the Basmala, the verse, the names, the date and the venue. Run the command again after any change to `index.html`.

## Changing the details

All details are at the top of the script in `index.html`:

- **`CONFIG`**: names (English and Arabic), date and time (`dateISO`, with Egypt's `+02:00` offset), venue, map search, and:
  - `mapsLink`: the venue's exact Google Maps share link, if you want directions to go to a specific pin.
  - `defaultLanguage`: `'auto'`, `'en'` or `'ar'`.
- **`TEXT`**: every sentence on the page, in English (`en`) and Arabic (`ar`).

The countdown, calendar entries and all dates on the page update from `dateISO` automatically.

## Access code

The access screen used during testing is turned off (`CONFIG.testAccess.enabled: false`), so anyone with the link goes straight to the invitation. Setting it back to `true` brings the screen back with the same code. The page asks search engines not to list it (`noindex`).

## Previewing on your computer

```bash
python3 tools/serve.py 8791
```

Then open <http://localhost:8791>. To redraw the WhatsApp picture after changing names or the date, open <http://localhost:8791/tools/og-stars.html>; it replaces `og-image.jpg`. The picture's text is written inside that file, so update it there too.

## Putting it online

The site is served by GitHub Pages from the `main` branch of this repository. The WhatsApp preview uses the full address of `og-image.jpg`, set in the `og:image` and `og:url` lines near the top of `index.html`. If the invitation is hosted at a different address, change those two lines to match.
